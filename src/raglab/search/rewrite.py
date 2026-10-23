"""Przepisywanie pytania na język ustawy przed wyszukiwaniem (etap 3, pytania potoczne).

Pytania potoczne („ile mogę odliczyć VAT od auta, którym jeżdżę też prywatnie”) przegrywają w wyszukiwaniu
z pytaniami w języku przepisów (hybryda R@5 0,79 vs 0,90). Model przepisuje pytanie na sformułowania,
jakich używa ustawa, a wyszukiwanie łączy wyniki dla pytania oryginalnego i przepisanego (RRF).

Dwie strategie:
- `rewrite` — pytanie przeformułowane na język ustawy + słowa kluczowe;
- `hyde`    — hipotetyczny fragment przepisu, który odpowiadałby na pytanie (Gao i in. 2022).

Model NIE dostaje numerów artykułów ani niczego z zestawów testowych; nie wolno mu podawać numerów
artykułów (wtedy mierzylibyśmy pamięć modelu, nie wyszukiwanie). Wyniki są cache'owane na dysku.
"""

from __future__ import annotations

import hashlib
import json
import re
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from raglab.ingest.sources import REPO_ROOT
from raglab.llm import LLM, LLMError, parse_json

REWRITE_MODELS = ["gpt-5.6-luna", "gpt-5.6-terra"]
CACHE = REPO_ROOT / "data" / "cache" / "rewrite.jsonl"

PROMPTS = {
    "rewrite": """Przepisz pytanie użytkownika o polskie prawo podatkowe (VAT, PIT, Ordynacja podatkowa) na język,
jakim posługuje się ustawa, żeby wyszukiwarka znalazła właściwy przepis.

- Zamień słowa potoczne na terminy ustawowe (np. „auto” → „samochód osobowy”, „firma” → „działalność
  gospodarcza”, „odpisać VAT” → „obniżyć kwotę podatku należnego o kwotę podatku naliczonego”,
  „skarbówka” → „naczelnik urzędu skarbowego”).
- Dodaj 3–8 słów kluczowych, które prawdopodobnie występują w szukanym przepisie.
- NIE podawaj numerów artykułów, stawek, kwot ani odpowiedzi — tylko przeformułuj pytanie.

Odpowiedz wyłącznie JSON: {{"query": "przeformułowane pytanie", "keywords": ["...", "..."]}}

Pytanie: {question}""",
    "hyde": """Napisz jeden krótki (2–4 zdania) fragment polskiej ustawy podatkowej (VAT, PIT albo Ordynacji
podatkowej), który mógłby odpowiadać na pytanie użytkownika — w stylu przepisu („Podatnik jest obowiązany…”,
„Zwalnia się od podatku…”). Nie musi być dosłowny. NIE podawaj numerów artykułów.

Odpowiedz wyłącznie JSON: {{"query": "tekst fragmentu"}}

Pytanie: {question}""",
}

_lock = threading.Lock()
_mem: dict[str, str] | None = None


def _key(strategy: str, question: str) -> str:
    return hashlib.sha1(f"{strategy}|{REWRITE_MODELS[0]}|{PROMPTS[strategy]}|{question}".encode()).hexdigest()[:16]


def _load() -> dict[str, str]:
    global _mem
    if _mem is None:
        _mem = {}
        if CACHE.exists():
            for line in CACHE.read_text(encoding="utf-8").splitlines():
                r = json.loads(line)
                _mem[r["key"]] = r["query"]
    return _mem


_RE_ARTNO = re.compile(r"\bart(?:ykuł\w*|\.)\s*\d+[a-z]*", re.I)


def _strip_article_numbers(s: str) -> str:
    return re.sub(r"\s+", " ", _RE_ARTNO.sub("", s)).strip()


def rewrite(question: str, strategy: str, llm: LLM | None = None) -> str:
    """Przepisane zapytanie (z cache albo z modelu). Przy błędzie modelu — pytanie oryginalne."""
    mem = _load()
    k = _key(strategy, question)
    if k in mem:
        return mem[k]
    llm = llm or LLM(REWRITE_MODELS)
    try:
        c = llm.complete(
            [{"role": "user", "content": PROMPTS[strategy].format(question=question)}],
            max_tokens=1200,
            temperature=0.0,
        )
        d = parse_json(c.text)
        if not isinstance(d, dict) or not d.get("query"):
            raise ValueError("brak pola query")
        q = str(d["query"])
        if d.get("keywords"):
            q += " " + " ".join(str(x) for x in d["keywords"])
        q = _strip_article_numbers(q)
    except (LLMError, ValueError):
        return question  # nie cache'ujemy błędu
    with _lock:
        mem[k] = q
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        with CACHE.open("a", encoding="utf-8") as f:
            f.write(
                json.dumps({"key": k, "strategy": strategy, "question": question, "query": q}, ensure_ascii=False)
                + "\n"
            )
    return q


def prefetch(questions: list[str], strategies: list[str], workers: int = 6) -> None:
    llm = LLM(REWRITE_MODELS)
    todo = [(q, s) for s in strategies for q in questions if _key(s, q) not in _load()]
    if not todo:
        return
    with ThreadPoolExecutor(workers) as ex:
        list(ex.map(lambda qs: rewrite(qs[0], qs[1], llm), todo))


__all__ = ["CACHE", "PROMPTS", "Path", "prefetch", "rewrite"]
