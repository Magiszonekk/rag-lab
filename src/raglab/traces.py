"""Ślady zapytań (koncept D9): zapis do Postgresa, odczyt dla /trace/<id>, maskowanie danych osobowych.

Zapis jest „best effort”: brak bazy nie może zatrzymać odpowiedzi (demo ma działać dalej, ślad trafia do logu).
W śladach nie ma adresów ani endpointów bramki modeli — tylko nazwa modelu, który odpowiedział.
"""

from __future__ import annotations

import json
import logging
import os
import re
import uuid
from typing import Any

from raglab.llm import load_env

log = logging.getLogger("raglab.traces")

_PATTERNS = [
    (re.compile(r"\b\d{11}\b"), "[PESEL]"),
    (re.compile(r"\b\d{3}[- ]?\d{3}[- ]?\d{2}[- ]?\d{2}\b"), "[NIP]"),
    (re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b"), "[EMAIL]"),
    (re.compile(r"(?<!\d)(?:\+48[ -]?)?\d{3}[ -]?\d{3}[ -]?\d{3}(?!\d)"), "[TELEFON]"),
]


def mask(text: str) -> str:
    for rx, repl in _PATTERNS:
        text = rx.sub(repl, text)
    return text


def new_id() -> str:
    return uuid.uuid4().hex[:12]


def _dsn() -> str:
    load_env()
    return (
        f"host=127.0.0.1 port={os.environ.get('RAGLAB_DB_PORT', '5436')} "
        f"dbname={os.environ.get('POSTGRES_DB', 'raglab')} user={os.environ.get('POSTGRES_USER', 'raglab')} "
        f"password={os.environ.get('POSTGRES_PASSWORD', '')} connect_timeout=3"
    )


def steps_from_answer(a: dict[str, Any]) -> list[dict[str, Any]]:
    """Kroki śladu z obiektu odpowiedzi (Answer.to_json + ewentualny wynik verify)."""
    steps: list[dict[str, Any]] = []
    for e in a.get("trace") or []:
        steps.append({"kind": e.get("step", "agent"), "attrs": e})
    if not a.get("trace"):
        steps.append({"kind": "retrieve", "attrs": {"retrieved": a.get("retrieved", [])}})
    steps.append({"kind": "context", "attrs": {"blocks": [
        {"address": c["address"], "status": c.get("status"), "note": c.get("note"), "chars": len(c.get("text", ""))}
        for c in a.get("context", [])]}})  # fmt: skip
    steps.append({"kind": "generate", "attrs": {"model": a.get("served_model"), "prompt_tokens": a.get("prompt_tokens"),
                                                "completion_tokens": a.get("completion_tokens"),
                                                "latency_ms": a.get("latency_ms")}})  # fmt: skip
    if a.get("llm_check"):
        steps.append({"kind": "verify", "attrs": {**a["llm_check"], "fixed": a.get("verify_fixed", False),
                                                  "blocked": a.get("verify_blocked", False)}})  # fmt: skip
    return steps


def migrate() -> None:
    """Idempotentne założenie tabel (db/init/*.sql uruchamia się tylko przy pierwszym starcie kontenera)."""
    import psycopg

    from raglab.ingest.sources import REPO_ROOT

    sql = (REPO_ROOT / "db" / "init" / "002_traces.sql").read_text(encoding="utf-8")
    with psycopg.connect(_dsn()) as conn:
        conn.execute(sql)


def save(trace_id: str, source: str, variant: str, verify: str, a: dict[str, Any]) -> bool:
    try:
        import psycopg

        with psycopg.connect(_dsn()) as conn, conn.cursor() as cur:
            cur.execute(
                """INSERT INTO traces (id, source, variant, verify, question, answer, refused, citations, model,
                   served_model, prompt_tokens, completion_tokens, latency_ms, error)
                   VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT (id) DO NOTHING""",
                (trace_id, source, variant, verify, mask(a.get("question", "")), a.get("answer"), a.get("refused"),
                 json.dumps(a.get("citations", []), ensure_ascii=False), a.get("model"), a.get("served_model"),
                 a.get("prompt_tokens"), a.get("completion_tokens"), json.dumps(a.get("latency_ms", {})),
                 a.get("error")),
            )  # fmt: skip
            for i, s in enumerate(steps_from_answer(a)):
                cur.execute(
                    "INSERT INTO trace_steps (trace_id, seq, kind, attrs) VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING",
                    (trace_id, i, s["kind"], json.dumps(s["attrs"], ensure_ascii=False, default=str)),
                )
        return True
    except Exception as e:  # ślad nie może zatrzymać odpowiedzi
        log.warning("nie zapisano śladu %s: %s", trace_id, type(e).__name__)
        return False


def load(trace_id: str) -> dict[str, Any] | None:
    try:
        import psycopg
        from psycopg.rows import dict_row

        with psycopg.connect(_dsn(), row_factory=dict_row) as conn, conn.cursor() as cur:
            cur.execute("SELECT * FROM traces WHERE id = %s", (trace_id,))
            t = cur.fetchone()
            if not t:
                return None
            cur.execute("SELECT seq, kind, attrs FROM trace_steps WHERE trace_id = %s ORDER BY seq", (trace_id,))
            t["steps"] = cur.fetchall()
            t["created_at"] = str(t["created_at"])
            return dict(t)
    except Exception as e:
        log.warning("nie odczytano śladu %s: %s", trace_id, type(e).__name__)
        return None
