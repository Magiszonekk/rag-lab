"""Klient LLM zgodny z OpenAI (self-hosted OpenAI-compatible gateway — koncept D11).

Konfiguracja wyłącznie z `.env` / zmiennych środowiska; adres i klucz nigdy nie trafiają do logów ani wyników.
Zwraca też model, który FAKTYCZNIE odpowiedział (proxy potrafi podmienić model — zapisujemy oba).
"""

from __future__ import annotations

import contextvars
import json
import os
import time
from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import httpx

from raglab.ingest.sources import REPO_ROOT

RETRYABLE = {429, 500, 502, 503, 504}


def load_env(path: Path = REPO_ROOT / ".env") -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())


@dataclass
class Completion:
    text: str
    requested_model: str
    served_model: str
    prompt_tokens: int
    completion_tokens: int
    latency_ms: int


class LLMError(RuntimeError):
    pass


# Model dla WSZYSTKICH kroków systemu (HyDE, odpowiedź, agent, weryfikacja) w bieżącym kontekście.
# API demo ustawia tu klienta bramki demo (D11) — bez tego kroki pomocnicze wołałyby domyślne modele ról
# (klucz ewaluacji, modele z subskrypcji). Ewaluacja zostawia None.
_system_llm: contextvars.ContextVar[LLM | None] = contextvars.ContextVar("raglab_system_llm", default=None)


# Strumień dla demo: callback dostaje SKUMULOWANY surowy tekst odpowiedzi końcowej (po ponowieniu zaczyna od nowa,
# więc odbiorca po prostu podmienia tekst) oraz zdarzenia postępu (kontekst, kroki agenta, weryfikacja).
# Ewaluacja zostawia None — wtedy zwykłe zapytania bez streamingu, wyniki bez zmian.
_progress: contextvars.ContextVar[Callable[[str, dict[str, Any]], None] | None] = contextvars.ContextVar(
    "raglab_progress", default=None
)


def progress(kind: str, **data: Any) -> None:
    cb = _progress.get()
    if cb is not None:
        cb(kind, data)


def use_progress(cb: Callable[[str, dict[str, Any]], None] | None) -> contextvars.Token[Any]:
    return _progress.set(cb)


def answer_stream() -> Callable[[str], None] | None:
    """Callback strumienia tekstu odpowiedzi końcowej (tylko gdy ktoś słucha postępu)."""
    cb = _progress.get()
    if cb is None:
        return None
    return lambda raw: cb("answer_raw", {"raw": raw})


def system_llm() -> LLM | None:
    return _system_llm.get()


def use_system_llm(llm: LLM | None) -> contextvars.Token[LLM | None]:
    return _system_llm.set(llm)


class LLM:
    def __init__(self, models: list[str], *, timeout: float = 120.0, attempts: int = 3, backoff: float = 1.0) -> None:
        load_env()
        self.base = os.environ["LLM_BASE_URL"].rstrip("/")
        self._key = os.environ["LLM_API_KEY"]
        self.models = models
        self.client = httpx.Client(timeout=timeout)
        # darmowe modele: chwilowe 429 (limit na minutę) — więcej prób i dłuższe czekanie (backoff * 2**próba)
        self.attempts = attempts
        self.backoff = backoff

    def complete(
        self,
        messages: list[dict[str, str]],
        *,
        max_tokens: int = 1500,
        temperature: float = 0.7,
        json_mode: bool = False,
        on_text: Callable[[str], None] | None = None,
    ) -> Completion:
        last_err = ""
        for model in self.models:
            for attempt in range(self.attempts):
                body: dict[str, object] = {
                    "model": model,
                    "messages": messages,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                }
                if json_mode:
                    body["response_format"] = {"type": "json_object"}
                t0 = time.monotonic()
                if on_text is not None:
                    try:
                        return self._stream(body, model, on_text, t0)
                    except _Retry as e:
                        last_err = f"{model}: {e}"
                        if "cooldown" in str(e):
                            break
                        time.sleep(self.backoff * 2**attempt)
                        continue
                    except _Fatal as e:
                        last_err = f"{model}: {e}"
                        break
                try:
                    r = self.client.post(
                        f"{self.base}/chat/completions",
                        headers={"Authorization": f"Bearer {self._key}"},
                        json=body,
                    )
                except httpx.HTTPError as e:
                    last_err = f"{model}: {type(e).__name__}"
                    time.sleep(self.backoff * 2**attempt)
                    continue
                if r.status_code in RETRYABLE:
                    last_err = f"{model}: HTTP {r.status_code}"
                    if "cooldown" in r.text:
                        break  # cooldown trwa godzinami — od razu następny model
                    time.sleep(self.backoff * 2**attempt)
                    continue
                if r.status_code != 200:
                    last_err = f"{model}: HTTP {r.status_code} {r.text[:120]}"
                    break
                try:
                    d = r.json()
                    text = (d["choices"][0]["message"].get("content") or "").strip()
                except (ValueError, KeyError, IndexError, TypeError):
                    # HTTP 200 z błędem w treści (darmowe modele przez OpenRouter: {"error": {...}}) — jak 429
                    last_err = f"{model}: HTTP 200 bez choices: {r.text[:120]}"
                    time.sleep(self.backoff * 2**attempt)
                    continue
                if not text:
                    last_err = f"{model}: pusta odpowiedź"
                    break
                u = d.get("usage") or {}
                return Completion(
                    text=text,
                    requested_model=model,
                    served_model=str(d.get("model", model)),
                    prompt_tokens=int(u.get("prompt_tokens", 0)),
                    completion_tokens=int(u.get("completion_tokens", 0)),
                    latency_ms=int((time.monotonic() - t0) * 1000),
                )
        raise LLMError(f"żaden model nie odpowiedział; ostatni błąd: {last_err}")

    def _stream(self, body: dict[str, object], model: str, on_text: Callable[[str], None], t0: float) -> Completion:
        """Zapytanie ze `stream: true` (SSE). on_text dostaje skumulowany tekst; błąd przed końcem → ponowienie."""
        body = {**body, "stream": True, "stream_options": {"include_usage": True}}
        parts: list[str] = []
        served: str = model
        usage: dict[str, Any] = {}
        on_text("")  # ponowienie: odbiorca czyści poprzedni częściowy tekst
        try:
            with self.client.stream("POST", f"{self.base}/chat/completions",
                                    headers={"Authorization": f"Bearer {self._key}"}, json=body) as r:  # fmt: skip
                if r.status_code in RETRYABLE:
                    raise _Retry(f"HTTP {r.status_code} {r.read().decode(errors='replace')[:120]}")
                if r.status_code != 200:
                    raise _Fatal(f"HTTP {r.status_code} {r.read().decode(errors='replace')[:120]}")
                for line in r.iter_lines():
                    if not line.startswith("data:"):
                        continue
                    data = line[5:].strip()
                    if data == "[DONE]":
                        break
                    try:
                        d = json.loads(data)
                    except ValueError:
                        continue
                    if "error" in d and not d.get("choices"):
                        raise _Retry(f"błąd w strumieniu: {str(d['error'])[:120]}")
                    served = str(d.get("model") or served)
                    usage = d.get("usage") or usage
                    for ch in d.get("choices") or []:
                        piece = (ch.get("delta") or {}).get("content")
                        if piece:
                            parts.append(piece)
                            on_text("".join(parts))
        except httpx.HTTPError as e:
            raise _Retry(type(e).__name__) from e
        text = "".join(parts).strip()
        if not text:
            raise _Fatal("pusta odpowiedź")
        return Completion(text=text, requested_model=model, served_model=served,
                          prompt_tokens=int(usage.get("prompt_tokens", 0)),
                          completion_tokens=int(usage.get("completion_tokens", 0)),
                          latency_ms=int((time.monotonic() - t0) * 1000))  # fmt: skip


class _Retry(Exception):
    pass


class _Fatal(Exception):
    pass


def partial_answer(raw: str) -> str:
    """Wartość pola "answer" z NIEDOKOŃCZONEGO JSON-a odpowiedzi (do wyświetlania na bieżąco).

    Model zwraca {"answer": "...", "citations": [...], ...}; dekoduje znaki do pierwszego niezamkniętego
    cudzysłowu, z sekwencjami ucieczki. Niedokończona sekwencja na końcu jest pomijana do następnego kawałka.
    """
    i = raw.find('"answer"')
    if i < 0:
        return ""
    j = raw.find('"', raw.find(":", i + 8) + 1)
    if j < 0:
        return ""
    out: list[str] = []
    k = j + 1
    esc = {"n": "\n", "t": "\t", "r": "", '"': '"', "\\": "\\", "/": "/", "b": "", "f": ""}
    while k < len(raw):
        c = raw[k]
        if c == '"':
            break
        if c == "\\":
            if k + 1 >= len(raw):
                break
            n = raw[k + 1]
            if n == "u":
                if k + 6 > len(raw):
                    break
                if all(h in "0123456789abcdefABCDEF" for h in raw[k + 2 : k + 6]):
                    out.append(chr(int(raw[k + 2 : k + 6], 16)))
                k += 6
                continue
            out.append(esc.get(n, n))
            k += 2
            continue
        out.append(c)
        k += 1
    return "".join(out)


def parse_json(text: str) -> object:
    """JSON z odpowiedzi modelu, także owinięty w ```json …```."""
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(t)
