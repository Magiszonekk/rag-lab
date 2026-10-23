"""Podział korpusu na fragmenty (koncept D3).

Strategie:
- `structural` (domyślna, D3 W2): fragment = ustęp (albo artykuł bez ustępów) z nagłówkiem kontekstu
  „Ustawa o VAT > DZIAŁ IX … > Rozdział 1 … > art. 86 ust. 2”; ustęp dłuższy niż `max_tokens` dzielony na
  grupy punktów, każda z nagłówkiem i zdaniem wprowadzającym ustępu; krótkie sąsiednie ustępy tego samego
  artykułu sklejane do `min_tokens`;
- `fixed` (punkt odniesienia): okna `window` tokenów z zakładką `overlap`, bez znajomości struktury.

Każdy fragment zna listę adresów jednostek, które zawiera (`covers`) — po tym liczymy trafienia (D6:
trafienie = fragment zawiera ustęp wzorcowy albo ustęp wzorcowy zawiera fragment).
Tokeny liczone szacunkowo: 1,6 × liczba słów (tak jak w pomiarach z konceptu).
"""

from __future__ import annotations

from dataclasses import dataclass, field

from raglab.annotate_temporal import load_labels
from raglab.corpus import ACT_LABEL, Located, address, iter_units, render_unit
from raglab.models import Act, Article, Unit

ACT_TITLE = {"vat": "Ustawa o VAT", "pit": "Ustawa o PIT", "op": "Ordynacja podatkowa"}


def est_tokens(text: str) -> int:
    return int(len(text.split()) * 1.6)


@dataclass
class Chunk:
    id: str
    act: str
    article: str
    covers: list[str]  # adresy jednostek zawartych w fragmencie (wszystkie poziomy)
    header: str
    body: str
    status: str = "in_force"  # etykieta czasowa artykułu (annotate_temporal)
    meta: dict[str, str] = field(default_factory=dict)
    # ile słów WŁASNEGO tekstu każdej jednostki jest we fragmencie — do ścisłej miary trafienia
    own_words: dict[str, int] = field(default_factory=dict)

    @property
    def body_words(self) -> int:
        return sum(self.own_words.values()) or len(self.body.split())

    @property
    def text(self) -> str:
        return f"{self.header}\n{self.body}"


def _header(act: Act, art: Article, unit_label: str) -> str:
    parts = [ACT_TITLE.get(act.source.key, act.source.name), *art.path, unit_label]
    return " > ".join(p for p in parts if p)


def _covers(act_key: str, chain: tuple[Unit, ...]) -> list[str]:
    out: list[str] = []

    def walk(ch: tuple[Unit, ...]) -> None:
        out.append(address(act_key, ch))
        for c in ch[-1].children:
            walk((*ch, c))

    walk(chain)
    return out


def structural(act: Act, *, max_tokens: int = 400, min_tokens: int = 50) -> list[Chunk]:
    labels = load_labels()
    key = act.source.key
    chunks: list[Chunk] = []

    words_of = {loc.address: len((loc.unit.text + " " + loc.unit.tail).split()) for loc in iter_units(act)}

    def add(art: Article, chain: tuple[Unit, ...], label: str, body: str, covers: list[str]) -> None:
        cid = f"{key}:{address(key, chain)}:{len(chunks)}"
        chunks.append(
            Chunk(
                id=cid,
                act=key,
                article=art.number or "",
                covers=covers,
                header=_header(act, art, label),
                body=body,
                status=labels.get((key, art.number or ""), "in_force"),
                own_words={a: words_of.get(a, 0) for a in covers if words_of.get(a, 0)},
            )
        )

    for art in act.articles:
        if art.repealed:
            continue
        units = (
            [art]
            if not any(c.kind == "paragraph" for c in art.children)
            else [c for c in art.children if c.kind == "paragraph" and not c.repealed]
        )
        pending: list[tuple[tuple[Unit, ...], str]] = []  # krótkie ustępy do sklejenia

        def flush_pending(art: Article = art, pending: list[tuple[tuple[Unit, ...], str]] = pending) -> None:
            if not pending:
                return
            chains = [ch for ch, _ in pending]
            labels_ = [address(key, ch).split(" ", 1)[1] for ch in chains]
            label = labels_[0] if len(labels_) == 1 else f"{labels_[0]}–{labels_[-1].split()[-1]}"
            body = "\n".join(b for _, b in pending)
            covers = [a for ch in chains for a in _covers(key, ch)]
            add(art, chains[0], label, body, covers)
            pending.clear()

        for unit in units:
            chain: tuple[Unit, ...] = (art,) if unit is art else (art, unit)
            body = render_unit(unit) if unit is art else _par_text(unit)
            label = address(key, chain).split(" ", 1)[1]
            if unit is not art and art.text:  # artykuł z tekstem przed ustępami (rzadkie)
                body = art.text + "\n" + body
            n = est_tokens(body)
            if n <= max_tokens:
                if n < min_tokens:
                    pending.append((chain, body))
                    if sum(est_tokens(b) for _, b in pending) >= min_tokens:
                        flush_pending()
                    continue
                flush_pending()
                add(art, chain, label, body, _covers(key, chain))
                continue
            flush_pending()
            # długi ustęp → grupy punktów z tym samym nagłówkiem i zdaniem wprowadzającym
            intro = unit.text
            points = [c for c in unit.children if not c.repealed]
            if not points:
                add(art, chain, label, body, _covers(key, chain))
                continue
            group: list[Unit] = []
            size = est_tokens(intro)
            for p in points:
                ptxt = _point_text(p)
                if group and size + est_tokens(ptxt) > max_tokens:
                    _add_group(add, key, art, chain, label, intro, group, unit)
                    group, size = [], est_tokens(intro)
                group.append(p)
                size += est_tokens(ptxt)
            if group:
                _add_group(add, key, art, chain, label, intro, group, unit)
        flush_pending()
    return chunks


def _par_text(u: Unit) -> str:
    n = u.number or ""
    label = n if n.startswith("§") else f"{n}."
    return f"{label} {render_unit(u).lstrip()}"


def _point_text(p: Unit) -> str:
    return f"{p.number}) {render_unit(p).lstrip()}"


def _add_group(add, key, art, chain, label, intro, group, unit) -> None:  # type: ignore[no-untyped-def]
    first, last = group[0].number, group[-1].number
    plabel = f"{label} pkt {first}" if first == last else f"{label} pkt {first}–{last}"
    body = "\n".join([intro, *(_point_text(p) for p in group)])
    if unit.tail and group[-1] is [c for c in unit.children if not c.repealed][-1]:
        body += "\n" + unit.tail
    covers = [address(key, chain)] + [a for p in group for a in _covers(key, (*chain, p))]
    add(art, (*chain, group[0]), plabel, body, covers)


def fixed(act: Act, *, window: int = 400, overlap: int = 50) -> list[Chunk]:
    """Stałe okna tokenów na ciągłym tekście aktu; `covers` = jednostki, których tekst wpada w okno."""
    key = act.source.key
    words: list[str] = []
    owner: list[str] = []  # adres najgłębszej jednostki dla każdego słowa
    for loc in iter_units(act):
        if loc.unit.repealed:
            continue
        for w in (loc.unit.text + " " + loc.unit.tail).split():
            words.append(w)
            owner.append(loc.address)
    step_w = int(window / 1.6)
    ov_w = int(overlap / 1.6)
    chunks: list[Chunk] = []
    i = 0
    while i < len(words):
        j = min(len(words), i + step_w)
        covered = sorted(set(owner[i:j]), key=owner[i:j].index)
        # dodaj przodków: trafienie w ustęp liczy się, gdy okno zawiera którąkolwiek jego część
        full: list[str] = []
        for a in covered:
            parts = a.split(" ")
            for k in range(3, len(parts) + 1, 2):
                anc = " ".join(parts[:k])
                if anc not in full:
                    full.append(anc)
        art = covered[0].split(" ")[2] if covered else ""
        own: dict[str, int] = {}
        for a in owner[i:j]:
            own[a] = own.get(a, 0) + 1
        chunks.append(
            Chunk(
                id=f"{key}:win:{len(chunks)}",
                act=key,
                article=art,
                covers=full,
                header=ACT_LABEL.get(key, key),
                body=" ".join(words[i:j]),
                own_words=own,
            )
        )
        if j == len(words):
            break
        i = j - ov_w
    return chunks


def located_by_address(act: Act) -> dict[str, Located]:
    return {loc.address: loc for loc in iter_units(act)}
