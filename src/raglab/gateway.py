"""Bramka LiteLLM (koncept D11): zakładanie kluczy wirtualnych i testy wymagane przed ruchem publicznym.

    uv run python -m raglab.gateway setup   # klucze rag-lab-demo i rag-lab-eval (zapis do .env, bez wypisywania)
    uv run python -m raglab.gateway test    # testy D11

Testy:
1. klucz demo dostaje odmowę dla modelu spoza swojej listy (eval-answer = Claude z subskrypcji);
2. klucz demo działa dla swojego modelu (demo-answer);
3. klucz z wyczerpanym budżetem jest odrzucany (osobny klucz testowy z budżetem 0.000001 USD);
4. limit RPM odrzuca nadmiarowe zapytania (osobny klucz testowy z rpm_limit=1).
Test limitu po stronie upstreamu (twardy limit na kluczu RAG Lab w bramce właściciela) robi właściciel.
"""

from __future__ import annotations

import argparse
import os
import sys
from typing import Any

import httpx

from raglab.ingest.sources import REPO_ROOT
from raglab.llm import load_env

ENV = REPO_ROOT / ".env"


def _base() -> str:
    load_env()
    # w klastrze (Helm) bramka to usługa, np. http://raglab-litellm:4000
    return os.environ.get("RAGLAB_LITELLM_URL") or f"http://127.0.0.1:{os.environ.get('RAGLAB_LITELLM_PORT', '3027')}"


def _admin() -> dict[str, str]:
    return {"Authorization": f"Bearer {os.environ['LITELLM_MASTER_KEY']}"}


def _gen(**body: Any) -> str:
    r = httpx.post(f"{_base()}/key/generate", headers=_admin(), json=body, timeout=30)
    r.raise_for_status()
    return str(r.json()["key"])


def _set_env(name: str, value: str) -> None:
    lines = ENV.read_text(encoding="utf-8").splitlines() if ENV.exists() else []
    lines = [x for x in lines if not x.startswith(name + "=")] + [f"{name}={value}"]
    ENV.write_text("\n".join(lines) + "\n", encoding="utf-8")
    ENV.chmod(0o600)


def setup() -> None:
    load_env()
    if os.environ.get("LLM_DEMO_API_KEY", "").startswith("sk-") and os.environ.get("LLM_EVAL_GATEWAY_KEY"):
        print("klucze już są w .env", file=sys.stderr)
        return
    demo = _gen(key_alias="rag-lab-demo", models=["demo-answer"], max_budget=float(os.environ.get(
        "RAGLAB_DEMO_BUDGET_USD", "5")), budget_duration="30d", rpm_limit=20, tpm_limit=200_000)  # fmt: skip
    ev = _gen(key_alias="rag-lab-eval", models=["eval-answer", "eval-judge"])
    _set_env("LLM_DEMO_BASE_URL", _base() + "/v1")
    _set_env("LLM_DEMO_API_KEY", demo)
    _set_env("LLM_DEMO_MODEL", "demo-answer")
    _set_env("LLM_EVAL_GATEWAY_KEY", ev)
    print("zapisano klucze rag-lab-demo i rag-lab-eval w .env (chmod 600)", file=sys.stderr)


def _chat(key: str, model: str) -> httpx.Response:
    return httpx.post(f"{_base()}/v1/chat/completions", headers={"Authorization": f"Bearer {key}"}, timeout=120,
                      json={"model": model, "messages": [{"role": "user", "content": "Odpowiedz jednym słowem: ok"}],
                            "max_tokens": 400})  # fmt: skip


def test() -> int:
    load_env()
    demo = os.environ["LLM_DEMO_API_KEY"]
    results: list[tuple[str, bool, object]] = []

    r = _chat(demo, "eval-answer")
    results.append(("demo → model spoza listy (Claude) odrzucony", r.status_code in (401, 403), r.status_code))
    r = _chat(demo, "demo-answer")
    results.append(("demo → demo-answer działa", r.status_code == 200, r.status_code))
    broke = _gen(key_alias="rag-lab-test-budget", models=["demo-answer"], max_budget=0.000001)
    _chat(broke, "demo-answer")  # pierwsze zapytanie zużywa budżet
    r = _chat(broke, "demo-answer")
    # LiteLLM: 422 {"type": "budget_exceeded"}; wymaga cen w model_info (bez nich koszt = 0 i budżet nie działa)
    results.append(("wyczerpany budżet odrzucony", r.status_code in (400, 401, 403, 422, 429) and "budget" in r.text,
                    r.status_code))  # fmt: skip
    slow = _gen(key_alias="rag-lab-test-rpm", models=["demo-answer"], rpm_limit=1)
    codes = [_chat(slow, "demo-answer").status_code for _ in range(3)]
    results.append(("limit RPM odrzuca nadmiar", 429 in codes, codes))
    # zapas: model główny pada → LiteLLM przechodzi na demo-answer-fallback-* (klucz nie ma do nich dostępu wprost)
    fbk = _gen(key_alias="rag-lab-test-fallback", models=["demo-broken-test"])
    r = _chat(fbk, "demo-broken-test")
    results.append(("padnięty model główny → zapas odpowiada", r.status_code == 200
                    and r.headers.get("x-litellm-attempted-fallbacks", "0") != "0", r.status_code))  # fmt: skip
    r = _chat(demo, "demo-answer-fallback-1")
    results.append(("demo → zapas wprost odrzucony", r.status_code in (401, 403), r.status_code))
    for k in (broke, slow, fbk):
        httpx.post(f"{_base()}/key/delete", headers=_admin(), json={"keys": [k]}, timeout=30)

    ok = True
    for name, passed, detail in results:
        ok &= passed
        print(f"{'OK ' if passed else 'BŁĄD'} {name} ({detail})", file=sys.stderr)
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="raglab.gateway")
    ap.add_argument("cmd", choices=["setup", "test"])
    a = ap.parse_args(argv)
    if a.cmd == "setup":
        setup()
        return 0
    return test()


if __name__ == "__main__":
    raise SystemExit(main())
