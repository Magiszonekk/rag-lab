"""Ewaluacja wyszukiwania na zestawie wyszukiwania (koncept D6, D8): recall@k, MRR, act accuracy.

Trafienie: fragment pokrywa adres wzorcowy (fragment zawiera ustęp/punkt wzorcowy) ALBO adres wzorcowy jest
przodkiem/potomkiem adresu pokrytego przez fragment (ustęp wzorcowy zawiera fragment-grupę punktów). Liczymy
pierwszą pozycję trafienia w rankingu fragmentów.

Raport: wartości z 95% przedziałami ufności (bootstrap po pytaniach) i porównania par konfiguracji
na tych samych pytaniach (test McNemara dla hit@5, bootstrap różnicy MRR).

    uv run python -m raglab.search.evaluate                    # pełna macierz
    uv run python -m raglab.search.evaluate --configs bm25-morfeusz2 --ci-gate   # bramka CI (D8)
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
import time
from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from typing import Any

from raglab.corpus import load_corpus
from raglab.ingest.sources import REPO_ROOT
from raglab.search.chunking import Chunk, est_tokens, fixed, structural
from raglab.search.index import ApiEmbedder, BM25Index, Embedder, Hit, VectorIndex, demote_historical, rrf
from raglab.search.normalize import get_normalizer

EVAL_DIR = REPO_ROOT / "data" / "eval"
RESULTS_DIR = REPO_ROOT / "results"
KS = (1, 3, 5, 10, 20)
# Qwen3-Embedding: instrukcja zadania tylko przy pytaniu (format z karty modelu), dokumenty bez prefiksu.
QWEN3_TASK = "Given a question about Polish tax law, retrieve the statutory provision that answers it"
EMBED_MODELS: dict[str, tuple[str, str, str] | tuple[str, str, str, str]] = {
    "mmlw-base": ("sdadas/mmlw-roberta-base", "zapytanie: ", ""),
    # (model, prefiks pytania, prefiks dokumentu, provider przypięty w OpenRouter) — przez API
    "qwen3-8b": ("qwen/qwen3-embedding-8b", f"Instruct: {QWEN3_TASK}\nQuery: ", "", "DeepInfra"),
}


_CACHE_OBJS: list[Embedder | ApiEmbedder] = []
GOLD_WORDS: dict[str, int] = {}  # adres → liczba słów jednostki z potomkami (wypełniane w main)


def _in_subtree(a: str, gold: str) -> bool:
    # „VAT art. 2” nie może trafiać w „VAT art. 2a”: wymagamy granicy słowa (spacja)
    return a == gold or a.startswith(gold + " ")


def is_hit(chunk: Chunk, gold: str, *, strict: bool = True) -> bool:
    """Trafienie.

    luźne: fragment dotyka jednostki wzorcowej albo jej przodka/potomka (choćby jednym słowem);
    ścisłe (domyślne): fragment zawiera ≥ 50% słów jednostki wzorcowej ALBO ≥ 50% fragmentu to jednostka
    wzorcowa (fragment-kawałek długiego ustępu). Ścisła miara nie nagradza długich okien za samo „dotknięcie”.
    """
    if not strict:
        return any(_in_subtree(a, gold) or gold.startswith(a + " ") for a in chunk.covers)
    overlap = sum(n for a, n in chunk.own_words.items() if _in_subtree(a, gold))
    if overlap == 0:
        return False
    total = GOLD_WORDS.get(gold) or overlap
    return overlap / total >= 0.5 or overlap / max(chunk.body_words, 1) >= 0.5


@dataclass
class QResult:
    qid: str
    act: str
    origin: str
    rank: int | None  # 1-based pozycja pierwszego trafienia, None = brak w top-20
    top_act: str | None
    tokens_at5: int = 0  # ile tokenów kontekstu dałoby top-5 (koszt dla modelu odpowiadającego)


def run_config(search: Callable[[str], list[Hit]], items: list[dict[str, Any]]) -> list[QResult]:
    out: list[QResult] = []
    for it in items:
        hits = search(str(it["question"]))
        golds = [str(a) for a in it["answers"]]
        rank = next((i for i, h in enumerate(hits, 1) if any(is_hit(h.chunk, g) for g in golds)), None)
        tok5 = sum(est_tokens(h.chunk.text) for h in hits[:5])
        out.append(
            QResult(str(it["id"]), str(it["act"]), str(it["origin"]), rank, hits[0].chunk.act if hits else None, tok5)
        )
    return out


def metrics(rs: list[QResult]) -> dict[str, float]:
    n = len(rs)
    m: dict[str, float] = {f"recall@{k}": sum(1 for r in rs if r.rank and r.rank <= k) / n for k in KS}
    m["mrr@20"] = sum(1 / r.rank for r in rs if r.rank) / n
    m["act_acc@1"] = sum(1 for r in rs if r.top_act == r.act) / n
    m["tokens@5"] = sum(r.tokens_at5 for r in rs) / n
    return m


def bootstrap_ci(rs: list[QResult], key: str, b: int = 2000, seed: int = 0) -> tuple[float, float]:
    rng = random.Random(seed)
    vals = []
    for _ in range(b):
        sample = [rs[rng.randrange(len(rs))] for _ in rs]
        vals.append(metrics(sample)[key])
    vals.sort()
    return vals[int(0.025 * b)], vals[int(0.975 * b)]


def mcnemar(a: list[QResult], b: list[QResult], k: int = 5) -> dict[str, float]:
    """Dokładny test McNemara (dwumianowy) dla hit@k na tych samych pytaniach."""

    def hit(r: QResult) -> bool:
        return bool(r.rank and r.rank <= k)

    only_a = sum(1 for x, y in zip(a, b, strict=True) if hit(x) and not hit(y))
    only_b = sum(1 for x, y in zip(a, b, strict=True) if hit(y) and not hit(x))
    n = only_a + only_b
    if n == 0:
        return {"only_a": 0, "only_b": 0, "p": 1.0}
    kmin = min(only_a, only_b)
    p = 2 * sum(math.comb(n, i) for i in range(kmin + 1)) / 2**n
    return {"only_a": only_a, "only_b": only_b, "p": min(1.0, p)}


def load_items(version: str) -> list[dict[str, Any]]:
    path = EVAL_DIR / f"retrieval_{version}.jsonl"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _with_rewrite(
    q: str,
    strategy: str,
    bm25: Callable[..., BM25Index],
    vec: Callable[..., VectorIndex],
    model: str = "mmlw-base",
) -> list[Hit]:
    from raglab.search.rewrite import rewrite

    b, v = bm25("structural", "morfeusz2"), vec("structural", model)
    rankings = [b.search(q, 50), v.search(q, 50)]
    for s in strategy.split("+"):
        rq = rewrite(q, s)
        rankings += [b.search(rq, 50), v.search(rq, 50)]
    return demote_historical(rrf(*rankings, top=20))


def build_configs(names: list[str]) -> dict[str, Callable[[str], list[Hit]]]:
    corpus = load_corpus()
    chunk_sets: dict[str, list[Chunk]] = {}

    def chunks(kind: str) -> list[Chunk]:
        if kind not in chunk_sets:
            if kind == "structural":
                chunk_sets[kind] = [c for act in corpus.values() for c in structural(act)]
            elif kind == "fixed":
                chunk_sets[kind] = [c for act in corpus.values() for c in fixed(act)]
            elif kind == "fixed128":  # okna wielkości mediany fragmentu strukturalnego (~107 tok.)
                chunk_sets[kind] = [c for act in corpus.values() for c in fixed(act, window=128, overlap=16)]
        return chunk_sets[kind]

    cache: dict[str, object] = {}
    _CACHE_OBJS.clear()

    def bm25(kind: str, lem: str) -> BM25Index:
        key = f"bm25:{kind}:{lem}"
        if key not in cache:
            cache[key] = BM25Index(chunks(kind), get_normalizer(lem))
        return cache[key]  # type: ignore[return-value]

    def vec(kind: str, model: str) -> VectorIndex:
        key = f"vec:{kind}:{model}"
        if key not in cache:
            spec = EMBED_MODELS[model]
            emb: Embedder | ApiEmbedder
            if len(spec) == 4:
                name, qp, dp, provider = spec
                emb = ApiEmbedder(name, provider=provider, query_prefix=qp, doc_prefix=dp)
            else:
                name, qp, dp = spec[:3]
                emb = Embedder(name, query_prefix=qp, doc_prefix=dp)
            _CACHE_OBJS.append(emb)
            cache[key] = VectorIndex(chunks(kind), emb)
        return cache[key]  # type: ignore[return-value]

    available: dict[str, Callable[[], Callable[[str], list[Hit]]]] = {
        "bm25-none": lambda: lambda q: bm25("structural", "none").search(q, 20),
        "bm25-morfeusz2": lambda: lambda q: bm25("structural", "morfeusz2").search(q, 20),
        "vec-mmlw-base": lambda: lambda q: vec("structural", "mmlw-base").search(q, 20),
        "hybrid-rrf": lambda: (
            lambda q: rrf(
                bm25("structural", "morfeusz2").search(q, 50), vec("structural", "mmlw-base").search(q, 50), top=20
            )
        ),
        "hybrid-rrf-demote": lambda: (
            lambda q: demote_historical(
                rrf(bm25("structural", "morfeusz2").search(q, 50), vec("structural", "mmlw-base").search(q, 50), top=20)
            )
        ),
        "hybrid-rrf-w2": lambda: (
            lambda q: rrf(
                bm25("structural", "morfeusz2").search(q, 50),
                vec("structural", "mmlw-base").search(q, 50),
                top=20,
                weights=(1.0, 2.0),
            )
        ),
        "hybrid-rrf-w2-demote": lambda: (
            lambda q: demote_historical(
                rrf(
                    bm25("structural", "morfeusz2").search(q, 50),
                    vec("structural", "mmlw-base").search(q, 50),
                    top=20,
                    weights=(1.0, 2.0),
                )
            )
        ),
        # przepisywanie pytania (search/rewrite.py): RRF wyników dla pytania oryginalnego i przepisanego
        "hybrid-rewrite": lambda: lambda q: _with_rewrite(q, "rewrite", bm25, vec),
        "hybrid-hyde": lambda: lambda q: _with_rewrite(q, "hyde", bm25, vec),
        "hybrid-rewrite-hyde": lambda: lambda q: _with_rewrite(q, "rewrite+hyde", bm25, vec),
        # porównanie modeli embeddingowych (D12): Qwen3-Embedding-8B przez API, provider przypięty
        "vec-qwen3-8b": lambda: lambda q: vec("structural", "qwen3-8b").search(q, 20),
        "hybrid-rrf-qwen3-8b": lambda: (
            lambda q: rrf(
                bm25("structural", "morfeusz2").search(q, 50), vec("structural", "qwen3-8b").search(q, 50), top=20
            )
        ),
        "hybrid-hyde-qwen3-8b": lambda: lambda q: _with_rewrite(q, "hyde", bm25, vec, "qwen3-8b"),
        "fixed-bm25-morfeusz2": lambda: lambda q: bm25("fixed", "morfeusz2").search(q, 20),
        "fixed-vec-mmlw-base": lambda: lambda q: vec("fixed", "mmlw-base").search(q, 20),
        "fixed128-bm25-morfeusz2": lambda: lambda q: bm25("fixed128", "morfeusz2").search(q, 20),
        "fixed128-vec-mmlw-base": lambda: lambda q: vec("fixed128", "mmlw-base").search(q, 20),
    }
    return {n: available[n]() for n in names}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="raglab.search.evaluate")
    ap.add_argument("--version", default="v1")
    ap.add_argument(
        "--configs",
        nargs="*",
        default=[
            "bm25-none",
            "bm25-morfeusz2",
            "vec-mmlw-base",
            "hybrid-rrf",
            "fixed-bm25-morfeusz2",
            "fixed-vec-mmlw-base",
            "fixed128-bm25-morfeusz2",
            "fixed128-vec-mmlw-base",
        ],
    )
    ap.add_argument(
        "--ci-gate",
        action="store_true",
        help="porównaj z results/retrieval_baseline.json i zakończ kodem 1 przy spadku",
    )
    ap.add_argument("--max-drop", type=float, default=0.02, help="dopuszczalny spadek recall@5 (bramka CI)")
    ap.add_argument("--write-baseline", action="store_true", help="zapisz baseline bramki CI (nie nadpisuje raportu)")
    ap.add_argument("--out", default=None, help="nazwa pliku raportu w results/ (domyślnie retrieval_<wersja>.json)")
    args = ap.parse_args(argv)

    items = load_items(args.version)
    rw = {
        s
        for c in args.configs
        if c in ("hybrid-rewrite", "hybrid-hyde", "hybrid-rewrite-hyde")
        for s in {"hybrid-rewrite": ["rewrite"], "hybrid-hyde": ["hyde"], "hybrid-rewrite-hyde": ["rewrite", "hyde"]}[c]
    }
    if rw:
        from raglab.search.rewrite import prefetch

        prefetch([it["question"] for it in items], sorted(rw))
    from raglab.corpus import iter_units as _iter

    for corpus_act in load_corpus().values():
        own = {loc.address: len((loc.unit.text + " " + loc.unit.tail).split()) for loc in _iter(corpus_act)}
        for addr in own:
            GOLD_WORDS[addr] = sum(n for a, n in own.items() if _in_subtree(a, addr))
    configs = build_configs(args.configs)
    per_config: dict[str, list[QResult]] = {}
    report: dict[str, object] = {
        "date": str(date.today()),
        "testset": f"retrieval_{args.version}",
        "n": len(items),
        "configs": {},
    }
    for name, search in configs.items():
        t0 = time.monotonic()
        rs = run_config(search, items)
        dt = time.monotonic() - t0
        per_config[name] = rs
        for obj in list(_CACHE_OBJS):
            obj.save()
        entry: dict[str, object] = {"latency_ms_per_query": round(1000 * dt / len(items), 1)}
        for subset, sel in (
            ("all", rs),
            ("generated", [r for r in rs if r.origin == "generated"]),
            ("paraphrased", [r for r in rs if r.origin == "paraphrased"]),
        ):
            m = metrics(sel)
            ci = {k: bootstrap_ci(sel, k) for k in ("recall@5", "mrr@20")}
            entry[subset] = {
                "n": len(sel),
                **{k: round(v, 3) for k, v in m.items()},
                "ci95": {k: [round(lo, 3), round(hi, 3)] for k, (lo, hi) in ci.items()},
            }
        for act in ("vat", "pit", "op"):
            sel = [r for r in rs if r.act == act]
            entry[f"act:{act}"] = {"n": len(sel), "recall@5": round(metrics(sel)["recall@5"], 3)}
        report["configs"][name] = entry  # type: ignore[index]
        a = entry["all"]
        print(
            f"{name:24} R@1 {a['recall@1']:.3f}  R@5 {a['recall@5']:.3f} {a['ci95']['recall@5']}  "  # type: ignore[index]
            f"R@20 {a['recall@20']:.3f}  MRR {a['mrr@20']:.3f}  act@1 {a['act_acc@1']:.3f}  "  # type: ignore[index]
            f"potoczne R@5 {entry['paraphrased']['recall@5']:.3f}  "  # type: ignore[index]
            f"tok@5 {a['tokens@5']:.0f}  {entry['latency_ms_per_query']} ms/q",  # type: ignore[index]
            file=sys.stderr,
        )
    names = list(per_config)
    pairs = {}
    for i, x in enumerate(names):
        for y in names[i + 1 :]:
            pairs[f"{x} vs {y}"] = mcnemar(per_config[x], per_config[y])
    report["mcnemar_hit@5"] = pairs
    per_q = {n: {r.qid: r.rank for r in rs} for n, rs in per_config.items()}
    RESULTS_DIR.mkdir(exist_ok=True)
    out = RESULTS_DIR / (args.out or f"retrieval_{args.version}.json")
    if not args.ci_gate and not args.write_baseline:
        out.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
        out.with_suffix(".per_question.json").write_text(json.dumps(per_q), encoding="utf-8")
        print(f"zapisano {out}", file=sys.stderr)
    base_path = RESULTS_DIR / "retrieval_baseline.json"
    if args.write_baseline:
        base = {n: report["configs"][n]["all"]["recall@5"] for n in names}  # type: ignore[index]
        base_path.write_text(
            json.dumps({"testset": f"retrieval_{args.version}", "recall@5": base}, indent=1), encoding="utf-8"
        )
    if args.ci_gate:
        base = json.loads(base_path.read_text())["recall@5"]
        failed = False
        for n in names:
            now = report["configs"][n]["all"]["recall@5"]  # type: ignore[index]
            ref = base.get(n)
            status = "OK"
            if ref is not None and now < ref - args.max_drop:
                status = "SPADEK"
                failed = True
            print(f"[bramka] {n}: recall@5 {now:.3f} (baseline {ref}) {status}")
        return 1 if failed else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
