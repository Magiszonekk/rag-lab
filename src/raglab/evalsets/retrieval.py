"""Zestaw wyszukiwania (koncept D6): pytania generowane z wylosowanego ustępu + warstwa potoczna.

Przebieg dla każdej jednostki źródłowej:
1. generator (model A) pisze pytanie, na które odpowiada TEN przepis, bez cytowania jego słów i bez numerów;
2. filtr automatyczny: odrzuca pytania z numerem artykułu / ustępu i pytania kopiujące ≥ 5 kolejnych słów
   z przepisu;
3. walidator (model z INNEJ rodziny niż generator) sprawdza, czy przepis faktycznie odpowiada na pytanie
   i czy pytanie jest jednoznaczne; odrzuca „nie”;
4. warstwa potoczna: trzeci przebieg przerabia część pytań na język potoczny, bez słownictwa ustawy.

Odpowiedź wzorcowa = adres prawny jednostki źródłowej (np. „VAT art. 86 ust. 2a”). Ograniczenie opisane
w koncepcie: generator zna tylko jeden przepis, więc trafienie w inny poprawny przepis liczy się jako pudło.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import re
import sys
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass, field
from datetime import date

from raglab.corpus import Located, iter_units, load_corpus
from raglab.ingest.sources import REPO_ROOT
from raglab.llm import LLM, Completion, LLMError, parse_json

EVAL_DIR = REPO_ROOT / "data" / "eval"
GENERATOR_MODELS = ["claude-sonnet-5", "gpt-5.6-terra"]
# Walidator z innej rodziny niż generator (koncept D7). Gemini 3.5/3.6 miały 2026-10-23 wyczerpaną kwotę
# u Google (model_cooldown) — GPT pierwszy, Gemini 3.8 zapasowo.
VALIDATOR_MODELS = ["gpt-5.6-terra", "gemini-3.8-flash", "gpt-5.6-luna"]
PARAPHRASE_MODELS = ["gemini-3.8-flash", "gpt-5.6-luna"]
COPY_LIMIT = 6  # ≥ tylu kolejnych słów z przepisu = przepisane; jedna poprawka z podaną frazą
QUOTA = {"vat": 100, "pit": 80, "op": 70}
MIN_WORDS, MAX_WORDS = 25, 420
# Przepisy przejściowe / epizodyczne / końcowe (np. stawki VAT „w roku 2023”, limity „na rok 2005”) opisują
# stan sprzed lat. Pytania z nich testują historię, nie obowiązujące prawo — wyłączone z zestawu (przegląd v1).
TRANSITIONAL = re.compile(r"przejściow|końcow|epizodyczn", re.I)

GEN_PROMPT = """Jesteś autorem zestawu testowego dla wyszukiwarki polskich przepisów podatkowych.
Dostajesz jeden przepis ({act_name}, stan prawny {state_date}). Napisz JEDNO pytanie, które zadałby
przedsiębiorca, księgowy lub podatnik, i na które odpowiedź znajduje się w tym przepisie.

Zasady:
- pytanie ma sens bez widzenia przepisu i dotyczy konkretnej sprawy (termin, kwota, warunek, obowiązek, wyjątek);
- jeśli przepis odwołuje się do czegoś z innego miejsca („zawiadomienie, o którym mowa w ust. 1”, „ten podatnik”),
  nazwij w pytaniu, o co chodzi (np. „zawiadomienie o wyborze opodatkowania”), żeby pytanie było jednoznaczne;
- NIE podawaj numerów artykułów, ustępów, punktów ani nazwy „art.”;
- NIE przepisuj fragmentów przepisu — użyj własnych słów (dopuszczalne pojedyncze terminy fachowe);
- jeśli przepis jest czysto techniczny (np. tylko odesłanie, delegacja do rozporządzenia, wejście w życie)
  i nie da się z niego zrobić sensownego pytania — zwróć "skip": true.

Odpowiedz wyłącznie JSON: {{"question": "...", "skip": false}}

PRZEPIS ({address}):
{text}"""

VAL_PROMPT = """Oceń parę: pytanie i przepis prawa podatkowego.
1. "answers": czy przepis zawiera odpowiedź na pytanie (pełną lub zasadniczą)? true/false
2. "specific": czy pytanie jest na tyle konkretne, że wskazuje tę właśnie sprawę (a nie ogólny temat,
   na który odpowiada pół ustawy)? true/false
3. "leaks": czy pytanie zawiera numer przepisu albo przepisane dłuższe fragmenty jego treści? true/false
Odpowiedz wyłącznie JSON: {{"answers": bool, "specific": bool, "leaks": bool, "note": "krótko"}}

PYTANIE: {question}

PRZEPIS ({address}):
{text}"""

PARA_PROMPT = """Przepisz pytanie tak, jak zadałby je zwykły człowiek w rozmowie albo na forum: językiem
potocznym, z konkretną sytuacją z życia, BEZ terminów z ustawy (np. zamiast „podatnik” — „ja”, „firma”;
zamiast „dostawa towarów” — „sprzedaż”; zamiast „zobowiązanie podatkowe” — „podatek do zapłaty”).
Sens pytania musi zostać ten sam — odpowiedź nadal musi wynikać z tego samego przepisu.
Odpowiedz wyłącznie JSON: {{"question": "..."}}

PYTANIE: {question}"""


@dataclass
class Item:
    id: str
    act: str
    state_date: str
    question: str
    answers: list[str]
    origin: str  # generated | paraphrased
    source_address: str
    parent_id: str | None = None
    models: dict[str, str] = field(default_factory=dict)
    validator: dict[str, object] = field(default_factory=dict)
    copied_run: int = 0  # najdłuższy ciąg słów wspólny z przepisem źródłowym (do analizy „leksykalności”)


def candidates(loc_iter: list[Located]) -> list[Located]:
    """Jednostki źródłowe: ustęp (lub artykuł bez ustępów); za długi ustęp → jego punkty."""
    out: list[Located] = []
    for loc in loc_iter:
        u = loc.unit
        if u.repealed or u.version is not None or any(c.version for c in loc.chain):
            continue
        if any(TRANSITIONAL.search(p) for p in loc.article.path):
            continue
        is_para = u.kind == "paragraph"
        is_flat_article = u.kind == "article" and not any(c.kind == "paragraph" for c in u.children)
        parent = loc.chain[-2] if len(loc.chain) > 1 else None
        is_point_of_long = (
            u.kind == "point"
            and parent is not None
            and parent.kind in ("paragraph", "article")
            and len(Located(loc.act, loc.article, loc.chain[:-1]).full_text().split()) > MAX_WORDS
        )
        if not (is_para or is_flat_article or is_point_of_long):
            continue
        n = len(loc.full_text().split())
        if MIN_WORDS <= n <= MAX_WORDS:
            out.append(loc)
    return out


def sample(corpus_units: dict[str, list[Located]], seed: int) -> list[Located]:
    """Losowanie warstwowe: limit na akt, najwyżej 1 jednostka na artykuł (żeby nie przepytać jednego art. 43)."""
    rng = random.Random(seed)
    picked: list[Located] = []
    for act, quota in QUOTA.items():
        by_art: dict[str, list[Located]] = {}
        for loc in corpus_units[act]:
            by_art.setdefault(loc.article.number or "", []).append(loc)
        arts = sorted(by_art)
        rng.shuffle(arts)
        # zapas ×1.6 na odrzucenia filtrów
        for art in arts[: int(quota * 1.6)]:
            picked.append(rng.choice(by_art[art]))
    return picked


_ADDR_LEAK = re.compile(r"\b(art\.|artykuł\w*|ust\.|ustęp\w*|§|pkt)\s*\d", re.I)


def _words(t: str) -> list[str]:
    return re.findall(r"\w+", t.lower())


def longest_copied(question: str, source: str) -> tuple[int, str]:
    """Najdłuższy ciąg kolejnych słów pytania, który występuje też w przepisie (długość, fraza)."""
    q, s = _words(question), _words(source)
    best, phrase = 0, ""
    for n in range(1, len(q) + 1):
        grams = {tuple(s[i : i + n]) for i in range(len(s) - n + 1)}
        hit = next((q[i : i + n] for i in range(len(q) - n + 1) if tuple(q[i : i + n]) in grams), None)
        if hit is None:
            break
        best, phrase = n, " ".join(hit)
    return best, phrase


FIX_PROMPT = """Twoje pytanie przepisuje z przepisu frazę: „{phrase}”. Napisz je jeszcze raz własnymi słowami
(sens bez zmian, utarty termin fachowy może zostać, ale nie cały ciąg). Odpowiedz wyłącznie JSON:
{{"question": "..."}}"""


def _id(*parts: str) -> str:
    return hashlib.sha1("|".join(parts).encode()).hexdigest()[:10]


def process(
    loc: Located, act_name: str, state: str, gen: LLM, val: LLM, para: LLM, para_p: float, rng: random.Random
) -> tuple[list[Item], dict[str, object]]:
    text = loc.full_text()
    log: dict[str, object] = {"address": loc.address}
    try:
        c: Completion = gen.complete(
            [
                {
                    "role": "user",
                    "content": GEN_PROMPT.format(act_name=act_name, state_date=state, address=loc.address, text=text),
                }
            ],
            max_tokens=2000,
            temperature=0.8,
        )
        g = parse_json(c.text)
        assert isinstance(g, dict)
    except (LLMError, ValueError, AssertionError) as e:
        log["status"] = f"gen_error:{type(e).__name__}"
        return [], log
    if g.get("skip"):
        log["status"] = "skip_by_generator"
        return [], log
    q = str(g.get("question", "")).strip()
    run, phrase = longest_copied(q, text)
    if q and run >= COPY_LIMIT:
        try:
            msgs = [
                {
                    "role": "user",
                    "content": GEN_PROMPT.format(act_name=act_name, state_date=state, address=loc.address, text=text),
                },
                {"role": "assistant", "content": c.text},
                {"role": "user", "content": FIX_PROMPT.format(phrase=phrase)},
            ]
            fixed = parse_json(gen.complete(msgs, max_tokens=2000, temperature=0.8).text)
            assert isinstance(fixed, dict)
            log["first_question"] = q
            q = str(fixed.get("question", "")).strip()
            run, phrase = longest_copied(q, text)
        except (LLMError, ValueError, AssertionError):
            pass
    if not q or _ADDR_LEAK.search(q) or run >= COPY_LIMIT:
        log["status"] = "filtered_leak"
        log["question"] = q
        log["copied"] = phrase
        return [], log
    try:
        v = val.complete(
            [{"role": "user", "content": VAL_PROMPT.format(question=q, address=loc.address, text=text)}],
            max_tokens=2500,
            temperature=0.0,
        )
        vd = parse_json(v.text)
        assert isinstance(vd, dict)
    except (LLMError, ValueError, AssertionError) as e:
        log["status"] = f"val_error:{type(e).__name__}"
        log["question"] = q
        log["error"] = str(e)[:200]
        return [], log
    if not (vd.get("answers") and vd.get("specific")) or vd.get("leaks"):
        log["status"] = "rejected_by_validator"
        log["question"] = q
        log["validator"] = vd
        return [], log
    base = Item(
        id=_id(loc.address, q),
        act=loc.act,
        state_date=state,
        question=q,
        answers=[loc.address],
        origin="generated",
        source_address=loc.address,
        models={"generator": c.served_model, "validator": v.served_model},
        validator=vd,
        copied_run=run,
    )
    items = [base]
    if rng.random() < para_p:
        try:
            p = para.complete(
                [{"role": "user", "content": PARA_PROMPT.format(question=q)}], max_tokens=2000, temperature=0.9
            )
            pd = parse_json(p.text)
            pq = str(pd.get("question", "")).strip() if isinstance(pd, dict) else ""
            if pq and not _ADDR_LEAK.search(pq):
                items.append(
                    Item(
                        id=_id(loc.address, pq),
                        act=loc.act,
                        state_date=state,
                        question=pq,
                        answers=[loc.address],
                        origin="paraphrased",
                        source_address=loc.address,
                        parent_id=base.id,
                        models={**base.models, "paraphraser": p.served_model},
                        copied_run=longest_copied(pq, text)[0],
                    )
                )
        except (LLMError, ValueError, AttributeError):
            pass
    log["status"] = "ok"
    return items, log


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="raglab.evalsets.retrieval")
    ap.add_argument("--version", default="v1")
    ap.add_argument("--seed", type=int, default=20261023)
    ap.add_argument("--paraphrase", type=float, default=0.4, help="odsetek pytań z wersją potoczną")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--limit", type=int, default=0, help="tylko N jednostek (próba)")
    args = ap.parse_args(argv)

    corpus = load_corpus()
    units = {k: candidates(list(iter_units(a))) for k, a in corpus.items()}
    picked = sample(units, args.seed)
    if args.limit:
        picked = picked[: args.limit]
    print({k: len(v) for k, v in units.items()}, "kandydatów;", len(picked), "wylosowanych", file=sys.stderr)

    gen, val, para = LLM(GENERATOR_MODELS), LLM(VALIDATOR_MODELS), LLM(PARAPHRASE_MODELS)
    EVAL_DIR.mkdir(parents=True, exist_ok=True)
    out_path = EVAL_DIR / f"retrieval_{args.version}.jsonl"
    log_path = EVAL_DIR / f"retrieval_{args.version}.log.jsonl"
    lock = threading.Lock()
    kept: dict[str, int] = {}
    with (
        out_path.open("w", encoding="utf-8") as out,
        log_path.open("w", encoding="utf-8") as lg,
        ThreadPoolExecutor(args.workers) as ex,
    ):
        futs = {}
        for i, loc in enumerate(picked):
            act = corpus[loc.act]
            futs[
                ex.submit(
                    process,
                    loc,
                    act.source.name,
                    str(act.state_date),
                    gen,
                    val,
                    para,
                    args.paraphrase,
                    random.Random(args.seed + i),
                )
            ] = loc
        for n, f in enumerate(as_completed(futs), 1):
            items, log = f.result()
            loc = futs[f]
            with lock:
                for it in items:
                    if it.origin == "generated" and kept.get(it.act, 0) >= QUOTA[it.act]:
                        break
                    if it.origin == "generated":
                        kept[it.act] = kept.get(it.act, 0) + 1
                    out.write(json.dumps(asdict(it), ensure_ascii=False) + "\n")
                lg.write(json.dumps(log, ensure_ascii=False) + "\n")
                out.flush()
                lg.flush()
            if n % 20 == 0:
                print(f"{n}/{len(picked)} {kept}", file=sys.stderr)
    meta = {
        "version": args.version,
        "created": str(date.today()),
        "seed": args.seed,
        "quota": QUOTA,
        "kept_generated": kept,
        "models": {"generator": GENERATOR_MODELS, "validator": VALIDATOR_MODELS, "paraphraser": PARAPHRASE_MODELS},
        "corpus": {
            k: {"eli": a.source.eli, "sha256": a.source.sha256, "state_date": str(a.state_date)}
            for k, a in corpus.items()
        },
        "prompts_sha1": {
            n: hashlib.sha1(p.encode()).hexdigest()[:10]
            for n, p in [("gen", GEN_PROMPT), ("val", VAL_PROMPT), ("para", PARA_PROMPT)]
        },
    }
    (EVAL_DIR / f"retrieval_{args.version}.meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8"
    )
    print(json.dumps(meta["kept_generated"]), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
