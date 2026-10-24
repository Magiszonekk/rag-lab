"""Ewaluacja odpowiedzi na złotym zestawie (koncept D5, D7, D6a).

Dla każdego pytania i wariantu: odpowiedź (cache na dysku — ponowne liczenie metryk bez wywołań LLM),
sprawdzanie `cite`, metryki deterministyczne (key_facts, cytaty) i sędzia LLM.

Poziomy `verify` (D5):
- `off`  — odpowiedź jak jest;
- `cite` — jeśli sprawdzanie deterministyczne nie przechodzi (nieistniejący cytat albo liczba bez pokrycia
            w cytowanych przepisach), odpowiedź jest zastępowana odmową „nie mogę potwierdzić …”;
- `llm`  — M2 (sprawdzanie zdań przez LLM).

    uv run python -m raglab.rag.evaluate --variants simple hybrid
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from typing import Any

from raglab.ingest.sources import REPO_ROOT
from raglab.llm import LLM
from raglab.rag.judge import JUDGE_MODELS, JUDGE_VERSION, judge
from raglab.rag.variants import ANSWER_MODELS, SYSTEM_PROMPT, answer
from raglab.rag.verify import check_cite, citation_recall, key_facts_present

GOLDEN = REPO_ROOT / "data" / "eval" / "golden" / "golden_v1.jsonl"
RUNS = REPO_ROOT / "results" / "answers"
CITE_REFUSAL = "Nie mogę potwierdzić tej odpowiedzi w przepisach, które mam — sprawdzenie cytatów i liczb nie przeszło."


def _cache_key(variant: str, question: str) -> str:
    h = hashlib.sha1(f"{variant}|{ANSWER_MODELS}|{SYSTEM_PROMPT}|{question}".encode()).hexdigest()[:16]
    return h


def apply_verify(ans: dict[str, Any], level: str, question: str) -> dict[str, Any]:
    if level == "off" or ans.get("refused") or ans.get("error"):
        return ans
    cc = check_cite(ans["answer"], ans["citations"], [c["address"] for c in ans["context"]], question)
    ans = {
        **ans,
        "cite_check": {"passed": cc.passed, "unsupported": cc.unsupported_numbers, "invalid": cc.invalid_citations},
    }
    if level == "cite" and not cc.passed:
        return {**ans, "answer": CITE_REFUSAL, "refused": True, "verify_blocked": True}
    return ans


def is_ooc(item: dict[str, Any]) -> bool:
    return bool(item["category"] == "out_of_corpus")


def should_refuse(item: dict[str, Any]) -> bool:
    return item.get("expected_behavior") in ("refuse", "refuse_with_pointer")


def bootstrap(vals: list[float], b: int = 2000, seed: int = 0) -> tuple[float, float]:
    if not vals:
        return (0.0, 0.0)
    rng = random.Random(seed)
    means = sorted(sum(vals[rng.randrange(len(vals))] for _ in vals) / len(vals) for _ in range(b))
    return means[int(0.025 * b)], means[int(0.975 * b)]


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    ans_rows = [r for r in rows if not is_ooc(r["item"])]
    ref_rows = [r for r in rows if should_refuse(r["item"])]
    ooc_other = [r for r in rows if is_ooc(r["item"]) and not should_refuse(r["item"])]
    correct = [1.0 if r["judge"]["verdict"] == "correct" else 0.0 for r in ans_rows]
    acceptable = [1.0 if r["judge"]["verdict"] in ("correct", "partial") else 0.0 for r in ans_rows]
    kf = [r["key_facts"] for r in ans_rows]
    faithful = [1.0 if r["judge"]["faithful"] else 0.0 for r in rows if r["judge"]["faithful"] is not None]
    false_ref = [1.0 if r["answer"]["refused"] else 0.0 for r in ans_rows]
    good_ref = [1.0 if r["answer"]["refused"] else 0.0 for r in ref_rows]
    ooc_ok = [1.0 if r["judge"]["verdict"] in ("refusal_ok", "correct") else 0.0 for r in ooc_other]
    tokens = [r["answer"]["prompt_tokens"] + r["answer"]["completion_tokens"] for r in rows]
    lat = sorted(sum(r["answer"]["latency_ms"].values()) for r in rows if r["answer"]["latency_ms"])

    def m(v: list[float]) -> dict[str, Any]:
        lo, hi = bootstrap(v)
        return {"mean": round(sum(v) / len(v), 3) if v else None, "ci95": [round(lo, 3), round(hi, 3)], "n": len(v)}

    return {
        "answerable_correct": m(correct),
        "answerable_correct_or_partial": m(acceptable),
        "key_facts": m(kf),
        "citation_recall": m([r["citation_recall"] for r in ans_rows]),
        "faithful": m(faithful),
        "false_refusals": m(false_ref),
        "correct_refusals": m(good_ref),
        "ooc_other_ok": m(ooc_ok),
        "verdicts": dict(Counter(r["judge"]["verdict"] for r in rows)),
        "tokens_per_question": round(sum(tokens) / len(tokens)) if tokens else 0,
        "latency_ms_p50": lat[len(lat) // 2] if lat else None,
        "latency_ms_p95": lat[int(0.95 * len(lat))] if lat else None,
        "errors": sum(1 for r in rows if r["answer"].get("error")),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="raglab.rag.evaluate")
    ap.add_argument("--variants", nargs="*", default=["simple", "hybrid"])
    ap.add_argument("--verify", nargs="*", default=["off", "cite"])
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--limit", type=int, default=0)
    args = ap.parse_args(argv)

    items = [json.loads(line) for line in GOLDEN.read_text(encoding="utf-8").splitlines() if line.strip()]
    if args.limit:
        items = items[: args.limit]
    RUNS.mkdir(parents=True, exist_ok=True)
    cache_path = RUNS / "answer_cache.jsonl"
    cache: dict[str, dict[str, Any]] = {}
    if cache_path.exists():
        for line in cache_path.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            cache[r["key"]] = r["answer"]
    judge_cache_path = RUNS / "judge_cache.jsonl"
    jcache: dict[str, dict[str, Any]] = {}
    if judge_cache_path.exists():
        for line in judge_cache_path.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            jcache[r["key"]] = r["judge"]

    answer_llm = LLM(ANSWER_MODELS)
    judge_llm = LLM(JUDGE_MODELS)

    # 1) odpowiedzi (sekwencyjnie po wariantach — wyszukiwanie ładuje modele raz; generacja równolegle)
    for variant in args.variants:
        todo = [it for it in items if _cache_key(variant, it["question"]) not in cache]
        print(f"{variant}: {len(todo)} odpowiedzi do wygenerowania", file=sys.stderr)

        def gen(it: dict[str, Any], variant: str = variant) -> tuple[str, dict[str, Any]]:
            return _cache_key(variant, it["question"]), answer(it["question"], variant, answer_llm).to_json()

        if todo:
            gen(todo[0])  # rozgrzanie indeksów w wątku głównym
        with ThreadPoolExecutor(args.workers) as ex, cache_path.open("a", encoding="utf-8") as f:
            for key, a in ex.map(gen, todo):
                if a.get("error"):
                    print(f"  błąd: {a['error'][:150]}", file=sys.stderr)
                    cache[key] = a  # liczy się jako błąd, ale bez zapisu — ponowienie w następnym przebiegu
                    continue
                cache[key] = a
                f.write(json.dumps({"key": key, "answer": a}, ensure_ascii=False) + "\n")
                f.flush()

    # 2) verify + metryki + sędzia
    report: dict[str, Any] = {
        "date": str(date.today()),
        "testset": "golden_v1",
        "n": len(items),
        "answer_models": ANSWER_MODELS,
        "judge_models": JUDGE_MODELS,
        "configs": {},
    }
    all_rows: dict[str, list[dict[str, Any]]] = {}
    for variant in args.variants:
        for level in args.verify:
            name = f"{variant}/verify={level}"
            jobs = []
            for it in items:
                raw = cache[_cache_key(variant, it["question"])]
                a = apply_verify(raw, level, it["question"])
                jobs.append((it, a))

            def score(job: tuple[dict[str, Any], dict[str, Any]]) -> dict[str, Any]:
                it, a = job
                jkey = hashlib.sha1(
                    json.dumps([JUDGE_VERSION, it["id"], a["answer"], a["refused"]], ensure_ascii=False).encode()
                ).hexdigest()
                j = jcache.get(jkey) or judge(it, a, judge_llm)
                return {
                    "jkey": jkey,
                    "item": it,
                    "answer": a,
                    "judge": j,
                    "key_facts": key_facts_present(a["answer"], it.get("key_facts", [])) if not a["refused"] else 0.0,
                    "citation_recall": citation_recall(
                        a["citations"], it.get("answers", []), it.get("required_all", False)
                    ),
                }

            with ThreadPoolExecutor(args.workers) as ex:
                rows = list(ex.map(score, jobs))
            with judge_cache_path.open("a", encoding="utf-8") as f:
                for r in rows:
                    if r["jkey"] not in jcache and r["judge"]["verdict"] != "error":
                        jcache[r["jkey"]] = r["judge"]
                        f.write(json.dumps({"key": r["jkey"], "judge": r["judge"]}, ensure_ascii=False) + "\n")
            all_rows[name] = rows
            s = summarize(rows)
            report["configs"][name] = s
            print(
                f"{name:22} poprawne {s['answerable_correct']['mean']} {s['answerable_correct']['ci95']}  "
                f"+częściowe {s['answerable_correct_or_partial']['mean']}  key_facts {s['key_facts']['mean']}  "
                f"cytaty {s['citation_recall']['mean']}  wierne {s['faithful']['mean']}  "
                f"odmowy ok {s['correct_refusals']['mean']} (n={s['correct_refusals']['n']})  "
                f"fałszywe odmowy {s['false_refusals']['mean']}  tok/q {s['tokens_per_question']}  "
                f"p50 {s['latency_ms_p50']} ms  błędy {s['errors']}",
                file=sys.stderr,
            )
    out = REPO_ROOT / "results" / "answers_golden_v1.json"
    out.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    detail = REPO_ROOT / "results" / "answers_golden_v1.details.jsonl"
    with detail.open("w", encoding="utf-8") as f:
        for name, rows in all_rows.items():
            for r in rows:
                f.write(
                    json.dumps(
                        {
                            "config": name,
                            "id": r["item"]["id"],
                            "category": r["item"]["category"],
                            "question": r["item"]["question"],
                            "answer": r["answer"]["answer"],
                            "citations": r["answer"]["citations"],
                            "refused": r["answer"]["refused"],
                            "served_model": r["answer"].get("served_model"),
                            "cite_check": r["answer"].get("cite_check"),
                            "key_facts": r["key_facts"],
                            "citation_recall": r["citation_recall"],
                            "judge": r["judge"],
                        },
                        ensure_ascii=False,
                    )
                    + "\n"
                )
    print(f"zapisano {out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
