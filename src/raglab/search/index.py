"""Indeksy wyszukiwania (koncept D3, D4, D12): BM25 na lematach, wektory, fuzja RRF.

Wszystko w pamięci — korpus M1 to ~5 tys. fragmentów. Postgres + pgvector dojdzie przy API demo;
na tym etapie porównujemy jakość wyszukiwania, a pamięć jest prostsza i deterministyczna (CI, D8).
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path

import bm25s
import numpy as np

from raglab.ingest.sources import REPO_ROOT
from raglab.search.chunking import Chunk
from raglab.search.normalize import Normalizer

CACHE_DIR = REPO_ROOT / "data" / "cache"


@dataclass
class Hit:
    chunk: Chunk
    score: float


class BM25Index:
    def __init__(self, chunks: list[Chunk], normalizer: Normalizer, *, k1: float = 1.2, b: float = 0.75) -> None:
        self.chunks = chunks
        self.normalizer = normalizer
        self.signature = normalizer.signature
        corpus_tokens = [normalizer.normalize(c.text) for c in chunks]
        self.retriever = bm25s.BM25(k1=k1, b=b)
        self.retriever.index(corpus_tokens, show_progress=False)

    def search(self, query: str, k: int = 20) -> list[Hit]:
        q = self.normalizer.normalize(query)
        if not q:
            return []
        scores = self.retriever.get_scores(q)
        top = np.argsort(-scores)[:k]
        return [Hit(self.chunks[i], float(scores[i])) for i in top if scores[i] > 0]


def _model_cached(model: str) -> bool:
    snap = Path.home() / ".cache" / "huggingface" / "hub" / f"models--{model.replace('/', '--')}" / "snapshots"
    return snap.exists() and any(snap.iterdir())


class Embedder:
    """sentence-transformers na CPU z cache na dysku (klucz: model + tekst) — D12."""

    def __init__(self, model: str, *, query_prefix: str = "", doc_prefix: str = "", batch_size: int = 32) -> None:
        # Model z lokalnego cache bez pytania Hugging Face o nowe wersje: na serwerze połączenie IPv6 z HF
        # potrafi wisieć w SYN-SENT (zmierzone 2026-10-23); pobrana wersja modelu i tak jest przypięta.
        if _model_cached(model):
            os.environ.setdefault("HF_HUB_OFFLINE", "1")
        from sentence_transformers import SentenceTransformer

        self.model_name = model
        self.query_prefix = query_prefix
        self.doc_prefix = doc_prefix
        self.batch_size = batch_size
        self.model = SentenceTransformer(model, device="cpu")
        self.model.max_seq_length = min(self.model.max_seq_length or 512, 512)
        safe = model.replace("/", "__")
        # cache: jedna macierz + lista kluczy (np.savez z tysiącami nazwanych tablic ładuje się minutami)
        self.cache_path = CACHE_DIR / f"emb_{safe}.npy"
        self.keys_path = CACHE_DIR / f"emb_{safe}.keys.json"
        self._cache: dict[str, np.ndarray] = {}
        self._dirty = False
        if self.cache_path.exists() and self.keys_path.exists():
            matrix = np.load(self.cache_path)
            keys = json.loads(self.keys_path.read_text())
            self._cache = {k: matrix[i] for i, k in enumerate(keys)}

    @staticmethod
    def _key(text: str) -> str:
        return hashlib.sha1(text.encode()).hexdigest()

    def encode(self, texts: list[str], *, is_query: bool) -> np.ndarray:
        prefix = self.query_prefix if is_query else self.doc_prefix
        full = [prefix + t for t in texts]
        keys = [self._key(t) for t in full]
        missing = [i for i, k in enumerate(keys) if k not in self._cache]
        if missing:
            vecs = self.model.encode(
                [full[i] for i in missing],
                batch_size=self.batch_size,
                normalize_embeddings=True,
                show_progress_bar=len(missing) > 200,
                convert_to_numpy=True,
            )
            for i, v in zip(missing, vecs, strict=True):
                self._cache[keys[i]] = v.astype(np.float32)
            self._dirty = True
            if not is_query or len(missing) > 50:
                self.save()
        return np.stack([self._cache[k] for k in keys])

    def save(self) -> None:
        if not self._dirty:
            return
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        keys = list(self._cache)
        np.save(self.cache_path, np.stack([self._cache[k] for k in keys]))
        self.keys_path.write_text(json.dumps(keys))
        self._dirty = False


class VectorIndex:
    def __init__(self, chunks: list[Chunk], embedder: Embedder) -> None:
        self.chunks = chunks
        self.embedder = embedder
        self.matrix = embedder.encode([c.text for c in chunks], is_query=False)

    def search(self, query: str, k: int = 20) -> list[Hit]:
        q = self.embedder.encode([query], is_query=True)[0]
        scores = self.matrix @ q
        top = np.argsort(-scores)[:k]
        return [Hit(self.chunks[i], float(scores[i])) for i in top]


def rrf(*rankings: list[Hit], k: int = 60, top: int = 20) -> list[Hit]:
    """Reciprocal rank fusion: score = Σ 1 / (k + rank)."""
    scores: dict[str, float] = {}
    by_id: dict[str, Chunk] = {}
    for ranking in rankings:
        for rank, h in enumerate(ranking, 1):
            scores[h.chunk.id] = scores.get(h.chunk.id, 0.0) + 1.0 / (k + rank)
            by_id[h.chunk.id] = h.chunk
    order = sorted(scores, key=lambda i: -scores[i])[:top]
    return [Hit(by_id[i], scores[i]) for i in order]


def write_index_meta(path: Path, meta: dict[str, object]) -> None:
    path.write_text(json.dumps(meta, ensure_ascii=False, indent=1), encoding="utf-8")
