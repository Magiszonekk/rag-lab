"""Normalizacja tekstu dla BM25 (koncept D4): tokenizacja, lematyzacja, stop-words.

Jedna funkcja `Normalizer.normalize()` używana i przy indeksowaniu, i przy pytaniu. Wersja lematyzatora
trafia do metadanych indeksu (`Normalizer.signature`) — niezgodność przy ładowaniu indeksu = błąd.
"""

from __future__ import annotations

import re
from functools import lru_cache
from typing import ClassVar, Protocol

_TOKEN = re.compile(r"[0-9]+(?:[.,][0-9]+)*|[^\W\d_]+(?:-[^\W\d_]+)*", re.UNICODE)

# Krótka lista słów funkcyjnych; celowo bez „nie” (zmienia sens przepisów) i bez liczebników.
STOPWORDS = frozenset(
    [
        "a",
        "aby",
        "albo",
        "ale",
        "ani",
        "bo",
        "by",
        "być",
        "być",
        "czy",
        "dla",
        "do",
        "gdy",
        "i",
        "ich",
        "ile",
        "im",
        "jak",
        "jako",
        "je",
        "jego",
        "jej",
        "jest",
        "jeżeli",
        "jeśli",
        "już",
        "lub",
        "ma",
        "mowa",
        "na",
        "nad",
        "o",
        "od",
        "oraz",
        "po",
        "pod",
        "przez",
        "przy",
        "się",
        "są",
        "ta",
        "tak",
        "te",
        "tego",
        "tej",
        "tej",
        "ten",
        "to",
        "tych",
        "tym",
        "u",
        "w",
        "we",
        "z",
        "za",
        "ze",
        "że",
        "który",
        "która",
        "które",
        "którego",
        "której",
        "których",
        "którym",
        "których",
        "także",
        "również",
        "zm",
        "poz",
        "dz",
        "u",
    ]
)


def tokenize(text: str) -> list[str]:
    return [t.lower() for t in _TOKEN.findall(text)]


class Lemmatizer(Protocol):
    name: str
    version: str

    def lemma(self, word: str) -> str: ...

    def lemmas(self, words: list[str]) -> list[str]: ...


class MorfeuszLemmatizer:
    """Morfeusz 2 (słownik SGJP): dla każdej formy bierze lemat pierwszej interpretacji.

    Bez ujednoznacznienia kontekstowego — w BM25 liczy się spójność (ta sama forma → ten sam lemat),
    a nie poprawność gramatyczna w danym zdaniu.
    """

    name = "morfeusz2"
    # Kolejność interpretacji: rzeczownik przed formą odczasownikową („zwolnienia” → „zwolnienie”, nie „zwolnić”),
    # przymiotnik przed rzeczownikiem z przymiotnika („trwałych” → „trwały”, nie „trwała”). Imiesłowy
    # (ppas/pact) zostają przy czasowniku — w ustawach „naliczony podatek” i „naliczyć podatek” to ta sama sprawa.
    POS_RANK: ClassVar[dict[str, int]] = {
        "subst": 0,
        "depr": 0,
        "adj": 1,
        "adja": 1,
        "adv": 2,
        "ppas": 3,
        "pact": 3,
        "ger": 4,
    }
    # Wieloznaczności, przy których SGJP podaje kilka lematów rzeczownikowych (zmierzone na korpusie).
    PREFER: ClassVar[dict[str, str]] = {
        "przychod": "przychód",
        "stawek": "stawka",
        "odsetek": "odsetki",
        "odsetka": "odsetki",
        "trwała": "trwały",
        "płatnica": "płatnik",
    }

    def __init__(self, surface_freq: dict[str, int] | None = None) -> None:
        import morfeusz2

        self._m = morfeusz2.Morfeusz(generate=False, expand_tags=False)
        self.version = f"morfeusz2-{morfeusz2.__version__}"
        self._cache: dict[str, str] = {}
        # Remis między lematami tej samej klasy rozstrzyga „poparcie” lematu w korpusie: ile tokenów
        # dopuszcza go jako interpretację („umów” → „umowa”, nie „um”; „środków” → „środek”, nie „środki”).
        # Reguła ogólna zamiast listy wyjątków; liczona raz z częstości form.
        self._support: dict[str, int] = {}
        for form, n in (surface_freq or {}).items():
            for _rank, base in self._candidates(form):
                self._support[base] = self._support.get(base, 0) + n

    def _candidates(self, w: str) -> list[tuple[int, str]]:
        cands: list[tuple[int, str]] = []
        for _s, _e, (_orth, lem, tag, _cls, _qual) in self._m.analyse(w):
            if tag == "ign":
                continue
            base = lem.split(":", 1)[0].lower()  # „podatnik:Sm1” → „podatnik”
            base = self.PREFER.get(base, base)
            cands.append((self.POS_RANK.get(tag.split(":", 1)[0], 5), base))
        return cands

    def lemma(self, word: str) -> str:
        w = word.lower()
        if w in self._cache:
            return self._cache[w]
        lemma = w
        cands = self._candidates(w)
        if cands:
            best = min(rank for rank, _ in cands)
            top = sorted({b for rank, b in cands if rank == best}, key=lambda b: (-self._support.get(b, 0), b))
            lemma = top[0]
        self._cache[w] = lemma
        return lemma

    def lemmas(self, words: list[str]) -> list[str]:
        return [self.lemma(w) for w in words]


class SpacyLemmatizer:
    """spaCy pl_core_news_md — lematyzacja kontekstowa (wolniejsza)."""

    name = "spacy"

    def __init__(self, model: str = "pl_core_news_md") -> None:
        import spacy

        self._nlp = spacy.load(model, disable=["parser", "ner"])
        self.version = f"spacy-{spacy.about.__version__}/{model}-{self._nlp.meta.get('version')}"

    def lemma(self, word: str) -> str:
        return str(self._nlp(word.lower())[0].lemma_.lower())

    def lemmas(self, words: list[str]) -> list[str]:
        doc = self._nlp(" ".join(words))
        return [t.lemma_.lower() for t in doc]


class IdentityLemmatizer:
    """Bez lematyzacji — wiersz porównawczy „simple” (D4)."""

    name = "none"
    version = "none"

    def lemma(self, word: str) -> str:
        return word.lower()

    def lemmas(self, words: list[str]) -> list[str]:
        return [w.lower() for w in words]


class Normalizer:
    def __init__(self, lemmatizer: Lemmatizer, *, stopwords: frozenset[str] = STOPWORDS) -> None:
        self.lemmatizer = lemmatizer
        self.stopwords = stopwords

    @property
    def signature(self) -> str:
        return f"{self.lemmatizer.version}|stop={len(self.stopwords)}"

    def normalize(self, text: str) -> list[str]:
        words = [w for w in tokenize(text) if w not in self.stopwords]
        return [lem for lem in self.lemmatizer.lemmas(words) if lem not in self.stopwords]


def corpus_surface_freq() -> dict[str, int]:
    from collections import Counter

    from raglab.corpus import iter_units, load_corpus

    c: Counter[str] = Counter()
    for act in load_corpus().values():
        for loc in iter_units(act):
            c.update(tokenize(loc.unit.text + " " + loc.unit.tail))
    return dict(c)


@lru_cache(maxsize=4)
def get_normalizer(kind: str) -> Normalizer:
    if kind == "morfeusz2":
        return Normalizer(MorfeuszLemmatizer(corpus_surface_freq()))
    if kind == "spacy":
        return Normalizer(SpacyLemmatizer())
    if kind == "none":
        return Normalizer(IdentityLemmatizer())
    raise ValueError(kind)
