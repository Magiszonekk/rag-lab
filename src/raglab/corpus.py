"""Adresowanie jednostek korpusu: „VAT art. 86 ust. 2 pkt 1 lit. a” (koncept D6: odpowiedź = adres prawny)."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

from raglab.ingest.sources import REPO_ROOT, load_sources
from raglab.models import Act, Article, Unit

CORPUS_DIR = REPO_ROOT / "data" / "corpus"
ACT_LABEL = {"vat": "VAT", "pit": "PIT", "op": "Ordynacja"}


@dataclass(frozen=True)
class Located:
    act: str  # klucz aktu, np. "vat"
    article: Article
    chain: tuple[Unit, ...]  # od artykułu do jednostki (włącznie)

    @property
    def unit(self) -> Unit:
        return self.chain[-1]

    @property
    def address(self) -> str:
        return address(self.act, self.chain)

    def full_text(self) -> str:
        """Treść jednostki z kontekstem nadrzędnym (zdania wprowadzające) i podrzędnym."""
        intro = [u.text for u in self.chain[:-1] if u.text]
        return "\n".join([*intro, render_unit(self.unit)])


def _part(u: Unit) -> str:
    n = u.number or ""
    if u.kind == "article":
        return f"art. {n}"
    if u.kind == "paragraph":
        return n if n.startswith("§") else f"ust. {n}"
    if u.kind == "point":
        return f"pkt {n}"
    return f"lit. {n}"


def address(act: str, chain: tuple[Unit, ...] | list[Unit]) -> str:
    return " ".join([ACT_LABEL.get(act, act), *(_part(u) for u in chain)])


def render_unit(u: Unit, depth: int = 0) -> str:
    lines = [("  " * depth + (u.text if not u.repealed else "(uchylony)")).rstrip()]
    for c in u.children:
        label = f"{c.number})" if c.kind in ("point", "letter") else f"{c.number}."
        lines.append("  " * (depth + 1) + label + " " + render_unit(c, depth + 1).lstrip())
    if u.tail:
        lines.append("  " * depth + u.tail)
    return "\n".join(line for line in lines if line.strip())


def load_act(key: str, corpus_dir: Path = CORPUS_DIR) -> Act:
    return Act.model_validate_json((corpus_dir / f"{key}.json").read_text(encoding="utf-8"))


def load_corpus(corpus_dir: Path = CORPUS_DIR) -> dict[str, Act]:
    return {s.key: load_act(s.key, corpus_dir) for s in load_sources()}


def iter_units(act: Act) -> Iterator[Located]:
    def walk(chain: tuple[Unit, ...]) -> Iterator[tuple[Unit, ...]]:
        yield chain
        for c in chain[-1].children:
            yield from walk((*chain, c))

    for art in act.articles:
        for chain in walk((art,)):
            yield Located(act.source.key, art, chain)
