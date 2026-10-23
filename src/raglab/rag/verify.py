"""Deterministyczne sprawdzanie odpowiedzi — poziom `verify=cite` (koncept D5) i metryki D7 warstwa 1.

1. **cytaty**: każdy cytowany adres musi wskazywać jednostkę, która była w kontekście (albo jej część/przodka);
2. **liczby**: każda liczba z jednostką (%, zł, euro, dni, miesięcy, lat) z odpowiedzi musi występować w tekście
   cytowanych przepisów — po normalizacji („23 %” = „23%”, „240 000 zł” = „240000 zł”, „pięciu lat” = „5 lat”).

Ten sam moduł liczy `key_facts` złotego zestawu (D7: jeden normalizator, nie dwa).
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from raglab.corpus import iter_units, load_corpus

NUMWORDS = {
    "jeden": 1, "jednego": 1, "dwa": 2, "dwóch": 2, "trzy": 3, "trzech": 3, "cztery": 4, "czterech": 4,
    "pięć": 5, "pięciu": 5, "sześć": 6, "sześciu": 6, "siedem": 7, "siedmiu": 7, "dziesięć": 10, "dziesięciu": 10,
    "dwanaście": 12, "dwunastu": 12, "czternaście": 14, "czternastu": 14, "trzydzieści": 30, "trzydziestu": 30,
}  # fmt: skip
# „rok” celowo poza listą: „2026 roku” to data, nie okres; okresy w latach mają formę „5 lat” / „3 lata”
UNIT = r"(%|proc\.?|procent\w*|zł|złotych|euro|dni|dnia|miesięc\w*|miesiąc\w*|lat|lata)(?!\w)"
RE_QTY = re.compile(rf"(\d{{1,3}}(?:[ \u00a0\u202f]\d{{3}})+|\d+(?:[.,]\d+)?)\s*{UNIT}", re.I)
# „15. dnia miesiąca”, „25. dnia” — liczebnik porządkowy przed „dnia”
RE_ORD_DAY = re.compile(r"\b(\d{1,2})\.\s*dni(a|u)\b", re.I)
RE_WORDQTY = re.compile(rf"\b({'|'.join(NUMWORDS)})\s+{UNIT}", re.I)


def _unit(u: str) -> str:
    u = u.lower()
    if u.startswith(("%", "proc")):
        return "%"
    if u.startswith(("zł", "złot")):
        return "zł"
    if u.startswith("euro"):
        return "euro"
    if u.startswith("dni") or u.startswith("dnia"):
        return "dni"
    if u.startswith("miesi"):
        return "mies"
    return "lat"


def quantities(text: str) -> set[tuple[str, str]]:
    out: set[tuple[str, str]] = set()
    for m in RE_QTY.finditer(text):
        num = re.sub(r"[ \u00a0\u202f]", "", m.group(1)).replace(",", ".")
        num = num.rstrip("0").rstrip(".") if "." in num else num
        out.add((num, _unit(m.group(2))))
    for m in RE_ORD_DAY.finditer(text):
        out.add((m.group(1), "dzień"))
    for m in RE_WORDQTY.finditer(text):
        out.add((str(NUMWORDS[m.group(1).lower()]), _unit(m.group(2))))
    return out


def norm_text(s: str) -> str:
    s = s.replace("\u202f", " ").replace("\u00a0", " ")
    s = re.sub(r"(\d)\s+(?=\d{3}\b)", r"\1", s)  # 240 000 → 240000
    return re.sub(r"\s+", " ", s).replace(" %", "%").strip().lower()


class Corpus:
    _inst: Corpus | None = None

    def __init__(self) -> None:
        self.text: dict[str, str] = {}
        for act in load_corpus().values():
            for loc in iter_units(act):
                self.text[loc.address] = loc.full_text()

    @classmethod
    def get(cls) -> Corpus:
        if cls._inst is None:
            cls._inst = cls()
        return cls._inst

    def resolve(self, addr: str) -> str | None:
        a = re.sub(r"\s+", " ", addr.replace("\u202f", " ")).strip().rstrip(".")
        a = re.sub(r"^(Ustawa o |ustawa o )", "", a)
        a = a.replace("Ordynacji podatkowej", "Ordynacja").replace("Ordynacja podatkowa", "Ordynacja")
        # cytat złożony: „art. 106j ust. 2 pkt 3, 5 i 6”, „art. 81b § 1 pkt 1 i § 2”, „art. 53 § 1 i 3” →
        # jednostka nadrzędna listy („art. 106j ust. 2”, „art. 81b”, „art. 53”)
        m = re.match(r"^(.*?)(?:,| i | oraz )", a)
        if m and re.search(r"\d", a[m.end() :]):
            head, rest = m.group(1), a[m.end() :]
            kw = re.match(r"\s*(§|ust\.|pkt|lit\.)", rest)
            if kw and f" {kw.group(1)} " in head:  # „… § 1 pkt 1 i § 2” → wspólny rodzic powyżej poziomu „§”
                a = head[: head.index(f" {kw.group(1)} ")]
            else:  # „… pkt 3, 5 i 6” → rodzic ostatniego poziomu
                a = re.sub(r" (ust\.|pkt|lit\.|§) [^ ]+$", "", head)
        while a:
            if a in self.text:
                return a
            if " " not in a:
                return None
            a = a.rsplit(" ", 2)[0] if re.search(r" (ust\.|pkt|lit\.|§) \S+$", a) else ""
        return None


@dataclass
class CiteCheck:
    citations_valid: float  # odsetek cytatów wskazujących jednostkę z kontekstu
    numbers_supported: float  # odsetek liczb z odpowiedzi występujących w cytowanych przepisach
    unsupported_numbers: list[str] = field(default_factory=list)
    invalid_citations: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return self.citations_valid == 1.0 and self.numbers_supported == 1.0


def _in_context(addr: str, context_units: set[str]) -> bool:
    return any(addr == u or u.startswith(addr + " ") or addr.startswith(u + " ") for u in context_units)


def check_cite(answer: str, citations: list[str], context_addresses: list[str], question: str = "") -> CiteCheck:
    corpus = Corpus.get()
    ctx_units: set[str] = set()
    for a in context_addresses:
        r = corpus.resolve(a.split(" pkt ")[0] if "–" in a else a) or corpus.resolve(a.split("–")[0])
        if r:
            ctx_units.add(r)
    valid, invalid = 0, []
    cited_text = ""
    for c in citations:
        r = corpus.resolve(c)
        if r and _in_context(r, ctx_units):
            valid += 1
            cited_text += " " + corpus.text[r]
        else:
            invalid.append(c)
    # liczby podane przez użytkownika w pytaniu (np. „laptop za 6000 zł”) nie muszą mieć źródła w przepisach
    qs = quantities(answer) - quantities(question)
    have = quantities(cited_text)
    unsupported = sorted(f"{n} {u}" for n, u in qs if (n, u) not in have)
    return CiteCheck(
        citations_valid=valid / len(citations) if citations else 0.0,
        numbers_supported=(len(qs) - len(unsupported)) / len(qs) if qs else 1.0,
        unsupported_numbers=unsupported,
        invalid_citations=invalid,
    )


def key_facts_present(answer: str, key_facts: list[str]) -> float:
    """Odsetek kluczowych faktów obecnych w odpowiedzi.

    Liczby porównywane jako (wartość, jednostka), reszta tekstowo.
    """
    if not key_facts:
        return 1.0
    a_norm = norm_text(answer)
    a_q = quantities(answer)
    hit = 0
    for kf in key_facts:
        kq = quantities(kf)
        if (kq and kq <= a_q) or norm_text(kf) in a_norm:
            hit += 1
    return hit / len(key_facts)


def citation_recall(citations: list[str], gold: list[str], required_all: bool) -> float:
    """Czy odpowiedź cytuje przepisy wzorcowe (adres albo jego część / przodek na poziomie ustępu)."""
    if not gold:
        return 1.0
    corpus = Corpus.get()
    res = [corpus.resolve(c) for c in citations]

    def ok(g: str) -> bool:
        return any(r and (r == g or g.startswith(r + " ") or r.startswith(g + " ")) for r in res)

    hits = [ok(g) for g in gold]
    return sum(hits) / len(gold) if required_all else float(any(hits))
