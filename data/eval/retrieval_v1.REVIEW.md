# Przegląd zestawu wyszukiwania v1 (2026-10-23)

Zestaw: `data/eval/retrieval_v1.jsonl` (zamrożony), surowy wynik generatora: `retrieval_v1.raw.jsonl`,
log decyzji generatora i walidatora: `retrieval_v1.log.jsonl`, próbka do przeglądu: `retrieval_v1.review_sample.json`.

## Generowanie

- 400 wylosowanych przepisów (najwyżej 1 na artykuł), generator `claude-sonnet-5`, walidator `gpt-5.6-terra`
  (inna rodzina — D7), wersje potoczne `gpt-5.6-luna` (100) i `gemini-3.8-flash` (3).
- Wynik generatora: 365 ok, 17 pominiętych przez generator (przepis techniczny), 17 odrzuconych przez walidator,
  1 odrzucone filtrem przepisywania (po jednej próbie poprawki; 26 pytań przeszło dzięki poprawce).
- Najdłuższy ciąg słów wspólny z przepisem (`copied_run`): pytania wygenerowane — mediana 3, maks. 5;
  potoczne — mediana 2. Zestaw jest umiarkowanie „leksykalny” (sprzyja BM25 mniej niż kopie przepisów).
- Zużycie klucza RAG Lab (`…(RAG Lab key)`, statystyki proxy): ok. 580 tys. tok. wejścia / 90 tys. wyjścia (Claude),
  150 tys. / 19 tys. (GPT-terra), 30 tys. / 18 tys. (GPT-luna) — łącznie z nieudanym pierwszym przebiegiem.

Nieudany pierwszy przebieg (`data/eval/failed/`): Gemini 3.5/3.6 zwracały 429 „You exceeded your current quota”
(kwota Google wyczerpana) → 296 błędów walidatora; filtr 5 słów odrzucał zwykłe nazwy prawnicze
(np. „przychodów nieznajdujących pokrycia w ujawnionych źródłach”). Naprawione: walidator GPT, próg 6 słów +
jedna poprawka generatora z podaną frazą.

## Przegląd ręczny (próbka: 25 z 250 wygenerowanych = 10%, 21 z 103 potocznych = 20%)

Ocena: czy przepis źródłowy odpowiada na pytanie, czy pytanie jest jednoznaczne, czy wersja potoczna
zachowuje sens.

**Wygenerowane (25):** 24 poprawne. Uwagi:
- #10 VAT art. 151 ust. 2 — pytanie poprawne, ale o przepis przejściowy z 2005 r. (bez wartości dla użytkownika);
- #1 VAT art. 106ga ust. 2 — pytanie łączy dwie rzeczy (podatnik zagraniczny + inne wyjątki); oba w tym ustępie, OK;
- #21 VAT art. 28l — pytanie o „usługi prawnicze dla osoby prywatnej spoza UE”; odpowiedź w tym przepisie, OK;
- #22 VAT art. 106ni ust. 4 — sprawdzone: ust. 4 obowiązuje dziś (tylko ust. 1–3 i 5–7 mają przypis
  „wejdzie w życie z dniem 1 stycznia 2027 r.”), OK.

**Potoczne (21):** 21 zachowuje sens i źródło. Uwagi:
- #27 PIT art. 35 ust. 1 — źródło to długi ustęp z 9 punktami; pytanie dotyczy pkt 9 (praktyka absolwencka).
  Wzorzec na poziomie ustępu jest poprawny, ale trafienie fragmentem „pkt 9” będzie liczone tylko, jeśli
  fragment zawiera ten ustęp — do uwzględnienia w metryce (trafienie = fragment ⊆ ustęp lub ustęp ⊆ fragment);
- #35 VAT art. 77 ust. 2 — „zwolnione z opłat” zamiast „zwolnione z VAT”: drobne rozmycie, sens zachowany;
- #42 VAT art. 146g ust. 1 — jak #10, przepis przejściowy (stawki 24%/9%/6% w latach przejściowych).

**Znalezisko systemowe 1 — przepisy przejściowe.** 58 z 353 pytań (16%) pochodziło z rozdziałów „przepisy
przejściowe / epizodyczne / końcowe”. Pierwsza poprawka (wyłączenie całych rozdziałów) była błędna: w tych
rozdziałach są też przepisy obowiązujące dziś — m.in. **VAT art. 146ef, podstawa obecnych stawek 23% i 8%**
(art. 41 ust. 1 nadal mówi „22%”). Wycięcie rozdziału usunęłoby z zestawu najczęstsze pytanie użytkowników.

Rozwiązanie: etykieta czasowa per artykuł (`raglab.annotate_temporal`, GPT, temp. 0, z uzasadnieniem) →
`data/annotations/temporal.jsonl` (150 artykułów) + **ręczne poprawki** `temporal_overrides.jsonl` (23 wpisy).
Model mylił się w ~15% przypadków, w tym w najważniejszym: art. 146ef oznaczył jako „conditional”
(warunek wydatków obronnych > 3% PKB; koniec okresu ogłasza minister — takiego obwieszczenia nie znaleziono),
a w art. 145f–145k podał nieistniejące daty końca okresu („28 lutego 2025 r.” zamiast 31 grudnia 2026 r. z art. 145e).
Z zestawu odpadają tylko pytania z przepisów `historical`.

**Znalezisko systemowe 2 — odesłania.** Generator widział tylko przepis źródłowy, więc przy odesłaniach
(„o których mowa w art. 145e ust. 1”) zgadywał kontekst — np. art. 145i (zawiadomienie przy odwrotnym obciążeniu
gazu i energii) dostał pytanie o „zawiadomienie przed wdrożeniem KSeF”. Rozwiązanie: `raglab.refs` rozwiązuje
odesłania wewnątrz aktu; generator i walidator dostają treść przepisów, do których źródło odsyła;
`raglab.evalsets.recheck` sprawdził cały zestaw: 184 z 305 pytań ma odesłania, **55 pytań (42 przepisy) miało zły
lub zbyt szeroki kontekst**. Te przepisy wygenerowano od nowa z odesłaniami i sprawdzono ponownie: 42 z 57 nowych
pytań przeszło, 15 (14 przepisów, głównie Ordynacja — klauzula GAAR, STIR) odrzucono.

Przy okazji znaleziony błąd ingestu: tytuł „DZIAŁ XIII …” w VAT gubiony, bo linia tytułu zaczynała się
niepogrubioną spacją → poprawione (pogrubienie z pierwszego niepustego spanu) + test.

## Zestaw v1 — wersja zamrożona

| akt | wygenerowane | potoczne |
|---|---|---|
| VAT | 85 | 37 |
| PIT | 58 | 20 |
| Ordynacja | 64 | 19 |
| razem | 207 | 76 |

Łącznie **283 pytania**, 207 unikalnych przepisów źródłowych. Pytania wygenerowane ponownie mają pole
`regenerated: "context_recheck"`.

Ograniczenia (do README): (1) jeden przepis źródłowy — trafienie w inny poprawny przepis liczy się jako pudło;
(2) pytania pisał model, który widział przepis, więc są bliżej słownictwa ustawy niż pytania ludzi — dlatego
warstwa potoczna raportowana osobno; (3) PIT ma mniej pytań niż zakładano (58 z 80), Ordynacja 64 z 70 — uzupełnić w v2, jeśli przedziały ufności
będą za szerokie; (4) walidator kontekstu to ten sam model co walidator pytań (GPT) — jego błędy są skorelowane.
