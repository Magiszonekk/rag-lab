"""Ingest: PDF z API Sejmu → struktura aktu → korpus JSON (koncept D1, D2)."""

from __future__ import annotations

from raglab.ingest.pdf_lines import read_pdf
from raglab.ingest.sources import fetch, pdf_path
from raglab.ingest.structure import parse_act
from raglab.ingest.tables import attach_table_rows
from raglab.models import Act, Source


def build_act(source: Source) -> Act:
    path = fetch(source)
    pdf = read_pdf(path)
    act = parse_act(pdf, source)
    attach_table_rows(pdf_path(source), act.annexes)
    return act
