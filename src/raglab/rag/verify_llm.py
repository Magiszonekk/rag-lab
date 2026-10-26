"""Sprawdzanie odpowiedzi przez model, zdanie po zdaniu — poziom `verify=llm` (koncept D5).

Deterministyczne `verify=cite` blokowało poprawne odpowiedzi z liczbami wyliczonymi albo przytoczonymi innymi
słowami („2 × 92,67 = 185,34 zł”, „pięć lat”). Tu model weryfikujący dostaje odpowiedź i przepisy z kontekstu
i dla każdego twierdzenia ocenia, czy wynika z przepisów (także przez prosty rachunek albo parafrazę).

Wynik:
- `pass` — wszystkie twierdzenia mają oparcie → odpowiedź bez zmian;
- `fix`  — część twierdzeń bez oparcia → odpowiedź poprawiona: zdania bez oparcia usunięte (model nie dopisuje
           niczego nowego);
- `fail` — główna teza bez oparcia → odmowa.

Weryfikator to część systemu (nie sędzia), więc może być tym samym modelem co odpowiadający.
"""

from __future__ import annotations

import hashlib
import json
import threading
from typing import Any

from raglab.ingest.sources import REPO_ROOT
from raglab.llm import LLM, LLMError, parse_json, system_llm

VERIFY_MODELS = ["claude-opus-5-5"]
CACHE = REPO_ROOT / "results" / "answers" / "verify_cache.jsonl"
LLM_REFUSAL = "Nie mogę potwierdzić tej odpowiedzi w przepisach, które mam."

PROMPT = """Sprawdzasz odpowiedź systemu na pytanie o polskie prawo podatkowe. System mógł korzystać WYŁĄCZNIE
z przepisów podanych niżej. Rozbij odpowiedź na pojedyncze twierdzenia (fakty, liczby, terminy, warunki,
wskazania przepisów) i dla każdego oceń, czy wynika z podanych przepisów.

Twierdzenie MA oparcie, jeśli:
- wynika wprost z treści przepisu, także w innych słowach (parafraza, „pięć lat” = „5 lat”);
- jest prostym rachunkiem na liczbach z przepisów lub z pytania (np. 2 × 92,67 zł = 185,34 zł);
- jest liczbą lub faktem podanym przez użytkownika w pytaniu;
- stwierdza, że w przepisach czegoś brakuje albo że wynik zależy od faktów, których nie znamy.

Twierdzenie NIE MA oparcia, jeśli pochodzi z wiedzy ogólnej, z przepisu, którego nie ma niżej, albo przeczy
przepisom. Przepis zastępujący (przejściowy) ma pierwszeństwo przed zastępowanym — zgodnie z adnotacjami.

Odpowiedz wyłącznie JSON:
{{"claims": [{{"claim": "krótko", "supported": true/false, "source": "adres przepisu albo 'pytanie' albo null"}}],
 "verdict": "pass" | "fix" | "fail",
 "fixed_answer": "przy fix: odpowiedź z usuniętymi zdaniami bez oparcia — nie dopisuj nic nowego; inaczej null"}}

"fail" wybierz, gdy bez oparcia jest główna teza odpowiedzi (np. kluczowa liczba lub rozstrzygnięcie).

PYTANIE: {question}

ODPOWIEDŹ SYSTEMU: {answer}
(cytaty: {citations})

PRZEPISY:
{context}"""

_lock = threading.Lock()
_mem: dict[str, dict[str, Any]] | None = None


def _key(ans: dict[str, Any], question: str) -> str:
    raw = json.dumps([VERIFY_MODELS, PROMPT, question, ans["answer"]], ensure_ascii=False)
    return hashlib.sha1(raw.encode()).hexdigest()


def _load() -> dict[str, dict[str, Any]]:
    global _mem
    if _mem is None:
        _mem = {}
        if CACHE.exists():
            for line in CACHE.read_text(encoding="utf-8").splitlines():
                r = json.loads(line)
                _mem[r["key"]] = r["result"]
    return _mem


def verify_llm(ans: dict[str, Any], question: str, llm: LLM | None = None) -> dict[str, Any]:
    """{"verdict": pass|fix|fail|error, "claims": [...], "fixed_answer": str|None}. Błędy nie są cache'owane."""
    mem = _load()
    k = _key(ans, question)
    if k in mem:
        return mem[k]
    sys_llm = system_llm()
    llm = llm or sys_llm or LLM(VERIFY_MODELS)
    expected = llm.models[0] if sys_llm is not None and llm is sys_llm else VERIFY_MODELS[0]
    if sys_llm is not None:
        k = _key({**ans, "answer": ans["answer"] + "@" + sys_llm.models[0]}, question)
        if k in mem:
            return mem[k]
    ctx = "\n\n".join(f"[{c['address']}]" + (f" ({c['note']})" if c.get("note") else "") + f"\n{c['text']}"
                      for c in ans.get("context", []))  # fmt: skip
    prompt = PROMPT.format(question=question, answer=ans["answer"], citations=", ".join(ans["citations"]),
                           context=ctx[:40000])  # fmt: skip
    try:
        c = llm.complete([{"role": "user", "content": prompt}], max_tokens=8000, temperature=0.0)
        if c.served_model != expected:
            raise ValueError(f"odpowiedział inny model: {c.served_model}")
        d = parse_json(c.text)
        if not isinstance(d, dict) or d.get("verdict") not in ("pass", "fix", "fail"):
            raise ValueError(f"zły format: {c.text[:120]}")
        if d["verdict"] == "fix" and not str(d.get("fixed_answer") or "").strip():
            d["verdict"] = "fail"
        result = {"verdict": d["verdict"], "claims": d.get("claims") or [],
                  "fixed_answer": d.get("fixed_answer") if d["verdict"] == "fix" else None}  # fmt: skip
    except (LLMError, ValueError) as e:
        return {"verdict": "error", "claims": [], "fixed_answer": None, "error": str(e)[:200]}
    with _lock:
        mem[k] = result
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        with CACHE.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"key": k, "result": result}, ensure_ascii=False) + "\n")
    return result


def apply_llm(ans: dict[str, Any], question: str, llm: LLM | None = None) -> dict[str, Any]:
    if ans.get("refused") or ans.get("error"):
        return ans
    v = verify_llm(ans, question, llm)
    unsupported = [c.get("claim") for c in v["claims"] if not c.get("supported")]
    out = {**ans, "llm_check": {"verdict": v["verdict"], "unsupported": unsupported}}
    if v["verdict"] == "fix":
        return {**out, "answer": v["fixed_answer"], "verify_fixed": True}
    if v["verdict"] == "fail":
        return {**out, "answer": LLM_REFUSAL, "refused": True, "verify_blocked": True}
    if v["verdict"] == "error":
        return {**out, "error": "verify: " + v.get("error", "")}
    return out
