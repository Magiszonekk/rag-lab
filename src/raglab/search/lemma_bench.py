"""Test lematyzatorów na słownictwie z ustaw podatkowych (koncept D4: wybór spaCy vs Morfeusz 2).

Mierzymy dwie rzeczy, które mają znaczenie dla BM25:
1. dokładność lematu na ręcznie przygotowanej liście form prawniczych (oczekiwany lemat),
2. spójność: czy różne formy tego samego słowa dają TEN SAM lemat (to decyduje o trafieniu w BM25,
   nawet jeśli sam lemat nie jest „słownikowy”),
oraz czas lematyzacji całego korpusu.

    uv sync --group bench
    uv pip install https://github.com/explosion/spacy-models/releases/download/pl_core_news_md-3.8.0/pl_core_news_md-3.8.0-py3-none-any.whl
    uv run python -m raglab.search.lemma_bench

Wynik 2026-10-23 (data/eval/lemma_bench.json): Morfeusz 2 z regułami wyboru interpretacji — 70/70 form,
10/10 grup spójnych (22/22 na grupach spoza strojenia), 1 s na korpus; spaCy pl_core_news_md — 62/70,
4/10 grup, 80 s. Wybrany: Morfeusz 2 (D4).
"""

from __future__ import annotations

import json
import time

from raglab.corpus import iter_units, load_corpus
from raglab.ingest.sources import REPO_ROOT
from raglab.search.normalize import MorfeuszLemmatizer, SpacyLemmatizer, corpus_surface_freq, tokenize

# forma → oczekiwany lemat (formy wzięte z tekstu ustaw). Imiesłowy (naliczonego, rejestrujących) akceptują
# lemat czasownika albo przymiotnika — dla BM25 liczy się spójność, nie wybór konwencji.
ALT = {"naliczonego": {"naliczyć"}, "rejestrujących": {"rejestrować"}}
GOLD: dict[str, str] = {
    "podatnikowi": "podatnik",
    "podatników": "podatnik",
    "podatnikami": "podatnik",
    "faktur": "faktura",
    "fakturze": "faktura",
    "fakturę": "faktura",
    "zwolnienia": "zwolnienie",
    "zwolnieniu": "zwolnienie",
    "nabyciu": "nabycie",
    "nabycia": "nabycie",
    "wewnątrzwspólnotowej": "wewnątrzwspólnotowy",
    "wewnątrzwspólnotowego": "wewnątrzwspólnotowy",
    "odliczenia": "odliczenie",
    "naliczonego": "naliczony",
    "należnego": "należny",
    "opodatkowania": "opodatkowanie",
    "opodatkowaniu": "opodatkowanie",
    "deklaracji": "deklaracja",
    "zaliczek": "zaliczka",
    "zaliczki": "zaliczka",
    "przedawnienia": "przedawnienie",
    "nadpłaty": "nadpłata",
    "nadpłatę": "nadpłata",
    "zobowiązania": "zobowiązanie",
    "płatnika": "płatnik",
    "płatnicy": "płatnik",
    "przychodów": "przychód",
    "przychodu": "przychód",
    "kosztów": "koszt",
    "amortyzacyjnych": "amortyzacyjny",
    "środków": "środek",
    "trwałych": "trwały",
    "leasingu": "leasing",
    "darowizn": "darowizna",
    "stawką": "stawka",
    "stawki": "stawka",
    "towarów": "towar",
    "usług": "usługa",
    "dostawy": "dostawa",
    "dostawę": "dostawa",
    "eksportu": "eksport",
    "importu": "import",
    "zeznania": "zeznanie",
    "zeznaniu": "zeznanie",
    "urzędu": "urząd",
    "skarbowego": "skarbowy",
    "organu": "organ",
    "postępowania": "postępowanie",
    "odwołania": "odwołanie",
    "interpretacji": "interpretacja",
    "pełnomocnika": "pełnomocnik",
    "wierzytelności": "wierzytelność",
    "nieściągalności": "nieściągalność",
    "samochodowymi": "samochodowy",
    "pojazdów": "pojazd",
    "ewidencji": "ewidencja",
    "rejestrujących": "rejestrujący",
    "kasach": "kasa",
    "obrotu": "obrót",
    "sprzedaży": "sprzedaż",
    "budynków": "budynek",
    "lokali": "lokal",
    "mieszkalnych": "mieszkalny",
    "spadku": "spadek",
    "wspólnika": "wspólnik",
    "spółki": "spółka",
    "dochodów": "dochód",
    "dochodu": "dochód",
    "ulgi": "ulga",
    "odsetek": "odsetki",
}

# grupy form, które w BM25 muszą trafić w ten sam lemat
GROUPS: list[list[str]] = [
    ["podatnik", "podatnika", "podatnikowi", "podatnikiem", "podatników", "podatnikami"],
    ["faktura", "faktury", "fakturę", "fakturze", "fakturą", "faktur"],
    ["zwolnienie", "zwolnienia", "zwolnieniu", "zwolnieniem"],
    ["nadpłata", "nadpłaty", "nadpłatę", "nadpłacie"],
    ["przychód", "przychodu", "przychodów", "przychodem", "przychody"],
    ["odliczenie", "odliczenia", "odliczeniu", "odliczeniem"],
    ["zeznanie", "zeznania", "zeznaniu", "zeznaniem"],
    ["wierzytelność", "wierzytelności", "wierzytelnością"],
    ["samochód", "samochodu", "samochodem", "samochody", "samochodów"],
    ["mieszkanie", "mieszkania", "mieszkaniu", "mieszkaniem"],
]


def main() -> int:
    corpus = load_corpus()
    texts = [" ".join(u.text for u in loc.chain[-1:]) for act in corpus.values() for loc in iter_units(act)]
    results: dict[str, dict[str, object]] = {}
    for lem in (MorfeuszLemmatizer(corpus_surface_freq()), SpacyLemmatizer()):
        name = lem.name
        ok = {f: lem.lemma(f) == g or lem.lemma(f) in ALT.get(f, set()) for f, g in GOLD.items()}
        acc = list(ok.values())
        errors = {f: lem.lemma(f) for f in GOLD if not ok[f]}
        consistent = 0
        split_groups = {}
        for grp in GROUPS:
            lemmas = {lem.lemma(f) for f in grp}
            if len(lemmas) == 1:
                consistent += 1
            else:
                split_groups[grp[0]] = sorted(lemmas)
        t0 = time.monotonic()
        n_tok = 0
        for t in texts:
            n_tok += len(lem.lemmas(tokenize(t)))
        dt = time.monotonic() - t0
        results[name] = {
            "version": lem.version,
            "gold_accuracy": round(sum(acc) / len(acc), 3),
            "gold_n": len(acc),
            "gold_errors": errors,
            "groups_consistent": f"{consistent}/{len(GROUPS)}",
            "split_groups": split_groups,
            "corpus_tokens": n_tok,
            "corpus_seconds": round(dt, 1),
        }
        print(name, json.dumps({k: v for k, v in results[name].items() if k != "gold_errors"}, ensure_ascii=False))
        print("   błędy:", errors)
    out = REPO_ROOT / "data" / "eval" / "lemma_bench.json"
    out.write_text(json.dumps(results, ensure_ascii=False, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
