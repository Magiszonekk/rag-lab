"""Klasyfikacja czasowa przepisów z rozdziałów przejściowych / epizodycznych / końcowych.

Problem (przegląd zestawu v1): rozdziały „przepisy przejściowe i końcowe” mieszają przepisy historyczne
(„w roku 2023 stawka wynosi…”, „przed dniem 1 maja 2004 r.”) z przepisami, które OBOWIĄZUJĄ dziś — np. VAT
art. 146ef ustala obecne stawki 23% / 8%, podczas gdy art. 41 ust. 1 nadal mówi o 22%. Wycięcie całych
rozdziałów usunęłoby z korpusu aktualne stawki VAT, a zostawienie ich bez oznaczenia każe systemowi
odpowiadać stawkami z 2023 r.

Rozwiązanie: każdy artykuł z takiego rozdziału dostaje etykietę względem daty stanu prawnego aktu:
- `in_force` — ma zastosowanie do zdarzeń w dniu stanu prawnego lub później,
- `historical` — dotyczy wyłącznie okresów / zdarzeń zakończonych przed tą datą,
- `conditional` — stosuje się tylko po spełnieniu warunku, który na tę datę nie jest spełniony
  albo nie da się tego ustalić z tekstu (np. ogłoszenie ministra),
Etykiety nadaje model (GPT, temperatura 0) z uzasadnieniem; wynik jest plikiem w repo i podlega przeglądowi.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from raglab.corpus import load_corpus, render_unit
from raglab.ingest.sources import REPO_ROOT
from raglab.llm import LLM, LLMError, parse_json

TRANSITIONAL = re.compile(r"przejściow|końcow|epizodyczn|czasow", re.I)
OUT = REPO_ROOT / "data" / "annotations" / "temporal.jsonl"
MODELS = ["gpt-5.6-terra", "gemini-3.8-flash"]

PROMPT = """Przepis pochodzi z rozdziału „{chapter}” ustawy: {act_name}.
Data stanu prawnego tekstu: {state_date}.

Zaklasyfikuj, czy ten przepis ma praktyczne zastosowanie do zdarzeń w dniu {state_date} lub później:
- "in_force": tak — stosuje się do bieżących zdarzeń (także jeśli jest to reguła z datą początkową w przeszłości
  i bez daty końcowej, albo okres trwa nadal, np. „od 2024 r. do końca 2026 r.”);
- "historical": nie — dotyczy wyłącznie okresów lub zdarzeń zakończonych przed {state_date}
  (np. „w roku 2023”, „przed dniem 1 maja 2004 r.”, rozliczenia za lata ubiegłe, stan epidemii już odwołany);
- "conditional": stosuje się tylko po spełnieniu warunku, którego spełnienia na {state_date} nie da się ustalić
  z samego tekstu (np. zależy od ogłoszenia ministra lub od przyszłego zdarzenia).

Jeśli przepis zmienia lub zastępuje regułę z innego artykułu (np. inna stawka niż w art. 41), podaj go
w "overrides" (np. "art. 41 ust. 1"). Odpowiedz wyłącznie JSON:
{{"label": "in_force|historical|conditional", "reason": "jedno zdanie z kluczową datą", "overrides": []}}

PRZEPIS (art. {number}):
{text}"""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="raglab.annotate_temporal")
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args(argv)
    corpus = load_corpus()
    jobs = []
    for key, act in corpus.items():
        for art in act.articles:
            if art.repealed or not any(TRANSITIONAL.search(p) for p in art.path):
                continue
            jobs.append((key, act, art))
    print(f"{len(jobs)} artykułów do klasyfikacji", file=sys.stderr)
    llm = LLM(MODELS)

    def run(job: tuple[str, object, object]) -> dict[str, object]:
        key, act, art = job
        text = render_unit(art)  # type: ignore[arg-type]
        prompt = PROMPT.format(
            chapter=art.path[-1],  # type: ignore[attr-defined]
            act_name=act.source.name,  # type: ignore[attr-defined]
            state_date=act.state_date,  # type: ignore[attr-defined]
            number=art.number,  # type: ignore[attr-defined]
            text=text[:6000],
        )
        rec: dict[str, object] = {"act": key, "article": art.number}  # type: ignore[attr-defined]
        try:
            c = llm.complete([{"role": "user", "content": prompt}], max_tokens=1500, temperature=0.0)
            d = parse_json(c.text)
            assert isinstance(d, dict) and d.get("label") in ("in_force", "historical", "conditional")
            rec.update(
                label=d["label"], reason=d.get("reason", ""), overrides=d.get("overrides", []), model=c.served_model
            )
        except (LLMError, ValueError, AssertionError) as e:
            rec.update(label="error", reason=str(e)[:200])
        return rec

    with ThreadPoolExecutor(args.workers) as ex:
        results = list(ex.map(run, jobs))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    counts: dict[str, int] = {}
    for r in results:
        k = f"{r['act']}/{r['label']}"
        counts[k] = counts.get(k, 0) + 1
    print(json.dumps(counts, ensure_ascii=False), file=sys.stderr)
    return 0


OVERRIDES = OUT.with_name("temporal_overrides.jsonl")


def load_labels(path: Path = OUT, overrides: Path = OVERRIDES) -> dict[tuple[str, str], str]:
    """(akt, numer artykułu) → etykieta; artykuły spoza rozdziałów przejściowych nie mają wpisu (= in_force).

    Ręczne poprawki z `temporal_overrides.jsonl` mają pierwszeństwo przed etykietami modelu.
    """
    out: dict[tuple[str, str], str] = {}
    for p in (path, overrides):
        if p.exists():
            for line in p.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    r = json.loads(line)
                    out[(r["act"], r["article"])] = r["label"]
    return out


if __name__ == "__main__":
    raise SystemExit(main())
