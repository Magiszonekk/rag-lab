"""Rozwiązywanie odwołań wewnątrz aktu: „o której mowa w art. 145e ust. 1” → treść tej jednostki.

Przegląd zestawu v1 pokazał, że model widzący tylko jeden przepis wymyśla kontekst odesłania
(art. 145i VAT o zawiadomieniu przy odwrotnym obciążeniu gazu → pytanie o „zawiadomienie przed KSeF”).
Ten sam mechanizm będzie potrzebny wariantowi agentowemu (koncept, sekcja 3: rozwijanie odwołań).

Heurystyka: odwołania do INNYCH aktów („art. 5 ustawy z dnia …”, „art. 13a Ordynacji podatkowej”,
„rozporządzenia 282/2011”) są pomijane; „ust. N” bez numeru artykułu odnosi się do bieżącego artykułu.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from raglab.corpus import Located, iter_units
from raglab.models import Act

_ART = r"\d+[a-ząćęłńóśźż]*"
_SUB = r"\d+[a-ząćęłńóśźż]*"
RE_REF = re.compile(
    rf"\bart\.\s*(?P<art>{_ART})"
    rf"(?:\s+(?:ust\.|§)\s*(?P<par>{_SUB}))?"
    rf"(?:\s+pkt\s*(?P<pt>{_SUB}))?"
)
RE_LOCAL_PAR = re.compile(rf"(?<!art\.\s)\b(?:ust\.|§)\s*(?P<par>{_SUB})(?:\s+pkt\s*(?P<pt>{_SUB}))?")
_OTHER_ACT = re.compile(
    r"^\s*(?:i\s+\d+\s*)?(?:ustawy\s+(?:z\s+dnia|o\s|–|-)|ustawy\s+wymienionej|Ordynacji|Kodeksu|rozporządzenia|dyrektywy|"
    r"Traktatu|ustawy\s+zmienianej|tej\s+ustawy|ustawy,\s+o\s+której)",
    re.I,
)


@dataclass(frozen=True)
class Ref:
    article: str
    paragraph: str | None
    point: str | None

    def label(self) -> str:
        parts = [f"art. {self.article}"]
        if self.paragraph:
            parts.append(self.paragraph if self.paragraph.startswith("§") else f"ust. {self.paragraph}")
        if self.point:
            parts.append(f"pkt {self.point}")
        return " ".join(parts)


def find_refs(text: str, current_article: str, *, uses_paragraph_sign: bool = False) -> list[Ref]:
    refs: list[Ref] = []
    for m in RE_REF.finditer(text):
        if _OTHER_ACT.match(text[m.end() : m.end() + 60]):
            continue
        par = m.group("par")
        if par and uses_paragraph_sign:
            par = f"§ {par}"
        refs.append(Ref(m.group("art"), par, m.group("pt")))
    stripped = RE_REF.sub(" ", text)
    for m in RE_LOCAL_PAR.finditer(stripped):
        par = m.group("par")
        if uses_paragraph_sign or m.group(0).startswith("§"):
            par = f"§ {par}"
        refs.append(Ref(current_article, par, m.group("pt")))
    seen: set[Ref] = set()
    out = []
    for r in refs:
        if r not in seen:
            seen.add(r)
            out.append(r)
    return out


class Resolver:
    def __init__(self, act: Act) -> None:
        self.act = act
        self.index: dict[str, Located] = {}
        for loc in iter_units(act):
            self.index[loc.address] = loc
        self.paragraph_sign = any(u.number and u.number.startswith("§") for a in act.articles[:50] for u in a.children)

    def resolve(self, ref: Ref) -> Located | None:
        from raglab.corpus import ACT_LABEL

        base = f"{ACT_LABEL.get(self.act.source.key, self.act.source.key)} {ref.label()}"
        for candidate in (base, base.rsplit(" pkt ", 1)[0], base.split(" ust. ")[0].split(" § ")[0]):
            if candidate in self.index:
                return self.index[candidate]
        return None

    def context_for(self, loc: Located, *, max_refs: int = 4, max_chars: int = 1500) -> list[tuple[str, str]]:
        """(adres, treść) jednostek, do których odsyła `loc`, bez niej samej i jej przodków."""
        own = {loc.address, *(Located(loc.act, loc.article, loc.chain[:i]).address for i in range(1, len(loc.chain)))}
        out: list[tuple[str, str]] = []
        for ref in find_refs(loc.full_text(), loc.article.number or "", uses_paragraph_sign=self.paragraph_sign):
            target = self.resolve(ref)
            if target is None or target.address in own or any(a == target.address for a, _ in out):
                continue
            out.append((target.address, target.full_text()[:max_chars]))
            if len(out) >= max_refs:
                break
        return out
