"""Złoży złoty zestaw v1 z wersji roboczych (subagenci) + poprawek z przeglądu ręcznego.

Każda poprawka ma uzasadnienie w GOLDEN_v1.REVIEW.md. Skrypt jest deterministyczny i wersjonowany,
żeby było widać różnicę między szkicem a zestawem zamrożonym.

    uv run python -m raglab.evalsets.golden_build
"""

from __future__ import annotations

import json
import re
import sys
from typing import Any

from raglab.annotate_temporal import load_labels
from raglab.corpus import iter_units, load_corpus
from raglab.ingest.sources import REPO_ROOT

GOLDEN = REPO_ROOT / "data" / "eval" / "golden"
DRAFTS = ["draft_vat", "draft_pit_op", "draft_ooc"]
STATE = {"vat": "2026-08-26", "pit": "2026-04-01", "op": "2026-04-21"}

# --- poprawki z przeglądu (id → zmiany pól) -------------------------------------------------------
PATCH: dict[str, dict[str, Any] | None] = {
    # art. 41 ust. 1 też jest poprawnym miejscem dla wyszukiwania (stawka podstawowa), ale wzorzec liczbowy to 23%
    # z art. 146ef; system, który zacytuje tylko art. 41 i poda 22%, oblewa key_facts — i o to chodzi.
    "g-vat-01": {
        "answers": ["VAT art. 146ef ust. 1", "VAT art. 41 ust. 1"],
        "required_all": False,
        "notes": "Pułapka: art. 41 ust. 1 mówi 22%; obowiązujące 23% wynika z art. 146ef ust. 1 pkt 1. "
        "Trafienie w art. 41 liczy się w wyszukiwaniu, ale odpowiedź z 22% jest błędna (key_facts).",
    },
    # pytanie o „wybrany samochód osobowy” bez kontekstu użycia — dodane, że chodzi o użytek mieszany
    "g-vat-07": {
        "question": "Jaki procent VAT z faktury za wydatki związane z samochodem osobowym używanym zarówno "
        "w firmie, jak i prywatnie można co do zasady odliczyć?",
        "answers": ["VAT art. 86a ust. 1", "VAT art. 86a ust. 3 pkt 1"],
        "required_all": False,
    },
    # „bez limitu dochodu” — w ust. 2 pkt 2 rzeczywiście brak limitu dochodu; zostawione, ale pytanie było podwójne
    # i mieszało dwie instytucje; wzorzec doprecyzowany o art. 6 ust. 4d (sposób liczenia).
    "g-pit-12": {
        "answers": ["PIT art. 27f ust. 2 pkt 2", "PIT art. 6 ust. 4c", "PIT art. 6 ust. 4d"],
        "reference_answer": "Na dwoje małoletnich dzieci odliczeniu podlega 92,67 zł na każde dziecko za każdy "
        "miesiąc sprawowania opieki; dla dwojga dzieci ustawa nie przewiduje limitu dochodu. Rodzic samotnie "
        "wychowujący małoletnie dzieci (m.in. panna, kawaler, wdowa, wdowiec, rozwódka, rozwodnik) może na wniosek "
        "w zeznaniu rocznym określić podatek w podwójnej wysokości podatku obliczonego od połowy swoich dochodów.",
    },
    # pkt 1 lit. a („kurs językowy”-podobne) — nie; tu: korekta przy środku trwałym — art. 91 ust. 7 jest przepisem,
    # który faktycznie stosuje korektę do sytuacji „miał prawo do pełnego odliczenia, potem prawo się zmieniło”.
    "g-vat-18": {
        "answers": ["VAT art. 91 ust. 7", "VAT art. 91 ust. 2"],
        "required_all": True,
        "reference_answer": "Tak. Gdy podatnik odliczył cały VAT, a potem zmieniło się prawo do odliczenia "
        "(część wykorzystania to czynności zwolnione), stosuje się odpowiednio przepisy o korekcie (art. 91 ust. 7). "
        "Dla środka trwałego o wartości początkowej powyżej 15 000 zł korekty dokonuje się w ciągu 5 kolejnych lat, "
        "licząc od roku oddania do użytkowania; roczna korekta dotyczy jednej piątej kwoty podatku naliczonego "
        "przy nabyciu (art. 91 ust. 2).",
        "key_facts": ["5 kolejnych lat", "jednej piątej"],
    },
    # pełnomocnictwo — dwa pytania-bliźniaki (g-op-08 multi, g-op-11 colloquial); multi przerobione na inne odesłanie
    "g-op-08": None,  # usunięte (duplikat tematu g-op-11), zastąpione przez g-op-12 niżej
    # brak zapowiedzi zmiany limitu jest prawdą tylko o korpusie — wzorzec bez sugestii, że limit „się nie zmieni”
    "g-ooc-12": {"expected_behavior": "answer_with_date"},
    # stawki VAT w 2010: wzorzec powoływał się na nieistniejący „przepis przejściowy dotyczący lat 2016 (art. 146f)”
    "g-ooc-14": {
        "reference_answer": "W przepisach, które mam (ustawa o VAT, stan na 2026-08-26), nie ma stawek "
        "obowiązujących w 2010 roku — korpus zawiera tekst obecny, a przepisy przejściowe dotyczą innych okresów. "
        "Nie mogę podać historycznej stawki."
    },
    # laptop za 6000 zł: korpus ZAWIERA rozstrzygnięcie (PIT art. 22d ust. 1 — jednorazowo do 10 000 zł). Sytuacja
    # „individual_advice” była źle dobrana: system powinien tu odpowiedzieć. Przeniesione do kategorii multi.
    "g-ooc-15": {
        "category": "multi",
        "act": "pit",
        "situation": None,
        "expected_behavior": None,
        "question": "Prowadzę jednoosobową działalność i kupiłem laptopa do pracy za 6000 zł. Czy mogę cały "
        "wydatek wrzucić w koszty od razu, czy muszę go amortyzować?",
        "reference_answer": "Można zaliczyć wydatek od razu: podatnicy mogą nie dokonywać odpisów amortyzacyjnych "
        "od składników majątku o wartości początkowej nieprzekraczającej 10 000 zł — wydatki na ich nabycie "
        "stanowią wtedy koszty uzyskania przychodów w miesiącu oddania do używania (PIT art. 22d ust. 1). "
        "Laptop za 6000 zł mieści się w tym limicie.",
        "answers": ["PIT art. 22d ust. 1"],
        "required_all": False,
        "key_facts": ["10 000 zł"],
        "evidence": {
            "PIT art. 22d ust. 1": "których wartość początkowa, określona zgodnie z art. 22g, nie przekracza 10 000 zł"
        },
        "id_new": "g-pit-16",
    },
    # płatność kartą: Ordynacja art. 60–61 reguluje zapłatę „innym instrumentem płatniczym” (przez e-Urząd).
    # Część „czy kartą w urzędzie” jest więc częściowo w korpusie; wzorzec poprawiony.
    "g-ooc-19": {
        "answers": ["Ordynacja art. 56 § 1", "Ordynacja art. 61 § 1 pkt 2"],
        "reference_answer": "Stawka odsetek za zwłokę to suma 200% podstawowej stopy kredytu lombardowego NBP "
        "i 2%, nie mniej niż 8% (Ordynacja art. 56 § 1). Co do zapłaty kartą: Ordynacja dopuszcza zapłatę "
        "„innym instrumentem płatniczym” za pośrednictwem konta w e-Urzędzie Skarbowym (art. 61 § 1 pkt 2); "
        "zasad płacenia kartą bezpośrednio w kasie urzędu w korpusie nie ma.",
    },
    # sprzedaż laptopa prywatnie: art. 15 ust. 2 (definicja działalności) jest kluczowy obok ust. 1
    "g-ooc-18": {"answers": ["VAT art. 15 ust. 1", "VAT art. 15 ust. 2"]},
}

NEW: list[dict[str, Any]] = [
    {
        "id": "g-op-12",
        "act": "op",
        "category": "multi",
        "question": "Złożyłem korektę deklaracji i zapłaciłem zaległość, ale dopiero po tym, jak dostałem zawiadomienie "
        "o zamiarze wszczęcia kontroli. Czy przysługuje mi obniżona stawka odsetek za zwłokę?",
        "reference_answer": "Nie. Obniżona stawka odsetek (50% stawki odsetek za zwłokę) przysługuje przy korekcie "
        "złożonej w ciągu 6 miesięcy od terminu złożenia deklaracji i zapłacie zaległości w ciągu 7 dni "
        "od korekty (art. 56a § 1), ale nie stosuje się jej do korekty złożonej po doręczeniu "
        "zawiadomienia o zamiarze wszczęcia kontroli podatkowej (art. 56a § 3 pkt 1).",
        "answers": ["Ordynacja art. 56a § 1", "Ordynacja art. 56a § 3 pkt 1"],
        "required_all": True,
        "key_facts": ["50 %", "zawiadomienia o zamiarze wszczęcia kontroli"],
        "evidence": {
            "Ordynacja art. 56a § 1": "Obniżoną stawkę odsetek za zwłokę w wysokości 50 % stawki odsetek za zwłokę "
            "stosuje się w przypadku spełnienia łącznie następujących warunków",
            "Ordynacja art. 56a § 3 pkt 1": "złożonej po doręczeniu zawiadomienia o zamiarze wszczęcia kontroli podatkowej",
        },
        "notes": "Dodane w przeglądzie zamiast g-op-08 (bliźniak g-op-11). Reguła + wyjątek.",
    },
]


def _norm(s: str) -> str:
    s = s.replace("\u202f", " ").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", s).replace(" %", "%").strip().lower()


def main() -> int:
    corpus = load_corpus()
    index = {loc.address: loc for act in corpus.values() for loc in iter_units(act)}
    labels = load_labels()
    items: list[dict[str, Any]] = []
    for name in DRAFTS:
        for line in (GOLDEN / f"{name}.jsonl").read_text(encoding="utf-8").splitlines():
            if line.strip():
                items.append(json.loads(line))
    out: list[dict[str, Any]] = []
    for it in items:
        if it["id"] in PATCH:
            p = PATCH[it["id"]]
            if p is None:
                continue
            it = {**it, **{k: v for k, v in p.items() if k != "id_new"}}
            if "id_new" in p:
                it["id"] = p["id_new"]
            it["reviewed"] = "patched"
        else:
            it["reviewed"] = "accepted"
        out.append(it)
    out.extend({**n, "reviewed": "added"} for n in NEW)

    errors: list[str] = []
    for it in out:
        it.setdefault("required_all", False)
        it["state_date"] = STATE.get(it.get("act") or "") if it.get("act") else None
        it["version"] = "golden_v1"
        for a in it.get("answers", []):
            loc = index.get(a)
            if loc is None:
                errors.append(f"{it['id']}: brak adresu {a}")
                continue
            if labels.get((loc.act, loc.article.number or "")) == "historical":
                errors.append(f"{it['id']}: przepis historyczny {a}")
        if it["category"] != "out_of_corpus":
            texts = " ".join(_norm(index[a].full_text()) for a in it["answers"] if a in index)
            for kf in it.get("key_facts", []):
                if _norm(kf) not in texts and _norm(kf).replace(" ", "") not in texts.replace(" ", ""):
                    errors.append(f"{it['id']}: key_fact {kf!r} nie występuje w przepisach")
            for a, ev in (it.get("evidence") or {}).items():
                if a in index and _norm(ev) not in _norm(index[a].full_text()):
                    errors.append(f"{it['id']}: evidence dla {a} nie jest dosłownym cytatem")
    ids = [it["id"] for it in out]
    if len(ids) != len(set(ids)):
        errors.append("powtórzone id")
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    path = GOLDEN / "golden_v1.jsonl"
    path.write_text("".join(json.dumps(it, ensure_ascii=False) + "\n" for it in out), encoding="utf-8")
    from collections import Counter

    c = Counter((it.get("act") or "-", it["category"]) for it in out)
    print(len(out), dict(sorted(c.items())), file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
