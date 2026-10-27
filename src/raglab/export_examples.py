"""Eksport gotowych przykładów dla demo (koncept D9/D10): statyczny JSON z odpowiedziami i śladami.

Przykłady to pytania ze złotego zestawu z odpowiedziami z ewaluacji (cache, bez nowych wywołań modelu) dla
wszystkich wariantów — frontend pokazuje je bez backendu (demo działa przy niedostępnym serwerze domowym).
Do każdego przykładu: ocena sędziego i wynik verify=llm, żeby w trybie porównania było widać różnice.

    uv run python -m raglab.export_examples
"""

from __future__ import annotations

import json
import sys
from datetime import date
from typing import Any

from raglab.ingest.sources import REPO_ROOT
from raglab.rag.evaluate import GOLDEN, RUNS, _cache_key, apply_verify
from raglab.rag.judge import JUDGE_MODELS
from raglab.rag.variants import ANSWER_MODELS, EMBED
from raglab.traces import steps_from_answer

OUT = REPO_ROOT / "web" / "public" / "examples.json"
VARIANTS = ["simple", "hybrid", "hyde", "agentic-strict"]
VARIANT_LABEL = {
    "simple": "Prosty (wektory)",
    "hybrid": "Hybrydowy (BM25 + wektory)",
    "hyde": "Hybrydowy + HyDE",
    "agentic-strict": "Agentowy",
}
# przykłady: różne kategorie, przypadki pokazujące różnice między wariantami i odmowy
EXAMPLE_IDS = [
    "g-vat-01",  # stawka 23% — przepis przejściowy zastępujący art. 41
    "g-vat-07",  # auto 50% — wygrywa tylko agent (dociąga art. 86a ust. 1)
    "g-vat-16",  # kancelaria — agent idzie za odesłaniem do art. 113 ust. 13
    "g-vat-26",  # kasa fiskalna w warsztacie — pytanie potoczne
    "g-pit-02",  # skala podatkowa
    "g-pit-15",  # alimenty 700 zł — verify=llm przycina zdanie
    "g-op-07",  # korekta deklaracji w trakcie postępowania
    "g-ooc-01",  # spoza tematu — odmowa
    "g-ooc-06",  # inna ustawa — odmowa ze wskazaniem
]


def _public(a: dict[str, Any]) -> dict[str, Any]:
    return {
        "answer": a.get("answer", ""),
        "citations": a.get("citations", []),
        "refused": a.get("refused", False),
        "context": [
            {"address": c["address"], "status": c.get("status"), "note": c.get("note"), "text": c["text"]}
            for c in a.get("context", [])
        ],
        "steps": steps_from_answer(a),
        "tokens": (a.get("prompt_tokens") or 0) + (a.get("completion_tokens") or 0),
        "latency_ms": sum((a.get("latency_ms") or {}).values()),
        "verify": a.get("llm_check"),
    }


def main() -> int:
    items = {json.loads(x)["id"]: json.loads(x) for x in GOLDEN.read_text(encoding="utf-8").splitlines() if x}
    cache: dict[str, dict[str, Any]] = {}
    for line in (RUNS / "answer_cache.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        cache[r["key"]] = r["answer"]
    details: dict[tuple[str, str], dict[str, Any]] = {}
    # wyniki serii zgodnej z bieżącą konfiguracją (RAGLAB_ANSWER_MODEL / RAGLAB_EMBED), np. Opus 5.5 + Qwen3-8B
    series = f"{ANSWER_MODELS[0]}__{EMBED}__{JUDGE_MODELS[0].split('/')[-1].split(':')[0]}"
    det_path = REPO_ROOT / "results" / "series" / f"answers_golden_v1.{series}.details.jsonl"
    if not det_path.exists():
        det_path = REPO_ROOT / "results" / "answers_golden_v1.details.jsonl"
    for line in det_path.read_text(encoding="utf-8").splitlines():
        d = json.loads(line)
        details[(d["config"], d["id"])] = d
    out = []
    missing = 0
    for qid in EXAMPLE_IDS:
        it = items[qid]
        ex: dict[str, Any] = {"id": qid, "question": it["question"], "category": it["category"],
                              "reference_answer": it.get("reference_answer"), "variants": {}}  # fmt: skip
        for v in VARIANTS:
            raw = cache.get(_cache_key(v, it["question"]))
            if raw is None:
                missing += 1
                continue
            a = apply_verify(raw, "llm", it["question"])  # z cache verify_llm — bez wywołań modelu, jeśli policzone
            pub = _public(a)
            j = details.get((f"{v}/verify=llm", qid)) or details.get((f"{v}/verify=off", qid))
            pub["judge"] = {"verdict": j["judge"]["verdict"], "reason": j["judge"]["reason"]} if j else None
            ex["variants"][v] = pub
        out.append(ex)
    meta = {
        "generated": str(date.today()),
        "answer_model": ANSWER_MODELS[0],
        "embedding": EMBED,
        "judge_model": JUDGE_MODELS[0],
        "variants": VARIANT_LABEL,
        "disclaimer": "Demo techniczne, nie porada podatkowa. Stan prawny podany przy każdym przepisie.",
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps({"meta": meta, "examples": out}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"zapisano {OUT} ({len(out)} przykładów, brak odpowiedzi: {missing})", file=sys.stderr)
    return 0 if missing == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
