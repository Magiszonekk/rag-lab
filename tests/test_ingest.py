"""Testy ingestu — warunek ukończenia etapu 1 (koncept D2).

Testy działają na prawdziwych PDF-ach z API Sejmu (zamrożonych po sha256 w data/sources.toml).
Wartości oczekiwane sprawdzone ręcznie z tekstem ustawy.
"""

from __future__ import annotations

from datetime import date

import pytest

from raglab.ingest import build_act
from raglab.ingest.pdf_lines import join_lines
from raglab.ingest.sources import get_source
from raglab.models import Act


@pytest.fixture(scope="session")
def acts() -> dict[str, Act]:
    return {k: build_act(get_source(k)) for k in ("vat", "pit", "op")}


@pytest.fixture(scope="session")
def vat(acts: dict[str, Act]) -> Act:
    return acts["vat"]


# --- metadane aktu (D1) -------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("key", "act_date", "state_date"),
    [
        ("vat", date(2004, 3, 11), date(2026, 8, 26)),
        ("pit", date(1991, 7, 26), date(2026, 4, 1)),
        ("op", date(1997, 8, 29), date(2026, 4, 21)),
    ],
)
def test_daty_aktu_i_stanu_prawnego(acts: dict[str, Act], key: str, act_date: date, state_date: date) -> None:
    assert acts[key].act_date == act_date
    assert acts[key].state_date == state_date


# --- przypisy (D2) ------------------------------------------------------------------------------


@pytest.mark.parametrize("key", ["vat", "pit", "op"])
def test_liczba_przypisow_zgadza_sie_z_najwyzszym_numerem(acts: dict[str, Act], key: str) -> None:
    notes = acts[key].footnotes
    assert sorted(notes) == list(range(1, max(notes) + 1))


def test_art2_vat_przypis_w_srodku_nie_psuje_numeracji_punktow(vat: Act) -> None:
    art = vat.article("2")
    numbers = [p.number for p in art.children]
    # przypis „1) Zmiany wymienionej umowy…” na dole s. 5 nie może stać się punktem 1
    assert numbers.count("1") == 1
    assert art.child("1").text.startswith("terytorium kraju – rozumie się przez to terytorium Rzeczypospolitej")
    assert "Zmiany wymienionej umowy" not in " ".join(p.text for p in art.walk())
    # znacznik przypisu „zm.1))” usunięty z treści, numer przypisu przy punkcie
    assert art.child("2").text.endswith("z późn. zm.);")
    assert art.child("2").footnote_refs == [1]
    assert vat.footnotes[1].startswith("Zmiany wymienionej umowy zostały ogłoszone")
    assert numbers[:7] == ["1", "2", "3", "4", "5", "5a", "6"]


@pytest.mark.parametrize("key", ["vat", "pit", "op"])
def test_brak_naglowkow_stron_w_tresci(acts: dict[str, Act], key: str) -> None:
    for art in acts[key].articles:
        for u in art.walk():
            assert "Dziennik Ustaw" not in u.text, (art.number, u.number)


# --- struktura (D2) -----------------------------------------------------------------------------


def test_art2_vat_definicje_i_czesc_wspolna(vat: Act) -> None:
    art = vat.article("2")
    assert art.text == "Ilekroć w dalszych przepisach jest mowa o:"
    assert len(art.children) == 69
    pkt8 = art.child("8")
    assert [lit.number for lit in pkt8.children] == ["a", "b"]
    assert pkt8.tail.startswith("– jeżeli wywóz towarów poza terytorium Unii Europejskiej")
    assert art.child("3").child("c").repealed


def test_art43_vat_dlugi_wielopoziomowy(vat: Act) -> None:
    art = vat.article("43")
    ust1 = art.child("1")
    assert ust1.text == "Zwalnia się od podatku:"
    assert len(ust1.children) == 46
    assert ust1.child("18").text.startswith("usługi w zakresie opieki medycznej, służące profilaktyce")
    assert art.path == ["DZIAŁ VIII Wysokość opodatkowania", "Rozdział 2 Zwolnienia"]


def test_art86_vat(vat: Act) -> None:
    art = vat.article("86")
    assert art.path == [
        "DZIAŁ IX Odliczenie i zwrot podatku. Odliczanie częściowe",
        "Rozdział 1 Odliczenie i zwrot podatku",
    ]
    assert art.child("1").text.startswith("W zakresie, w jakim towary i usługi są wykorzystywane do wykonywania")
    ust2 = art.child("2")
    assert ust2.text == "Kwotę podatku naliczonego stanowi:"
    assert [lit.number for lit in ust2.child("2").children] == ["a", "b", "c", "d"]
    assert ust2.child("5").repealed


def test_artykul_i_ustep_z_litera(vat: Act) -> None:
    assert [u.number for u in vat.article("2a").children] == ["1", "2", "3"]
    art86 = vat.article("86")
    assert art86.child("2a").text.startswith("W przypadku nabycia towarów i usług wykorzystywanych zarówno")
    assert [u.number for u in art86.children][:4] == ["1", "2", "2a", "2b"]


def test_artykuly_uchylone_i_pominiete(vat: Act) -> None:
    assert vat.article("12a").repealed
    assert vat.article("139–145").repealed  # „Art. 139–145. (pominięte)”


def test_numer_artykulu_z_polska_litera(acts: dict[str, Act]) -> None:
    pit = acts["pit"]
    assert pit.article("22ł").child("1").text.startswith("Od środków trwałych oraz wartości niematerialnych")
    assert pit.article("22l").child("4").text.startswith("Odpisów amortyzacyjnych od przyjętego do używania")


def test_pit_art45_termin_zeznania(acts: dict[str, Act]) -> None:
    text = acts["pit"].article("45").child("1").text
    assert "w terminie od dnia 15 lutego do dnia 30 kwietnia roku następującego po roku podatkowym" in text


def test_ordynacja_paragrafy(acts: dict[str, Act]) -> None:
    art = acts["op"].article("21")
    assert [u.number for u in art.children] == [
        "§ 1",
        "§ 2",
        "§ 3",
        "§ 3a",
        "§ 4",
        "§ 5",
    ]
    par1 = art.child("1")
    assert par1.text == "Zobowiązanie podatkowe powstaje z dniem:"
    assert [p.number for p in par1.children] == ["1", "2"]
    assert acts["op"].article("70").path == [
        "DZIAŁ III Zobowiązania podatkowe",
        "Rozdział 8 Przedawnienie",
    ]


@pytest.mark.parametrize("key", ["vat", "pit", "op"])
def test_numeracja_artykulow_rosnaca_bez_duplikatow(acts: dict[str, Act], key: str) -> None:
    numbers = [a.number for a in acts[key].articles]
    assert len(numbers) == len(set(numbers))


# --- wersje jednostek (D1) ----------------------------------------------------------------------


def test_jednostka_dwuwersyjna_art99_ust12_vat(vat: Act) -> None:
    versions = [u for u in vat.article("99").children if u.number == "12"]
    assert [u.version for u in versions] == ["until_change", "future"]
    assert versions[1].effective_from == date(2026, 10, 1)
    assert vat.article("99").child("12") is versions[0]  # domyślnie brzmienie obowiązujące w stanie korpusu


# --- załączniki i tabele (D2) -------------------------------------------------------------------


def test_zalaczniki_vat(vat: Act) -> None:
    assert len(vat.annexes) == 15
    assert vat.annex("1").repealed
    assert not vat.annex("6").repealed  # „Załącznik nr 640)” = zał. 6 + przypis 40


def test_zal3_vat_wiersz_tabeli(vat: Act) -> None:
    z3 = vat.annex("3")
    assert z3.title.startswith("WYKAZ TOWARÓW I USŁUG OPODATKOWANYCH STAWKĄ PODATKU")
    rows = {r.position: r for r in z3.rows}
    assert len(z3.rows) == 76
    assert {"10a", "10b", "10c"} <= set(rows)
    r12 = rows["12"]
    assert r12.cells == {
        "CN lub PKWiU": "bez względu na CN",
        "Nazwa towaru lub usługi (grupy towarów lub usług)": "Ziemia ogrodnicza",
    }
    assert r12.section == "Towary zwykle używane w rolnictwie"
    assert rows["1"].cells["CN lub PKWiU"] == "ex 09"
    assert rows["1"].section == "Towary spożywcze"


def test_zalaczniki_nie_doklejone_do_ostatniego_artykulu(vat: Act) -> None:
    last = vat.article("176")
    assert "WYKAZ TOWARÓW" not in " ".join(u.text for u in last.walk())


# --- funkcje pomocnicze -------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("a", "b", "out"),
    [
        ("terytorium Unii Euro-", "pejskiej;", "terytorium Unii Europejskiej;"),
        ("Państw-", "-Stron", "Państw-Stron"),
        ("Dz. U. z 2025 r.", "poz. 163", "Dz. U. z 2025 r. poz. 163"),
        ("art. 2 –", "zdanie", "art. 2 – zdanie"),
    ],
)
def test_join_lines(a: str, b: str, out: str) -> None:
    assert join_lines(a, b) == out
