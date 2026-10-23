"""Sędzia LLM (koncept D7, warstwa 2): ocena odpowiedzi względem wzorca i przepisów.

Sędzia jest z INNEJ rodziny niż model odpowiadający (odpowiada GPT → ocenia Claude), z jawną skalą
i uzasadnieniem. Kalibracja z człowiekiem — `judge_calibration.md` (D7).
"""

from __future__ import annotations

from typing import Any

from raglab.llm import LLM, LLMError, parse_json

JUDGE_MODELS = ["claude-sonnet-5", "claude-opus-4-7"]

JUDGE_PROMPT = """Oceniasz odpowiedź systemu RAG na pytanie o polskie prawo podatkowe. System może korzystać
WYŁĄCZNIE z przepisów, które dostał w kontekście (VAT, PIT, Ordynacja podatkowa). Masz wzorcową odpowiedź
przygotowaną z tekstu ustawy i oczekiwane zachowanie.

Skala „verdict”:
- "correct": odpowiedź merytorycznie zgodna z wzorcem (może być krótsza lub inaczej sformułowana, ale nie
  pomija niczego, co zmienia sens, i nie zawiera błędów);
- "partial": główna teza zgodna, ale brakuje istotnego warunku / wyjątku albo jest drobny błąd;
- "incorrect": teza sprzeczna z wzorcem, zła liczba / termin / stawka, albo odmowa tam, gdzie odpowiedź była
  w przepisach;
- "refusal_ok": system odmówił (albo odpowiedział tylko na część) i to było oczekiwane zachowanie;
- "refusal_missing": system odpowiedział, choć powinien był odmówić (np. podał fakty spoza swoich ustaw).

„faithful”: true, jeśli każde twierdzenie odpowiedzi wynika z PRZEPISÓW W KONTEKŚCIE (nie z wiedzy ogólnej),
nawet jeśli odpowiedź jest niepełna. false, jeśli coś zostało dopowiedziane spoza kontekstu.

Odpowiedz wyłącznie JSON:
{{"verdict": "...", "faithful": true/false, "reason": "1–2 zdania, konkretnie co jest dobrze/źle"}}

PYTANIE: {question}

OCZEKIWANE ZACHOWANIE: {expected}

WZORCOWA ODPOWIEDŹ: {reference}

ODPOWIEDŹ SYSTEMU: {answer}
(odmowa: {refused}; cytaty: {citations})

PRZEPISY W KONTEKŚCIE SYSTEMU:
{context}"""

EXPECTED = {
    "answer": "odpowiedzieć na podstawie przepisów",
    "refuse": "odmówić — pytanie poza zakresem (temat niepodatkowy)",
    "refuse_with_pointer": "odmówić — odpowiedź jest w innej ustawie niż VAT/PIT/Ordynacja; dobrze, jeśli ją wskaże",
    "answer_with_date": "podać stan według daty korpusu z wyraźną datą i zaznaczyć, że o innym okresie nie wie",
    "provisions_without_verdict": "przytoczyć przepisy i wskazać, od czego zależy rozstrzygnięcie, bez rozstrzygania",
    "partial_answer": "odpowiedzieć na część pokrytą przepisami i wprost wskazać, czego brakuje",
}


def judge(item: dict[str, Any], ans: dict[str, Any], llm: LLM) -> dict[str, Any]:
    expected = EXPECTED.get(item.get("expected_behavior") or "answer", "odpowiedzieć na podstawie przepisów")
    ctx = "\n\n".join(f"[{c['address']}]\n{c['text'][:2500]}" for c in ans.get("context", []))
    prompt = JUDGE_PROMPT.format(
        question=item["question"],
        expected=expected,
        reference=item.get("reference_answer", ""),
        answer=ans.get("answer", ""),
        refused=ans.get("refused"),
        citations=", ".join(ans.get("citations", [])),
        context=ctx[:14000],
    )
    try:
        c = llm.complete([{"role": "user", "content": prompt}], max_tokens=1500, temperature=0.0)
        d = parse_json(c.text)
        if not isinstance(d, dict) or d.get("verdict") not in (
            "correct",
            "partial",
            "incorrect",
            "refusal_ok",
            "refusal_missing",
        ):
            raise ValueError(f"zły format: {c.text[:120]}")
        return {
            "verdict": d["verdict"],
            "faithful": bool(d.get("faithful")),
            "reason": str(d.get("reason", "")),
            "judge_model": c.served_model,
        }
    except (LLMError, ValueError) as e:
        return {"verdict": "error", "faithful": None, "reason": str(e)[:200], "judge_model": ""}
