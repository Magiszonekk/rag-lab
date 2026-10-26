"""Publiczne API demo (koncept sekcja 6–7, D9–D11).

Zabezpieczenia (warstwa aplikacji — druga po budżecie bramki modeli):
- gotowe przykłady bez wywołań modelu (`/examples`);
- pytania na żywo tylko gdy LIVE_ENABLED=1 i skonfigurowana bramka demo (LLM_DEMO_*), inaczej 503 + przykłady;
- limit pytań na IP (okno godzinowe) i dzienny limit dla całego demo; cache odpowiedzi (to samo pytanie → bez
  wywołania); limit długości pytania; prosty filtr pytań niezwiązanych z podatkami;
- CORS tylko dla domeny frontendu (RAGLAB_CORS_ORIGINS);
- żadnych adresów bramki/proxy w odpowiedziach i śladach.

Uruchomienie lokalne:  uv run uvicorn raglab.api:app --host 127.0.0.1 --port 3026
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import threading
import time
from collections import defaultdict, deque
from datetime import date
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from raglab import traces
from raglab.ingest.sources import REPO_ROOT
from raglab.llm import LLM, load_env

load_env()

EXAMPLES = REPO_ROOT / "web" / "public" / "examples.json"
RESULTS = REPO_ROOT / "results"
VARIANTS = ("simple", "hybrid", "hyde", "agentic-strict")
MAX_QUESTION = 600
PER_IP_HOUR = int(os.environ.get("RAGLAB_PER_IP_HOUR", "10"))
PER_DAY = int(os.environ.get("RAGLAB_PER_DAY", "200"))
LIVE = os.environ.get("RAGLAB_LIVE_ENABLED", "0") == "1"
TAX_HINTS = (
    "podat", "vat", "pit", "ordynac", "faktur", "zwolni", "odlicz", "stawk", "zeznan", "deklarac", "ulg",
    "przychód", "przychod", "dochód", "dochod", "urząd skarb", "urzad skarb", "skarbów", "skarbow", "us ",
    "odsetk", "zaległ", "zaleg", "nadpłat", "nadplat", "przedawn", "kasa fiskal", "ksef", "jpk", "ryczał",
    "liniow", "skala", "amortyz", "koszt", "działalno", "dzialalno", "firm", "alimen", "spadk", "darowiz",
    "sprzeda", "najem", "wynajem", "leasing", "samoch", "mieszkan", "nieruchom", "zwrot", "korekt", "kontrol",
    "pełnomoc", "pelnomoc", "interpretac", "akcyz", "cło", "clo", "zus",
)  # fmt: skip

# baza niedostępna — API działa dalej (przykłady, wyniki), ślady tylko w logu
with contextlib.suppress(Exception):
    traces.migrate()

app = FastAPI(title="RAG Lab API", version="0.1", docs_url=None, redoc_url=None, openapi_url=None)
origins = [o.strip() for o in os.environ.get("RAGLAB_CORS_ORIGINS", "http://localhost:5173").split(",") if o.strip()]
app.add_middleware(CORSMiddleware, allow_origins=origins, allow_methods=["GET", "POST"], allow_headers=["content-type"])

_lock = threading.Lock()
_ip_hits: dict[str, deque[float]] = defaultdict(deque)
_day: dict[str, Any] = {"date": str(date.today()), "count": 0}
_cache: dict[str, dict[str, Any]] = {}


def _client_ip(req: Request) -> str:
    # za nginx na OVH: X-Real-IP ustawia nasz vhost (proxy_set_header X-Real-IP $remote_addr)
    return req.headers.get("x-real-ip") or (req.client.host if req.client else "?")


def _check_limits(ip: str) -> None:
    now = time.time()
    with _lock:
        if _day["date"] != str(date.today()):
            _day.update(date=str(date.today()), count=0)
        if _day["count"] >= PER_DAY:
            raise HTTPException(429, "Dzienny limit pytań na żywo w demo wyczerpany — zobacz gotowe przykłady.")
        q = _ip_hits[ip]
        while q and now - q[0] > 3600:
            q.popleft()
        if len(q) >= PER_IP_HOUR:
            raise HTTPException(429, "Limit pytań na godzinę z tego adresu — zobacz gotowe przykłady.")
        q.append(now)
        _day["count"] += 1


def looks_like_tax(q: str) -> bool:
    s = q.lower()
    return any(h in s for h in TAX_HINTS)


class AskIn(BaseModel):
    question: str = Field(min_length=5, max_length=MAX_QUESTION)
    variant: str = "agentic-strict"
    verify: str = "llm"


def _demo_llm() -> LLM:
    # bramka demo (D11): osobny endpoint i klucz z listą modeli tylko z kluczy API; nigdy klucz ewaluacji
    base, key, model = (os.environ.get(k) for k in ("LLM_DEMO_BASE_URL", "LLM_DEMO_API_KEY", "LLM_DEMO_MODEL"))
    if not (base and key and model):
        raise HTTPException(503, "Pytania na żywo są chwilowo wyłączone — zobacz gotowe przykłady.")
    llm = LLM([model], timeout=90.0)
    llm.base, llm._key = base.rstrip("/"), key
    return llm


def _answer(question: str, variant: str, verify: str, llm: LLM) -> dict[str, Any]:
    from raglab.llm import use_system_llm

    token = use_system_llm(llm)  # HyDE, agent, weryfikacja — wszystko przez bramkę demo
    try:
        return _answer_inner(question, variant, verify, llm)
    finally:
        from raglab.llm import _system_llm

        _system_llm.reset(token)


def _answer_inner(question: str, variant: str, verify: str, llm: LLM) -> dict[str, Any]:
    from raglab.rag.evaluate import apply_verify

    if variant.startswith("agentic"):
        from raglab.rag.agentic import run

        a = run(question, llm, strict=True).to_json()
    else:
        from raglab.rag.variants import answer

        a = answer(question, variant, llm).to_json()
    if verify == "llm" and not a.get("error"):
        from raglab.rag.verify_llm import apply_llm

        checked = apply_llm(a, question)
        # weryfikacja zawiodła (pusta odpowiedź / limit modelu) → odpowiedź oznaczona jako niesprawdzona,
        # zamiast „model niedostępny” przy gotowej odpowiedzi
        unchecked = {**a, "llm_check": {"verdict": "unchecked", "unsupported": []}}
        a = unchecked if checked.get("error") else checked
    elif verify == "cite":
        a = apply_verify(a, "cite", question)
    return a


def _public(a: dict[str, Any], trace_id: str) -> dict[str, Any]:
    return {
        "trace_id": trace_id,
        "answer": a.get("answer"),
        "citations": a.get("citations", []),
        "refused": a.get("refused", False),
        "context": [
            {"address": c["address"], "status": c.get("status"), "note": c.get("note"), "text": c["text"]}
            for c in a.get("context", [])
        ],
        "steps": traces.steps_from_answer(a),
        "model": a.get("served_model"),
        "tokens": (a.get("prompt_tokens") or 0) + (a.get("completion_tokens") or 0),
        "latency_ms": sum((a.get("latency_ms") or {}).values()),
        "verify": a.get("llm_check"),
        "error": "Model chwilowo niedostępny — spróbuj później." if a.get("error") else None,
    }


@app.get("/health")
def health() -> dict[str, Any]:
    return {"ok": True, "live": LIVE and bool(os.environ.get("LLM_DEMO_API_KEY"))}


@app.get("/examples")
def examples() -> Any:
    if not EXAMPLES.exists():
        raise HTTPException(404, "brak przykładów")
    return json.loads(EXAMPLES.read_text(encoding="utf-8"))


@app.get("/eval/results")
def eval_results() -> dict[str, Any]:
    out: dict[str, Any] = {}
    for name in ("answers_golden_v1.json", "retrieval_v1.json", "retrieval_v1_rewrite.json"):
        p = RESULTS / name
        if p.exists():
            d = json.loads(p.read_text(encoding="utf-8"))
            out[name.removesuffix(".json")] = {k: d[k] for k in ("date", "testset", "n", "configs") if k in d}
    return out


@app.get("/corpus")
def corpus() -> list[dict[str, Any]]:
    from raglab.corpus import ACT_LABEL, load_corpus

    watch: dict[str, Any] = {}
    wp = RESULTS / "law_watch.json"
    if wp.exists():
        watch = json.loads(wp.read_text(encoding="utf-8")).get("acts", {})
    out = []
    for k, a in load_corpus().items():
        w = watch.get(k, {})
        later = [c for c in w.get("changes_after_corpus", []) if c.get("already_in_force")]
        changes = [{"eli": c["eli"], "in_force_from": c["in_force_from"]} for c in later]
        row = {"act": ACT_LABEL.get(k, k), "title": a.title, "state_date": str(a.state_date)}
        out.append({**row, "articles": len(a.articles), "later_changes_in_force": len(later), "later_changes": changes})
    return out


@app.get("/trace/{trace_id}")
def trace(trace_id: str) -> dict[str, Any]:
    if not trace_id.isalnum() or len(trace_id) > 32:
        raise HTTPException(400, "zły identyfikator")
    t = traces.load(trace_id)
    if t is None:
        raise HTTPException(404, "nie ma takiego śladu")
    return t


def _live_answer(q: str, variant: str, verify: str, llm: LLM) -> dict[str, Any]:
    key = hashlib.sha1(f"{variant}|{verify}|{q.lower()}".encode()).hexdigest()
    if key in _cache:
        return {**_cache[key], "cached": True}
    a = _answer(q, variant, verify, llm)
    tid = traces.new_id()
    traces.save(tid, "live", variant, verify, a)
    out = _public(a, tid)
    if not a.get("error"):
        _cache[key] = out
    return out


def _off_topic() -> dict[str, Any]:
    return {"trace_id": None, "answer": "Odpowiadam tylko na pytania o polskie prawo podatkowe (VAT, PIT, Ordynacja "
            "podatkowa).", "refused": True, "citations": [], "context": [], "steps": []}  # fmt: skip


def _precheck(question: str, verify: str, req: Request, cost: int) -> tuple[str, LLM | None]:
    if verify not in ("off", "cite", "llm"):
        raise HTTPException(400, "nieznany poziom verify")
    if not LIVE:
        raise HTTPException(503, "Pytania na żywo są chwilowo wyłączone — zobacz gotowe przykłady.")
    q = " ".join(question.split())
    if not looks_like_tax(q):
        return q, None
    for _ in range(cost):
        _check_limits(_client_ip(req))
    return q, _demo_llm()


@app.post("/ask")
def ask(body: AskIn, req: Request) -> dict[str, Any]:
    if body.variant not in VARIANTS:
        raise HTTPException(400, "nieznany wariant albo poziom verify")
    q, llm = _precheck(body.question, body.verify, req, 1)
    return _off_topic() if llm is None else _live_answer(q, body.variant, body.verify, llm)


class CompareIn(BaseModel):
    question: str = Field(min_length=5, max_length=MAX_QUESTION)
    verify: str = "llm"


@app.post("/compare")
def compare(body: CompareIn, req: Request) -> dict[str, Any]:
    # 4 odpowiedzi = 4 pytania w limicie, sprawdzane z góry; warianty równolegle (agent ~20–30 s)
    from concurrent.futures import ThreadPoolExecutor

    q, llm = _precheck(body.question, body.verify, req, len(VARIANTS))
    if llm is None:
        return {v: _off_topic() for v in VARIANTS}
    demo = llm
    with ThreadPoolExecutor(len(VARIANTS)) as ex:
        return dict(zip(VARIANTS, ex.map(lambda v: _live_answer(q, v, body.verify, demo), VARIANTS), strict=True))
