"""Klient LLM zgodny z OpenAI (self-hosted OpenAI-compatible gateway — koncept D11).

Konfiguracja wyłącznie z `.env` / zmiennych środowiska; adres i klucz nigdy nie trafiają do logów ani wyników.
Zwraca też model, który FAKTYCZNIE odpowiedział (proxy potrafi podmienić model — zapisujemy oba).
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from pathlib import Path

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
                d = r.json()
                text = (d["choices"][0]["message"].get("content") or "").strip()
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


def parse_json(text: str) -> object:
    """JSON z odpowiedzi modelu, także owinięty w ```json …```."""
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1].rsplit("```", 1)[0]
    return json.loads(t)
