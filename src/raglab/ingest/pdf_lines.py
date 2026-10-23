"""Warstwa 1 ingestu: PDF Dziennika Ustaw → logiczne linie tekstu (koncept D2).

Co robi:
- wyznacza rozmiar czcionki treści per PDF (najczęstszy rozmiar, nie wpisany na sztywno),
- odcina nagłówek strony („Dziennik Ustaw – N – Poz. X”) po pozycji,
- rozpoznaje przypisy po czcionce: blok małych linii u dołu strony zaczynający się
  znacznikiem „N)” w indeksie górnym,
- usuwa znaczniki przypisów doklejone do słów (`zm.1))`, `Załącznik nr 640)`) — to osobne
  spany w indeksie górnym — i zapamiętuje numery przypisów przy linii,
- skleja fragmenty z tej samej wysokości (np. „1) ” i treść punktu) w jedną linię.
"""

from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

import pymupdf

HEADER_MAX_Y = 62.0
SAME_LINE_TOL = 2.5
_FOOTNOTE_MARK = re.compile(r"^\s*(\d+)\)\s*$")
_HEADER_TEXT = re.compile(r"^(Dziennik Ustaw|– \d+ –|Poz\. \d+)\s*$")


@dataclass
class Line:
    page: int  # numer strony od 1
    y: float
    x: float
    text: str
    size: float
    bold: bool
    footnote_refs: list[int] = field(default_factory=list)


@dataclass
class Footnote:
    number: int
    text: str
    page: int


@dataclass
class PdfText:
    lines: list[Line]
    footnotes: dict[int, Footnote]
    body_size: float
    left_margin: float
    page_count: int


@dataclass
class _Seg:
    y: float
    x: float
    text: str
    size: float
    bold: bool
    refs: list[int]
    min_size: float


def _body_size(doc: pymupdf.Document) -> float:
    sizes: Counter[float] = Counter()
    for pno in range(doc.page_count):
        for block in doc[pno].get_text("dict")["blocks"]:
            for line in block.get("lines", []):
                for span in line["spans"]:
                    if span["text"].strip():
                        sizes[round(span["size"], 1)] += len(span["text"])
    return sizes.most_common(1)[0][0]


def _segments(page: pymupdf.Page, body: float) -> list[_Seg]:
    segs: list[_Seg] = []
    for block in page.get_text("dict")["blocks"]:
        for line in block.get("lines", []):
            spans = [s for s in line["spans"] if s["text"]]
            if not "".join(s["text"] for s in spans).strip():
                continue
            text_parts: list[str] = []
            refs: list[int] = []
            for i, s in enumerate(spans):
                small = s["size"] < body - 2.0
                # Znacznik przypisu w treści: mały span „N)” w indeksie górnym, nie na początku linii.
                if small and i > 0 and (m := _FOOTNOTE_MARK.match(s["text"])):
                    refs.append(int(m.group(1)))
                    continue
                text_parts.append(s["text"])
            first = spans[0]
            visible = [s for s in spans if s["text"].strip()] or spans
            segs.append(
                _Seg(
                    y=line["bbox"][1],
                    x=line["bbox"][0],
                    text="".join(text_parts),
                    # rozmiar liczony bez spanów z samymi spacjami (bywają 12 pt w linii przypisu 9 pt)
                    size=max(s["size"] for s in visible),
                    bold=bool(first["flags"] & 16),
                    refs=refs,
                    min_size=min(s["size"] for s in visible),
                )
            )
    segs.sort(key=lambda s: (round(s.y / SAME_LINE_TOL), s.x))
    return segs


def _merge_same_y(segs: list[_Seg]) -> list[_Seg]:
    """Skleja segmenty z tej samej wysokości, w kolejności od lewej (np. „1) ” + treść punktu).

    Uwaga: y fragmentów jednej linii różni się o ułamki punktu (znacznik „1)” bywa 0,4 pt niżej
    niż treść), dlatego najpierw grupujemy po y z tolerancją, a dopiero potem sortujemy po x.
    """
    groups: list[list[_Seg]] = []
    for s in sorted(segs, key=lambda s: s.y):
        if groups and abs(groups[-1][0].y - s.y) <= SAME_LINE_TOL:
            groups[-1].append(s)
        else:
            groups.append([s])
    out: list[_Seg] = []
    for g in groups:
        g.sort(key=lambda s: s.x)
        first = g[0]
        merged = _Seg(
            min(s.y for s in g),
            first.x,
            first.text,
            first.size,
            first.bold,
            list(first.refs),
            first.min_size,
        )
        for s in g[1:]:
            sep = "" if merged.text.endswith(" ") or s.text.startswith(" ") else " "
            merged.text = merged.text + sep + s.text
            merged.refs += s.refs
            merged.size = max(merged.size, s.size)
            merged.min_size = min(merged.min_size, s.min_size)
            merged.bold = merged.bold or (s.bold and s.text.strip().startswith("Art."))
        out.append(merged)
    return out


def _split_footnotes(segs: list[_Seg], body: float) -> tuple[list[_Seg], list[_Seg]]:
    """Blok przypisów = ciągły ciąg małych linii u dołu strony, od pierwszego znacznika „N)”."""
    i = len(segs)
    while i > 0 and segs[i - 1].size < body - 0.5:
        i -= 1
    tail = segs[i:]
    start = next(
        (k for k, s in enumerate(tail) if s.min_size < body - 2.0 and re.match(r"^\s*\d+\)", s.text)),
        None,
    )
    if start is None:
        return segs, []
    return segs[: i + start], tail[start:]


def read_pdf(path: Path) -> PdfText:
    doc = pymupdf.open(path)
    body = _body_size(doc)
    lines: list[Line] = []
    footnotes: dict[int, Footnote] = {}
    for pno in range(1, doc.page_count + 1):
        raw = [
            s for s in _segments(doc[pno - 1], body) if not (s.y < HEADER_MAX_Y and _HEADER_TEXT.match(s.text.strip()))
        ]
        segs = _merge_same_y(raw)
        content, notes = _split_footnotes(segs, body)
        current: Footnote | None = None
        for n in notes:
            m = re.match(r"^\s*(\d+)\)\s*(.*)$", n.text)
            if m and n.min_size < body - 2.0:
                current = Footnote(int(m.group(1)), m.group(2).strip(), pno)
                footnotes[current.number] = current
            elif current is not None:
                current.text = _join(current.text, n.text.strip())
        for s in content:
            lines.append(Line(pno, s.y, s.x, s.text.rstrip(), s.size, s.bold, s.refs))
    margin = Counter(round(ln.x) for ln in lines if ln.size >= body - 0.5).most_common(2)
    left = float(min(x for x, _ in margin))
    return PdfText(lines, footnotes, body, left, doc.page_count)


def _join(a: str, b: str) -> str:
    """Skleja dwie linie, obsługując przeniesienia wyrazów."""
    a = a.rstrip()
    b = b.lstrip()
    if not a:
        return b
    if not b:
        return a
    if a.endswith("-") and b.startswith("-"):
        return a + b[1:]  # polska typografia: łącznik powtórzony na początku następnej linii
    if a.endswith("-") and not a.endswith(" -") and b[0].islower():
        return a[:-1] + b
    return a + " " + b


join_lines = _join
