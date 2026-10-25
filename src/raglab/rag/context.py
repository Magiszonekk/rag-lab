"""Budowa kontekstu dla modelu odpowiadającego (koncept D3 W3, D1, etap 2a).

- wyszukujemy fragmenty (ustępy), a do modelu idzie cały artykuł, jeśli jest krótki (≤ `max_article_tokens`),
  w przeciwnym razie sam fragment — „parent retrieval” z D3;
- każdy blok ma adres do cytowania, datę stanu prawnego i status czasowy (`raglab.annotate_temporal`);
- **przepisy zastępujące**: jeśli w kontekście jest przepis, którego wartość nadpisuje obowiązujący przepis
  przejściowy (np. VAT art. 41 ust. 1 „22%” ← art. 146ef „23%”), dokładamy przepis przejściowy z adnotacją.
  Bez tego system cytuje poprawny przepis i podaje nieaktualną stawkę — błąd nie do wykrycia sprawdzaniem cytatów.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from functools import lru_cache

from raglab.annotate_temporal import OUT as TEMPORAL_PATH
from raglab.annotate_temporal import load_labels
from raglab.corpus import ACT_LABEL, address, load_corpus, render_unit
from raglab.models import Act, Article
from raglab.search.chunking import Chunk, est_tokens
from raglab.search.index import Hit

STATUS_PL = {
    "in_force": "obowiązuje",
    "historical": "HISTORYCZNY — nie stosować do bieżących zdarzeń",
    "conditional": "warunkowy",
}


@dataclass
class Block:
    address: str  # adres do cytowania (artykuł albo fragment)
    act: str
    article: str
    text: str
    status: str
    note: str = ""
    units: set[str] = field(default_factory=set)  # adresy wszystkich jednostek zawartych w bloku
    replaces: set[str] = field(default_factory=set)  # przepis zastępujący: lokalne adresy, których wartość zastępuje

    def render(self, state_date: str) -> str:
        meta = f"stan prawny {state_date}; status: {STATUS_PL.get(self.status, self.status)}"
        if self.note:
            meta += f"; {self.note}"
        return f"[{self.address}] ({meta})\n{self.text}"


@lru_cache(maxsize=1)
def _corpus() -> dict[str, Act]:
    return load_corpus()


@lru_cache(maxsize=1)
def _overrides() -> dict[tuple[str, str], list[str]]:
    """(akt, adres zastępowany bez nazwy aktu) → numery obowiązujących artykułów, które zastępują jego WARTOŚĆ.

    Listy `overrides` od modelu (annotate_temporal) są zaszumione (np. art. 146ej — upoważnienie ministra —
    „zastępuje” art. 41 ust. 1). Dlatego kandydat przechodzi tylko, jeśli jego tekst dosłownie ustala wartość
    dla tego przepisu: „… o której mowa w art. 41 ust. 1 … wynosi 23 %”.
    """
    labels = load_labels()
    corpus = _corpus()
    out: dict[tuple[str, str], list[str]] = {}
    if not TEMPORAL_PATH.exists():
        return out
    for line in TEMPORAL_PATH.read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        if labels.get((r["act"], r["article"])) != "in_force":
            continue
        text = render_unit(corpus[r["act"]].article(r["article"]))
        sets_value = re.findall(r"o któr\w+ mowa w ([^;:]*?)wynosi\s+[\d,]+\s*%", text)
        for target in r.get("overrides") or []:
            m = re.match(r"^art\.\s*(\d+[a-ząćęłńóśźż]*)(?:\s+(ust\.|§)\s*(\d+[a-z]*))?", str(target))
            if not m:
                continue
            ref = rf"art\.\s*{re.escape(m.group(1))}\b" + (
                rf"\s+{re.escape(m.group(2))}\s*{m.group(3)}\b" if m.group(3) else ""
            )
            # „art. 41 ust. 1 i 13” — numer ustępu może stać na liście po „i” / przecinku
            ref_list = rf"art\.\s*{re.escape(m.group(1))}\s+ust\.\s*[\d\s,ia-z]*\b{m.group(3)}\b" if m.group(3) else ref
            if not any(re.search(ref, s) or re.search(ref_list, s) for s in sets_value):
                continue
            key = f"art. {m.group(1)}" + (f" {m.group(2)} {m.group(3)}" if m.group(3) else "")
            out.setdefault((r["act"], key), []).append(r["article"])
    return out


def _article_units(act_key: str, art: Article) -> set[str]:
    units: set[str] = set()

    def walk(chain: tuple) -> None:  # type: ignore[type-arg]
        units.add(address(act_key, chain))
        for c in chain[-1].children:
            walk((*chain, c))

    walk((art,))
    return units


def _article_block(act_key: str, art: Article, status: str, note: str = "") -> Block:
    label = ACT_LABEL.get(act_key, act_key)
    return Block(
        address=f"{label} art. {art.number}",
        act=act_key,
        article=art.number or "",
        text=render_unit(art),
        status=status,
        note=note,
        units=_article_units(act_key, art),
    )


def build_context(hits: list[Hit], *, k: int = 5, max_article_tokens: int = 1200, budget: int = 6000) -> list[Block]:
    corpus = _corpus()
    labels = load_labels()
    blocks: list[Block] = []
    seen_articles: set[tuple[str, str]] = set()
    used = 0
    for h in hits[:k]:
        c: Chunk = h.chunk
        act = corpus[c.act]
        status = labels.get((c.act, c.article), "in_force")
        art = act.article(c.article) if c.article else None
        if art is not None and est_tokens(render_unit(art)) <= max_article_tokens:
            if (c.act, c.article) in seen_articles:
                continue
            seen_articles.add((c.act, c.article))
            b = _article_block(c.act, art, status)
        else:
            label = c.header.split(" > ")[-1]
            b = Block(
                address=f"{ACT_LABEL.get(c.act, c.act)} {label}",
                act=c.act,
                article=c.article,
                text=c.body,
                status=status,
                units=set(c.covers),
            )
        cost = est_tokens(b.text)
        if used + cost > budget and blocks:
            break
        blocks.append(b)
        used += cost
    return attach_overrides(blocks, seen_articles, used, budget)


def attach_overrides(
    blocks: list[Block], seen_articles: set[tuple[str, str]], used: int, budget: int = 6000
) -> list[Block]:
    """Dokłada przepisy przejściowe zastępujące wartości z przepisów w kontekście (i adnotuje zastępowane)."""
    corpus = _corpus()
    # przepisy przejściowe zastępujące wartości z przepisów obecnych w kontekście
    ov = _overrides()
    extra: list[Block] = []
    for b in blocks:
        act_label = ACT_LABEL.get(b.act, b.act)
        for unit in sorted(b.units):
            local = unit[len(act_label) + 1 :]
            for art_no in ov.get((b.act, local), []):
                if (b.act, art_no) in seen_articles:
                    continue
                art = corpus[b.act].article(art_no)
                seen_articles.add((b.act, art_no))
                blk = _article_block(
                    b.act,
                    art,
                    "in_force",
                    note=f"przepis przejściowy zastępujący {local}; OBOWIĄZUJE w stanie prawnym korpusu "
                    "(brak obwieszczenia o końcu okresu)",
                )
                blk.replaces = {local}
                extra.append(blk)
            for e in extra:  # ten sam przepis zastępujący może dotyczyć kilku przepisów w kontekście
                if (b.act, e.article) in {(b.act, a) for a in ov.get((b.act, local), [])}:
                    e.replaces.add(local)
    # blok odsyła do okresu z obowiązującego przepisu zastępującego („w okresie, o którym mowa w art. 146ef”)
    overriding = {a for arts in ov.values() for a in arts}
    for b in list(blocks):
        for art_no in sorted(overriding):
            if (b.act, art_no) in seen_articles:
                continue
            if re.search(rf"o któr\w+ mowa w art\.\s*{re.escape(art_no)}\b", b.text):
                seen_articles.add((b.act, art_no))
                extra.append(
                    _article_block(
                        b.act,
                        corpus[b.act].article(art_no),
                        "in_force",
                        note="przepis przejściowy, do którego odsyła " + b.address,
                    )
                )
    for e in extra[:3]:
        if used + est_tokens(e.text) > budget * 1.3:
            break
        blocks.append(e)
        used += est_tokens(e.text)
        for b in blocks:
            if b is not e and e.replaces and any(u.endswith(" " + r) for u in b.units for r in e.replaces):
                b.note = (b.note + "; " if b.note else "") + (
                    f"UWAGA: wartość z tego przepisu jest obecnie zastąpiona — obowiązuje wartość z {e.address}"
                )
    return blocks


def block_for(addr: str, *, max_article_tokens: int = 1200) -> Block | None:
    """Blok dla adresu podanego przez agenta („VAT art. 86a ust. 1”): cały artykuł, jeśli krótki, inaczej jednostka.

    None, jeśli adres nie istnieje w korpusie.
    """
    from raglab.rag.verify import Corpus

    corpus = _corpus()
    labels = load_labels()
    resolved = Corpus.get().resolve(addr)
    if resolved is None:
        return None
    label, rest = resolved.split(" ", 1)
    act_key = next((k for k, v in ACT_LABEL.items() if v == label), None)
    m = re.match(r"art\. (\S+)", rest)
    if act_key is None or m is None:
        return None
    art = corpus[act_key].article(m.group(1))
    status = labels.get((act_key, art.number or ""), "in_force")
    if est_tokens(render_unit(art)) <= max_article_tokens or resolved == f"{label} art. {art.number}":
        return _article_block(act_key, art, status)
    units = {u for u in Corpus.get().text if u == resolved or u.startswith(resolved + " ")}
    text = Corpus.get().text[resolved]
    return Block(address=resolved, act=act_key, article=art.number or "", text=text, status=status, units=units)


def state_dates() -> dict[str, str]:
    return {k: str(a.state_date) for k, a in _corpus().items()}
