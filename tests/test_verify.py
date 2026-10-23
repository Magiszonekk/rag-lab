"""Testy sprawdzania odpowiedzi (verify=cite) i przepisów zastępujących w kontekście."""

from raglab.rag.verify import Corpus, check_cite, key_facts_present, quantities


def test_quantities_normalize_units_and_spaces() -> None:
    q = quantities("stawka 23 % i 240 000 zł, pięciu lat, 3 lata, 15. dnia, 90 dni, 8,5 %, 12 proc.")
    assert {("23", "%"), ("240000", "zł"), ("5", "lat"), ("3", "lat"), ("15", "dzień"), ("90", "dni"),
            ("8.5", "%"), ("12", "%")} <= q  # fmt: skip


def test_quantities_ignore_years_and_word_prefixes() -> None:
    assert quantities("w 2026 roku; latarnia; 7 latach") == set()


def test_resolve_walks_up_to_existing_unit() -> None:
    c = Corpus.get()
    assert c.resolve("VAT art. 41 ust. 1") == "VAT art. 41 ust. 1"
    assert c.resolve("ustawa o VAT art. 146ef ust. 1 pkt 1") is not None
    assert c.resolve("VAT art. 99999") is None


def test_cite_flags_number_not_in_cited_provision() -> None:
    ctx = ["VAT art. 41 ust. 1", "VAT art. 146ef"]
    ok = check_cite("Stawka podstawowa wynosi 23%.", ["VAT art. 146ef"], ctx)
    assert ok.passed
    bad = check_cite("Stawka podstawowa wynosi 25%.", ["VAT art. 146ef"], ctx)
    assert not bad.passed and bad.unsupported_numbers == ["25 %"]


def test_cite_rejects_citation_outside_context() -> None:
    r = check_cite("Zwolnienie podmiotowe.", ["VAT art. 113 ust. 1"], ["VAT art. 41 ust. 1"])
    assert r.citations_valid == 0.0 and not r.passed


def test_cite_ignores_numbers_from_question() -> None:
    r = check_cite("Przy kwocie 6000 zł stosuje się przepis.", ["VAT art. 41 ust. 1"], ["VAT art. 41 ust. 1"],
                   question="Kupiłem laptop za 6000 zł")  # fmt: skip
    assert r.numbers_supported == 1.0


def test_key_facts_numbers_and_text() -> None:
    assert key_facts_present("Stawka wynosi 23 %, a obniżona 8%.", ["23%", "8 %"]) == 1.0
    assert key_facts_present("Termin wynosi pięć lat.", ["5 lat", "koniec roku kalendarzowego"]) == 0.5


def test_override_provision_added_for_replaced_rate() -> None:
    from raglab.rag.context import _overrides

    ov = _overrides()
    assert ov[("vat", "art. 41 ust. 1")] == ["146ef"]
    # art. 146ej (upoważnienie ministra) nie ustala wartości — nie może być „przepisem zastępującym”
    assert all("146ej" not in v for v in ov.values())


def test_resolve_compound_citations_to_parent() -> None:
    c = Corpus.get()
    assert c.resolve("VAT art. 106j ust. 2 pkt 3, 5 i 6") == "VAT art. 106j ust. 2"
    assert c.resolve("Ordynacja art. 81b § 1 pkt 1 i § 2") == "Ordynacja art. 81b"
    assert c.resolve("Ordynacja art. 53 § 1 i 3") == "Ordynacja art. 53"
