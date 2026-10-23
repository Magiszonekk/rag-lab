"""Lista źródeł i pobieranie PDF-ów z API Sejmu z weryfikacją sha256."""

from __future__ import annotations

import hashlib
import tomllib
from pathlib import Path

import httpx

from raglab.models import Source

REPO_ROOT = Path(__file__).resolve().parents[3]
SOURCES_FILE = REPO_ROOT / "data" / "sources.toml"
RAW_DIR = REPO_ROOT / "data" / "raw"


class ChecksumError(RuntimeError):
    pass


def load_sources(path: Path = SOURCES_FILE) -> list[Source]:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    return [Source(**s) for s in data["source"]]


def get_source(key: str) -> Source:
    for s in load_sources():
        if s.key == key:
            return s
    raise KeyError(key)


def pdf_path(source: Source) -> Path:
    return RAW_DIR / (source.eli.replace("/", "_") + ".pdf")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def fetch(source: Source, *, client: httpx.Client | None = None) -> Path:
    """Pobiera PDF, jeśli go brak; zawsze sprawdza sha256."""
    path = pdf_path(source)
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        own = client is None
        c = client or httpx.Client(timeout=120, follow_redirects=True)
        try:
            r = c.get(source.url)
            r.raise_for_status()
            tmp = path.with_suffix(".part")
            tmp.write_bytes(r.content)
            tmp.rename(path)
        finally:
            if own:
                c.close()
    actual = sha256_file(path)
    if actual != source.sha256:
        raise ChecksumError(
            f"{source.key} ({source.eli}): sha256 {actual} != oczekiwane {source.sha256}. "
            "Plik u źródła się zmienił — odświeżenie korpusu wymaga świadomej decyzji (koncept D1)."
        )
    return path
