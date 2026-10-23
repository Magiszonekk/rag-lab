"""Model danych korpusu: akt → artykuł → ustęp → punkt → litera, plus załączniki i przypisy (koncept D2)."""

from __future__ import annotations

from datetime import date
from typing import Literal

from pydantic import BaseModel, Field

UnitKind = Literal["article", "paragraph", "point", "letter"]


class Unit(BaseModel):
    """Jednostka redakcyjna ustawy.

    `text` to treść własna (dla punktu z literami: zdanie wprowadzające),
    `tail` to „część wspólna” po wyliczeniu (np. „– jeżeli wywóz towarów …”).
    """

    kind: UnitKind
    number: str | None = None
    text: str = ""
    tail: str = ""
    children: list[Unit] = Field(default_factory=list)
    repealed: bool = False
    footnote_refs: list[int] = Field(default_factory=list)
    page: int
    # Tekst jednolity bywa „dwuwersyjny”: ta sama jednostka w brzmieniu obecnym (przypis „obowiązuje do
    # wejścia w życie zmiany”) i przyszłym (przypis „wejdzie w życie z dniem …”). Ustawiane z przypisów.
    version: Literal["until_change", "future"] | None = None
    effective_from: date | None = None

    def child(self, number: str) -> Unit:
        """Jednostka podrzędna po numerze; „§ 2” i „2” są równoważne (Ordynacja ma paragrafy)."""
        want = number.replace("§", "").strip()
        found = [c for c in self.children if c.number is not None and c.number.replace("§", "").strip() == want]
        if len(found) == 1:
            return found[0]
        if found:  # kilka wersji tej samej jednostki: obowiązująca w stanie korpusu, nie przyszła
            current = [c for c in found if c.version != "future" and not c.repealed]
            return (current or found)[0]
        raise KeyError(f"{self.kind} {self.number}: brak jednostki podrzędnej {number!r}")

    def walk(self) -> list[Unit]:
        out: list[Unit] = [self]
        for c in self.children:
            out.extend(c.walk())
        return out


class Article(Unit):
    kind: UnitKind = "article"
    path: list[str] = Field(default_factory=list)  # np. ["DZIAŁ IX Odliczenie…", "Rozdział 1 Odliczenie…"]


class AnnexRow(BaseModel):
    position: str
    cells: dict[str, str]
    section: str | None = None
    page: int


class Annex(BaseModel):
    number: str
    title: str = ""
    text: str = ""
    repealed: bool = False
    rows: list[AnnexRow] = Field(default_factory=list)
    footnote_refs: list[int] = Field(default_factory=list)
    page: int


class Source(BaseModel):
    key: str  # krótka nazwa, np. "vat"
    eli: str  # ELI tekstu jednolitego, np. "DU/2026/1263"
    name: str
    url: str
    sha256: str


class Act(BaseModel):
    source: Source
    title: str
    act_date: date | None
    state_date: date | None  # stan prawny tekstu jednolitego (D1)
    articles: list[Article]
    annexes: list[Annex] = Field(default_factory=list)
    footnotes: dict[int, str] = Field(default_factory=dict)

    def article(self, number: str) -> Article:
        for a in self.articles:
            if a.number == number:
                return a
        raise KeyError(f"{self.source.key}: brak art. {number}")

    def annex(self, number: str) -> Annex:
        for a in self.annexes:
            if a.number == number:
                return a
        raise KeyError(f"{self.source.key}: brak załącznika nr {number}")
