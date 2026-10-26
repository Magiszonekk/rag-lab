"""Przygotowanie embeddingów Qwen3-8B (D12) dla porównania Sonnet 5.5 vs Opus 5.5 — bez ewaluacji i bez sędziego.

1. przepisania HyDE dla wskazanych modeli (cache data/cache/rewrite.jsonl — klucz zależy od modelu);
2. wektory Qwen3-8B (OpenRouter, DeepInfra przypięty) dla: pytań obu zestawów + tekstów HyDE każdego modelu.
Korpus jest już w cache (5205 fragmentów).

    uv run python -m raglab.search.prepare_qwen --models claude-opus-5-5 claude-sonnet-5-5
"""

from __future__ import annotations

import argparse
import json
import sys

from raglab.llm import load_env
from raglab.search import rewrite as RW
from raglab.search.evaluate import EMBED_MODELS, EVAL_DIR
from raglab.search.index import ApiEmbedder


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="raglab.search.prepare_qwen")
    ap.add_argument("--models", nargs="+", default=["claude-opus-5-5", "claude-sonnet-5-5"])
    ap.add_argument("--sets", nargs="+", default=["golden", "v1"])
    args = ap.parse_args(argv)
    load_env()

    questions: list[str] = []
    for s in args.sets:
        path = EVAL_DIR / f"retrieval_{s}.jsonl"
        questions += [json.loads(x)["question"] for x in path.read_text(encoding="utf-8").splitlines() if x.strip()]
    golden = [json.loads(x)["question"] for x in (EVAL_DIR / "golden" / "golden_v1.jsonl").read_text(
        encoding="utf-8").splitlines() if x.strip()]  # fmt: skip
    questions = list(dict.fromkeys(questions + golden))  # + pytania spoza korpusu (nie ma ich w retrieval_golden)

    texts: list[str] = list(questions)
    original = list(RW.REWRITE_MODELS)
    try:
        for m in args.models:
            RW.REWRITE_MODELS[:] = [m]
            RW.prefetch(questions, ["hyde"], workers=3)  # rzuca wyjątek, gdy któreś przepisanie się nie udało
            mem = RW._load()
            hy = [mem[RW._key("hyde", q)] for q in questions]
            print(f"{m}: HyDE {len(hy)}/{len(questions)}", file=sys.stderr)
            texts += hy
    finally:
        RW.REWRITE_MODELS[:] = original

    name, qp, dp, provider = EMBED_MODELS["qwen3-8b"]  # type: ignore[misc]
    emb = ApiEmbedder(name, provider=provider, query_prefix=qp, doc_prefix=dp)
    before = len(emb._cache)
    emb.encode(list(dict.fromkeys(texts)), is_query=True)
    print(f"Qwen3-8B: nowych wektorów {len(emb._cache) - before}, tokenów {emb.tokens}, koszt ${emb.cost_usd:.4f}",
          file=sys.stderr)  # fmt: skip
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
