"""Warstwa 2 ingestu: logiczne linie → struktura aktu (koncept D2).

Hierarchia: akt → (dział / rozdział / oddział jako ścieżka) → artykuł → ustęp → punkt → litera.
Tirety są doklejane do tekstu najgłębszej jednostki; „część wspólna” po wyliczeniu (np. „– jeżeli …”)
trafia do pola `tail` jednostki nadrzędnej.

Granice jednostek rozpoznajemy po trzech cechach naraz: wzorcu na początku linii („Art. 5.”, „2a.”,
„3)”, „b)”), wcięciu (x względem lewego marginesu) i odstępie pionowym (nowa jednostka ma większy
odstęp niż kolejna linia tego samego akapitu). Sam regex na tekście nie wystarcza.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date

from raglab.ingest.pdf_lines import Line, PdfText, join_lines
from raglab.models import Act, Annex, Article, Source, Unit

MONTHS = {
    "stycznia": 1, "lutego": 2, "marca": 3, "kwietnia": 4, "maja": 5, "czerwca": 6,
    "lipca": 7, "sierpnia": 8, "września": 9, "października": 10, "listopada": 11, "grudnia": 12,
}  # fmt: skip

# Numery jednostek mogą mieć polskie litery (PIT: art. 22ł, 22ł¹ nie występuje, ale „ł” tak).
LET = "a-ząćęłńóśźż"
NUM = rf"\d+[{LET}]*(?:[–-]\d+[{LET}]*)?"
RE_ART = re.compile(rf"^Art\.\s*({NUM})\.\s*(.*)$")
# Ustęp: „2a. Treść…” (ustawy) albo „§ 2a. Treść…” (kodeksy, np. Ordynacja podatkowa).
RE_PARA = re.compile(rf"^((?:§\s*)?{NUM})\.\s+(.*)$")
RE_POINT = re.compile(rf"^({NUM})\)\s*(.*)$")
RE_LETTER = re.compile(rf"^([{LET}]{{1,3}}(?:[–-][{LET}]{{1,3}})?)\)\s*(.*)$")
RE_HEADING = re.compile(r"^(DZIAŁ|Dział|TYTUŁ|Tytuł|Rozdział|ROZDZIAŁ|Oddział|ODDZIAŁ)\s+\S+")
RE_REPEALED = re.compile(r"^\((uchylony|uchylona|uchylone|pominięty|pominięta|pominięte)\)\s*$")
RE_ANNEX = re.compile(r"^Załącznik\s+nr\s+(\d+[a-z]*)\b")
RE_DATE = re.compile(r"(\d{1,2})\s+(" + "|".join(MONTHS) + r")\s+(\d{4})\s*r\.")

NEW_BLOCK_GAP = 14.5  # pt; kolejna linia akapitu ma ~12–13 pt odstępu, nowa jednostka ≥ 15 pt
MARKED_BLOCK_GAP = 13.6  # pt; próg dla linii, które zaczynają się znacznikiem jednostki


class StructureError(RuntimeError):
    pass


def _parse_date(text: str) -> date | None:
    m = RE_DATE.search(text)
    if not m:
        return None
    return date(int(m.group(3)), MONTHS[m.group(2)], int(m.group(1)))


@dataclass
class _Block:
    lines: list[Line]

    @property
    def first(self) -> Line:
        return self.lines[0]

    @property
    def text(self) -> str:
        out = ""
        for ln in self.lines:
            out = join_lines(out, ln.text)
        return out.strip()

    @property
    def refs(self) -> list[int]:
        return [r for ln in self.lines for r in ln.footnote_refs]


def _is_repealed(text: str) -> bool:
    return bool(RE_REPEALED.match(text.strip()))


class _Builder:
    def __init__(self, left: float) -> None:
        self.left = left
        self.indent = left + 21.0
        self.articles: list[Article] = []
        self.path: dict[str, str] = {}
        self.art: Article | None = None
        self.para: Unit | None = None
        self.point: Unit | None = None
        self.letter: Unit | None = None

    # --- pomocnicze -------------------------------------------------------------------------
    def _near(self, x: float, target: float, tol: float = 6.0) -> bool:
        return abs(x - target) <= tol

    def _deepest(self) -> Unit:
        for u in (self.letter, self.point, self.para, self.art):
            if u is not None:
                return u
        raise StructureError("tekst poza artykułem")

    def _append(self, unit: Unit, text: str, refs: list[int], sep: str = "\n") -> None:
        unit.text = (unit.text + sep + text).strip() if unit.text else text
        unit.footnote_refs += refs

    def _point_parent(self) -> Unit:
        assert self.art is not None
        return self.para if self.para is not None else self.art

    # --- jednostki ----------------------------------------------------------------------------
    def heading(self, block: _Block, title: str) -> None:
        kind = block.text.split()[0].lower()
        level = {"dział": 0, "tytuł": 0, "rozdział": 1, "oddział": 2}[kind]
        for k in [k for k in self.path if {"dział": 0, "tytuł": 0, "rozdział": 1, "oddział": 2}[k] >= level]:
            del self.path[k]
        self.path[kind] = f"{block.text} {title}".strip()

    def article(self, number: str, rest: str, block: _Block) -> None:
        page = block.first.page
        art = Article(number=number, page=page, path=list(self.path.values()))
        self.articles.append(art)
        self.art, self.para, self.point, self.letter = art, None, None, None
        m = RE_PARA.match(rest)
        if m:
            self.paragraph(m.group(1), m.group(2), block.refs, page)
        elif _is_repealed(rest):
            art.repealed = True
        else:
            self._append(art, rest, block.refs)

    def paragraph(self, number: str, rest: str, refs: list[int], page: int) -> None:
        assert self.art is not None
        u = Unit(kind="paragraph", number=number, page=page, repealed=_is_repealed(rest))
        if not u.repealed:
            u.text = rest
        u.footnote_refs = refs
        self.art.children.append(u)
        self.para, self.point, self.letter = u, None, None

    def point_(self, number: str, rest: str, refs: list[int], page: int) -> None:
        u = Unit(
            kind="point",
            number=number,
            page=page,
            repealed=_is_repealed(rest),
            footnote_refs=refs,
        )
        if not u.repealed:
            u.text = rest
        self._point_parent().children.append(u)
        self.point, self.letter = u, None

    def letter_(self, number: str, rest: str, refs: list[int], page: int) -> None:
        if self.point is None:
            raise StructureError(f"litera {number}) bez punktu (art. {self.art and self.art.number}, s. {page})")
        u = Unit(
            kind="letter",
            number=number,
            page=page,
            repealed=_is_repealed(rest),
            footnote_refs=refs,
        )
        if not u.repealed:
            u.text = rest
        self.point.children.append(u)
        self.letter = u

    def dash(self, block: _Block) -> None:
        text, x = block.text, block.first.x
        if x >= self.indent + 10:  # tiret wewnątrz litery / punktu
            self._append(self._deepest(), text, block.refs)
            return
        if self._near(x, self.left):  # część wspólna po wyliczeniu punktów
            target = self._point_parent() if self.point is not None else self._deepest()
            self.point = self.letter = None
        elif self.letter is not None:  # część wspólna po wyliczeniu liter
            assert self.point is not None
            target = self.point
            self.letter = None
        else:
            self._append(self._deepest(), text, block.refs)
            return
        target.tail = (target.tail + "\n" + text).strip()
        target.footnote_refs += block.refs

    def feed(self, block: _Block) -> None:
        text, x, page = block.text, block.first.x, block.first.page
        if (m := RE_ART.match(text)) and block.first.bold:
            self.article(m.group(1), m.group(2), block)
        elif self.art is None:
            return  # nagłówek aktu przed art. 1
        elif (m := RE_PARA.match(text)) and self._near(x, self.indent):
            self.paragraph(m.group(1), m.group(2), block.refs, page)
        elif (m := RE_POINT.match(text)) and self._near(x, self.left):
            self.point_(m.group(1), m.group(2), block.refs, page)
        elif (m := RE_LETTER.match(text)) and self._near(x, self.indent):
            self.letter_(m.group(1), m.group(2), block.refs, page)
        elif text.startswith(("–", "‒")):
            self.dash(block)
        else:
            self._append(self._deepest(), text, block.refs)


def _blocks(lines: list[Line], left: float) -> list[_Block]:
    """Grupuje linie w bloki = pojedyncze jednostki (nagłówek, artykuł, ustęp, punkt, tiret…)."""
    starts = (RE_ART, RE_PARA, RE_POINT, RE_LETTER)
    blocks: list[_Block] = []
    prev: Line | None = None
    for ln in lines:
        t = ln.text.strip()
        looks_new = any(r.match(t) for r in starts) or t.startswith(("–", "‒")) or bool(RE_HEADING.match(t))
        if prev is None:
            new = True
        elif ln.page != prev.page:
            # pierwsza linia strony: brak odstępu do porównania, decyduje wzorzec + wcięcie
            new = looks_new and not (RE_PARA.match(t) and abs(ln.x - left) < 6)
        else:
            gap = ln.y - prev.y
            # Linia ze znacznikiem jednostki („5)”, „a)”, „2.”) wystarcza z mniejszym odstępem:
            # zmierzone na VAT — nowe punkty mają 14–21 pt, kontynuacje akapitu ≤ 13 pt.
            new = gap > NEW_BLOCK_GAP or (looks_new and gap > MARKED_BLOCK_GAP) or (ln.bold and bool(RE_ART.match(t)))
        if new:
            blocks.append(_Block([ln]))
        else:
            blocks[-1].lines.append(ln)
        prev = ln
    return blocks


def parse_act(pdf: PdfText, source: Source) -> Act:
    lines = pdf.lines
    # Tekst aktu zaczyna się po „Załącznik do obwieszczenia …”; wcześniej jest obwieszczenie,
    # które cytuje przepisy przejściowe innych ustaw („Art. 11. …”) — nie należą do korpusu.
    start = next(
        (i for i, ln in enumerate(lines) if ln.text.startswith("Załącznik do obwieszczenia")),
        None,
    )
    if start is None:
        raise StructureError(f"{source.key}: nie znaleziono początku tekstu jednolitego")
    preamble = " ".join(ln.text for ln in lines[:start])
    state = re.search(r"stanu prawnego na dzień\s+(\d{1,2}\s+\w+\s+\d{4}\s*r\.)", preamble)
    body = lines[start:]

    annex_start = next(
        (
            i
            for i, ln in enumerate(body)
            if ln.x > 300 and (ln.text.startswith("Załączniki do ustawy") or RE_ANNEX.match(ln.text))
        ),
        len(body),
    )
    act_lines, annex_lines = body[:annex_start], body[annex_start:]

    title_lines = [ln.text.strip() for ln in act_lines[:12]]
    act_date = next(
        (d for t in title_lines if t.startswith("z dnia") and (d := _parse_date(t))),
        None,
    )

    builder = _Builder(pdf.left_margin)
    blocks = _blocks(act_lines, pdf.left_margin)
    i = 0
    while i < len(blocks):
        b = blocks[i]
        if RE_HEADING.match(b.text) and b.first.x > pdf.left_margin + 60 and not b.first.bold:
            title = ""
            while i + 1 < len(blocks) and blocks[i + 1].first.bold and not RE_ART.match(blocks[i + 1].text):
                i += 1
                title = join_lines(title, blocks[i].text)
            builder.heading(b, title)
        else:
            builder.feed(b)
        i += 1

    footnotes = {n: f.text for n, f in pdf.footnotes.items()}
    _mark_versions(builder.articles, footnotes)
    return Act(
        source=source,
        title=source.name,
        act_date=act_date,
        state_date=_parse_date(state.group(1)) if state else None,
        articles=builder.articles,
        annexes=_annexes(annex_lines, pdf.left_margin),
        footnotes=footnotes,
    )


def _annexes(lines: list[Line], left: float) -> list[Annex]:
    """Załączniki jako osobne dokumenty. Wiersze tabel dokłada `tables.py` (pdfplumber)."""
    annexes: list[Annex] = []
    for ln in lines:
        m = RE_ANNEX.match(ln.text.strip())
        if m and ln.x > 300:
            annexes.append(Annex(number=m.group(1), page=ln.page))
            continue
        if not annexes:
            continue
        a = annexes[-1]
        t = ln.text.strip()
        if not a.text and _is_repealed(t):
            a.repealed = True
            continue
        a.text = (a.text + "\n" + t).strip()
        a.footnote_refs += ln.footnote_refs
        if not a.title and t.isupper() and len(t) > 10:
            a.title = t
    return annexes


RE_UNTIL = re.compile(r"(w tym brzmieniu )?obowiązuje do (dnia )?wejścia w życie zmiany", re.IGNORECASE)
RE_FUTURE = re.compile(r"wejdzie w życie z dniem\s+(\d{1,2}\s+\w+\s+\d{4}\s*r\.)", re.IGNORECASE)


def _mark_versions(articles: list[Article], footnotes: dict[int, str]) -> None:
    """Oznacza jednostki „dwuwersyjne” na podstawie treści przypisów (koncept D1)."""
    for art in articles:
        for unit in art.walk():
            for ref in unit.footnote_refs:
                note = footnotes.get(ref, "")
                if RE_UNTIL.search(note):
                    unit.version = "until_change"
                elif m := RE_FUTURE.search(note):
                    unit.version = "future"
                    unit.effective_from = _parse_date(m.group(1))
