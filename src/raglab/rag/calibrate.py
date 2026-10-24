"""Kalibracja sędziego LLM (koncept D7).

1. Drugi sędzia z innej rodziny modeli ocenia te same odpowiedzi (ten sam prompt, ten sam kontekst).
2. Zgodność: procent zgodnych werdyktów i kappa Cohena na werdyktach zredukowanych do 4 klas
   (ok / częściowa / błąd / odmowa słuszna).
3. Arkusz do przeglądu ręcznego: wszystkie werdykty sporne + losowa próbka zgodnych, z tekstem kontekstu.
   Przegląd ręczny zapisuje się w `data/eval/golden/judge_review_v1.jsonl` ({"config","id","verdict","note"}).
4. Raport: trafność obu sędziów względem przeglądu ręcznego.

    uv run python -m raglab.rag.calibrate run      # drugi sędzia + arkusz
    uv run python -m raglab.rag.calibrate report   # po przeglądzie ręcznym
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from typing import Any

from raglab.ingest.sources import REPO_ROOT
from raglab.llm import LLM
from raglab.rag.evaluate import GOLDEN, RUNS, _cache_key, apply_verify
from raglab.rag.judge import JUDGE_VERSION, judge

# gemini-3.8-flash przez bramkę ~70 s na odpowiedź (zmierzone) — niepraktyczne dla ~200 ocen.
SECOND_JUDGE = ["gemini-2.5-flash"]  # trzecia rodzina: ani Claude (odpowiada), ani Nemotron (sędzia 1)
CONFIGS = ["simple/verify=off", "hybrid/verify=off", "hyde/verify=off"]
DETAILS = REPO_ROOT / "results" / "answers_golden_v1.details.jsonl"
SECOND = RUNS / "judge2_cache.jsonl"
SHEET = REPO_ROOT / "data" / "eval" / "golden" / "judge_review_v1.SHEET.md"
REVIEW = REPO_ROOT / "data" / "eval" / "golden" / "judge_review_v1.jsonl"
OUT = REPO_ROOT / "results" / "judge_calibration_v1.json"

COLLAPSE = {"correct": "ok", "partial": "partial", "incorrect": "wrong", "refusal_missing": "wrong",
            "refusal_ok": "refusal_ok", "error": "error"}  # fmt: skip


def kappa(a: list[str], b: list[str]) -> float:
    n = len(a)
    po = sum(x == y for x, y in zip(a, b, strict=True)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[k] * cb[k] for k in set(a) | set(b)) / n**2
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def _rows() -> list[dict[str, Any]]:
    items = {json.loads(x)["id"]: json.loads(x) for x in GOLDEN.read_text(encoding="utf-8").splitlines() if x}
    cache = {}
    for line in (RUNS / "answer_cache.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        cache[r["key"]] = r["answer"]
    rows = []
    for line in DETAILS.read_text(encoding="utf-8").splitlines():
        d = json.loads(line)
        if d["config"] not in CONFIGS:
            continue
        it = items[d["id"]]
        variant, level = d["config"].split("/verify=")
        ans = apply_verify(cache[_cache_key(variant, it["question"])], level, it["question"])
        rows.append({"config": d["config"], "item": it, "answer": ans, "judge1": d["judge"]})
    return rows


def run() -> None:
    rows = _rows()
    done: dict[str, dict[str, Any]] = {}
    if SECOND.exists():
        for line in SECOND.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            done[r["key"]] = r["judge"]
    llm = LLM(SECOND_JUDGE, timeout=240.0, attempts=6, backoff=5.0)

    def key(r: dict[str, Any]) -> str:
        raw = json.dumps([JUDGE_VERSION, SECOND_JUDGE, r["item"]["id"], r["answer"]["answer"]], ensure_ascii=False)
        return hashlib.sha1(raw.encode()).hexdigest()

    todo = [r for r in rows if key(r) not in done]
    print(f"drugi sędzia: {len(todo)} ocen do wykonania", file=sys.stderr)
    with ThreadPoolExecutor(2) as ex, SECOND.open("a", encoding="utf-8") as f:
        for r, j in zip(todo, ex.map(lambda r: judge(r["item"], r["answer"], llm), todo), strict=True):
            if j["verdict"] != "error":
                done[key(r)] = j
                f.write(json.dumps({"key": key(r), "judge": j}, ensure_ascii=False) + "\n")
    for r in rows:
        r["judge2"] = done.get(key(r), {"verdict": "error", "faithful": None, "reason": "", "judge_model": ""})

    a = [COLLAPSE[r["judge1"]["verdict"]] for r in rows]
    b = [COLLAPSE[r["judge2"]["verdict"]] for r in rows]
    agree = sum(x == y for x, y in zip(a, b, strict=True))
    print(f"zgodność {agree}/{len(rows)} = {agree / len(rows):.3f}, kappa {kappa(a, b):.3f}", file=sys.stderr)
    print("macierz (sędzia1 → sędzia2):", Counter(zip(a, b, strict=True)).most_common(), file=sys.stderr)

    # arkusz: wszystkie spory + 15 losowych zgodnych
    rng = random.Random(1)
    disagree = [r for r, x, y in zip(rows, a, b, strict=True) if x != y]
    agreeing = [r for r, x, y in zip(rows, a, b, strict=True) if x == y]
    sample = disagree + rng.sample(agreeing, min(15, len(agreeing)))
    lines = [
        "# Przegląd ręczny werdyktów sędziego (golden v1)\n",
        f"Spory: {len(disagree)}, próbka zgodnych: {len(sample) - len(disagree)}.\n",
    ]
    for r in sample:
        it, ans = r["item"], r["answer"]
        lines += [
            f"\n## {r['config']} · {it['id']} ({it['category']}, "
            f"oczekiwane: {it.get('expected_behavior') or 'answer'})",
            f"**Pytanie:** {it['question']}",
            f"**Wzorzec:** {it.get('reference_answer', '')}",
            f"**Odpowiedź** (odmowa={ans['refused']}; cytaty: {', '.join(ans['citations'])}): {ans['answer']}",
            f"**Kontekst:** {', '.join(c['address'] for c in ans['context'])}",
            f"**Sędzia 1** ({r['judge1'].get('judge_model')}): {r['judge1']['verdict']} — {r['judge1']['reason']}",
            f"**Sędzia 2** ({r['judge2'].get('judge_model')}): {r['judge2']['verdict']} — {r['judge2']['reason']}",
        ]
    SHEET.write_text("\n".join(lines) + "\n", encoding="utf-8")
    json.dump([{"config": r["config"], "id": r["item"]["id"], "j1": r["judge1"]["verdict"],
                "j2": r["judge2"]["verdict"]} for r in rows],
              (RUNS / "calib_pairs.json").open("w"), ensure_ascii=False)  # fmt: skip
    print(f"arkusz: {SHEET} ({len(sample)} pozycji)", file=sys.stderr)


def report() -> None:
    pairs = {(p["config"], p["id"]): p for p in json.loads((RUNS / "calib_pairs.json").read_text())}
    rev = [json.loads(x) for x in REVIEW.read_text(encoding="utf-8").splitlines() if x.strip()]
    a = [COLLAPSE[p["j1"]] for p in pairs.values()]
    b = [COLLAPSE[p["j2"]] for p in pairs.values()]
    out: dict[str, Any] = {
        "n": len(pairs),
        "judge_agreement": round(sum(x == y for x, y in zip(a, b, strict=True)) / len(a), 3),
        "judge_kappa": round(kappa(a, b), 3),
        "reviewed": len(rev),
    }
    disputed = [
        r for r in rev if COLLAPSE[pairs[(r["config"], r["id"])]["j1"]] != COLLAPSE[pairs[(r["config"], r["id"])]["j2"]]
    ]
    agreed = [r for r in rev if r not in disputed]
    for name, subset in (("disputed", disputed), ("agreed_sample", agreed)):
        for j in ("j1", "j2"):
            ok = sum(COLLAPSE[pairs[(r["config"], r["id"])][j]] == COLLAPSE[r["verdict"]] for r in subset)
            out[f"{name}_{j}_matches_review"] = f"{ok}/{len(subset)}"
    # korekta wyników: o ile zmienia się „poprawne” per wariant, gdy werdykty sporne zastąpić przeglądem
    for cfg in CONFIGS:
        ids = [k for k in pairs if k[0] == cfg]
        fixed = {(r["config"], r["id"]): r["verdict"] for r in rev}
        items = {json.loads(x)["id"]: json.loads(x) for x in GOLDEN.read_text(encoding="utf-8").splitlines() if x}
        ans_ids = [k for k in ids if items[k[1]]["category"] != "out_of_corpus"]
        j1 = sum(pairs[k]["j1"] == "correct" for k in ans_ids) / len(ans_ids)
        adj = sum(fixed.get(k, pairs[k]["j1"]) == "correct" for k in ans_ids) / len(ans_ids)
        out[f"{cfg}_correct_judge1"] = round(j1, 3)
        out[f"{cfg}_correct_after_review"] = round(adj, 3)
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="raglab.rag.calibrate")
    ap.add_argument("cmd", choices=["run", "report"])
    args = ap.parse_args(argv)
    run() if args.cmd == "run" else report()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
