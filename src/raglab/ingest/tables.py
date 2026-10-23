"""Tabele w załącznikach (np. zał. 3 VAT — stawka 8%) przez pdfplumber: jeden wiersz = jeden rekord (koncept D2).

pdfplumber rozpoznaje linie siatki tabeli, więc wiersz „Poz. 12 | PKWiU … | Pszenica” wychodzi w całości,
zamiast rozsypanego tekstu.

Reguły dla wierszy bez numeru pozycji:
- pierwszy wiersz tabeli na kolejnej stronie załącznika = kontynuacja pozycji z poprzedniej strony,
- w pozostałych miejscach = nagłówek sekcji („Towary spożywcze”), przypisywany kolejnym pozycjom.
"""

from __future__ import annotations

import re
from pathlib import Path

import pdfplumber
from pdfplumber.page import Page

from raglab.models import Annex, AnnexRow

_POS = re.compile(r"^\d+[a-z]*$")
_POS_HEADERS = {"poz", "lp", "l.p", "poz. nr"}


def _clean(cell: str | None) -> str:
    text = re.sub(r"\s*\n\s*", " ", cell or "").strip()
    # „zm.37))” → „zm.)” — znaczniki przypisów w komórkach (pdfplumber nie zna indeksu górnego)
    return re.sub(r"(?<=[\w.])\d{1,3}\)(?=\))", "", text)


def _extend(row: AnnexRow, cells: list[str], offset: int) -> None:
    """Dokleja kontynuację komórek (pozycja przechodząca na następną stronę)."""
    for key, c in zip(list(row.cells), cells[offset:], strict=False):
        if c:
            row.cells[key] = (row.cells[key] + " " + c).strip()


def _inside(inner: tuple[float, float, float, float], outer: tuple[float, float, float, float]) -> bool:
    return (
        inner[0] >= outer[0] - 1 and inner[1] >= outer[1] - 1 and inner[2] <= outer[2] + 1 and inner[3] <= outer[3] + 1
    )


def _annex_heads(page: Page) -> list[tuple[float, str]]:
    """Nagłówki „Załącznik nr N” na stronie (prawa kolumna), z pozycją pionową."""
    words = page.extract_words()
    heads: list[tuple[float, str]] = []
    for i, w in enumerate(words[:-2]):
        is_head = w["text"] == "Załącznik" and words[i + 1]["text"] == "nr" and w["x0"] > 300
        if is_head and (num := re.match(r"\d+[a-z]*", words[i + 2]["text"])):
            heads.append((float(w["top"]), num.group(0)))
    return heads


def _owner(heads: list[tuple[float, str]], top: float, current: str) -> str:
    """Do którego załącznika należy tabela zaczynająca się na wysokości `top`."""
    above = [num for h_top, num in heads if h_top < top]
    return above[-1] if above else current


def _footnote_number_prefix(num: str, known: set[str]) -> str:
    """„640” z „Załącznik nr 640)” → „6” (znacznik przypisu 40 doklejony do numeru)."""
    if num in known:
        return num
    for k in range(len(num) - 1, 0, -1):
        if num[:k] in known:
            return num[:k]
    return num


def attach_table_rows(pdf_path: Path, annexes: list[Annex]) -> None:
    if not annexes:
        return
    by_num = {a.number: a for a in annexes}
    first_page = min(a.page for a in annexes)
    with pdfplumber.open(pdf_path) as pdf:
        current = annexes[0].number
        headers: dict[str, list[str]] = {}
        sections: dict[str, str | None] = {}
        for pno in range(first_page, len(pdf.pages) + 1):
            page = pdf.pages[pno - 1]
            heads = [(t, _footnote_number_prefix(n, set(by_num))) for t, n in _annex_heads(page)]
            tables = page.find_tables()
            # pdfplumber czasem widzi „tabelę w tabeli” (ramka wokół fragmentu komórki) — pomijamy zagnieżdżone
            tables = [t for t in tables if not any(o is not t and _inside(t.bbox, o.bbox) for o in tables)]
            for table in sorted(tables, key=lambda t: t.bbox[1]):
                owner = _owner(heads, table.bbox[1], current)
                annex = by_num.get(owner)
                if annex is None or annex.repealed:
                    continue
                first_row = True
                for raw in table.extract():
                    cells = [_clean(c) for c in raw]
                    if not any(cells):
                        continue
                    header = headers.get(owner)
                    if header is None and not _POS.match(cells[0]):
                        headers[owner] = [c or f"kolumna {k + 1}" for k, c in enumerate(cells)]
                        continue
                    if header is not None and cells == header:
                        first_row = False
                        continue  # nagłówek powtórzony na kolejnej stronie
                    nonempty = [c for c in cells if c]
                    if len(nonempty) >= 2 and nonempty == [str(k + 1) for k in range(len(nonempty))]:
                        continue  # wiersz numeracji kolumn „1 | 2 | 3”
                    has_pos = (header or [""])[0].rstrip(".").lower() in _POS_HEADERS
                    if header is not None and not has_pos:
                        # tabela bez kolumny pozycji (np. „Kod CN | Wyszczególnienie”): numer = kolejność
                        if first_row and annex.rows and pno > annex.rows[-1].page and not cells[0]:
                            _extend(annex.rows[-1], cells, offset=0)
                        else:
                            annex.rows.append(
                                AnnexRow(
                                    position=str(len(annex.rows) + 1),
                                    cells={header[k]: c for k, c in enumerate(cells) if k < len(header)},
                                    section=sections.get(owner),
                                    page=pno,
                                )
                            )
                    elif _POS.match(cells[0]):
                        names = header or [f"kolumna {k + 1}" for k in range(len(cells))]
                        annex.rows.append(
                            AnnexRow(
                                position=cells[0],
                                cells={names[k]: c for k, c in enumerate(cells) if 0 < k < len(names)},
                                section=sections.get(owner),
                                page=pno,
                            )
                        )
                    elif first_row and annex.rows and pno > annex.rows[-1].page:
                        _extend(annex.rows[-1], cells, offset=1)
                    else:
                        sections[owner] = next((c for c in reversed(cells) if c), None)
                    first_row = False
                current = owner
            if heads:
                current = heads[-1][1]
