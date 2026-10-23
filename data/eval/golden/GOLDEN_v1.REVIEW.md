# Przegląd złotego zestawu v1 (2026-10-23)

Zestaw: `data/eval/golden/golden_v1.jsonl` (zamrożony), budowany deterministycznie skryptem
`raglab.evalsets.golden_build` ze szkiców `draft_*.jsonl` + poprawek z tego przeglądu.

## Jak powstał

Właściciel nie zna prawa podatkowego, więc pytania przygotowały trzy subagenty (model z rodziny Claude),
równolegle, z narzędziem `raglab.lookup` do czytania korpusu i zakazem pisania z pamięci:
- VAT — 26 pytań (12 fakt, 8 łączących przepisy, 6 potocznych),
- PIT + Ordynacja — 26 pytań (14 / 7 / 5),
- spoza korpusu — 20 pytań w 5 sytuacjach z koncepcji D6a, każde z udokumentowanym sprawdzeniem
  (`absence_check`, wyszukiwania po wszystkich trzech aktach), że odpowiedzi nie ma w korpusie.

Każde pytanie ma wzorcową odpowiedź, adresy przepisów, `key_facts` i dosłowne cytaty (`evidence`).

## Kontrola automatyczna (cały zestaw)

Wszystkie adresy istnieją w korpusie, żaden nie jest przepisem `historical` ani jednostką dwuwersyjną,
każdy cytat jest dosłowny, każdy `key_fact` występuje w tekście wskazanych przepisów: **72/72 bez błędów**.

## Przegląd ręczny (wszystkie 72 pytania, wzorce porównane z treścią ustawy)

Kontrola automatyczna sprawdza tylko, czy cytaty istnieją — nie czy wzorzec poprawnie z nich wnioskuje.
Ręczny przegląd znalazł **9 pytań do poprawy** (12%); poprawki są w `golden_build.py` (`PATCH`, `NEW`):

| id | problem | poprawka |
|---|---|---|
| g-ooc-15 | „sytuacja indywidualna” (laptop za 6000 zł) — **korpus zawiera rozstrzygnięcie**: PIT art. 22d ust. 1, jednorazowo do 10 000 zł. Wzorzec kazał odmówić odpowiedzi, której system powinien udzielić | przeniesione do kategorii `multi` jako g-pit-16 z poprawnym wzorcem |
| g-ooc-19 | „płatność kartą — brak w korpusie”: Ordynacja art. 61 § 1 pkt 2 dopuszcza „inny instrument płatniczy” przez e-Urząd | wzorzec poprawiony, art. 61 dodany do odpowiedzi |
| g-ooc-14 | wzorzec powoływał się na nieistniejący „przepis przejściowy dotyczący lat 2016 (art. 146f)” | wzorzec bez zmyślonego odwołania |
| g-vat-18 | korekta przy środku trwałym: wzorzec opierał się na art. 90 ust. 1, a sytuację „pełne odliczenie, potem zmiana prawa” reguluje art. 91 ust. 7 | adresy: art. 91 ust. 7 + ust. 2 |
| g-vat-01 | stawka podstawowa: art. 41 ust. 1 też jest poprawnym miejscem dla wyszukiwania | art. 41 ust. 1 dodany do `answers`; `key_facts` = 23% (odpowiedź „22%” nadal oblewa) |
| g-vat-07 | pytanie o 50% odliczenia bez warunku użytku mieszanego — wtedy odpowiedź „100%” też byłaby poprawna (art. 86a ust. 3) | pytanie doprecyzowane, art. 86a ust. 3 pkt 1 dodany |
| g-pit-12 | sposób liczenia podatku samotnego rodzica jest w art. 6 ust. 4d, nie w ust. 4c | ust. 4d dodany, wzorzec doprecyzowany |
| g-ooc-18 | sprzedaż prywatna: kluczowa definicja działalności to art. 15 ust. 2 | dodany do `answers` |
| g-op-08 | bliźniak g-op-11 (te same przepisy o pełnomocnictwie) | usunięte, zastąpione g-op-12: obniżone odsetki (art. 56a § 1) i wyjątek po zawiadomieniu o kontroli (§ 3 pkt 1) |

Wniosek dla README: **pytania pisane przez model z dostępem do korpusu i samokontrolą nadal miały 12%
błędów merytorycznych** — najczęściej w kategorii „spoza korpusu” (3 z 20), gdzie model był zbyt pewny,
że czegoś w korpusie nie ma. Sama kontrola „cytat istnieje” tego nie łapie.

## Zestaw v1

| akt | fakt | łączące przepisy | potoczne | razem |
|---|---|---|---|---|
| VAT | 12 | 8 | 6 | 26 |
| PIT | 8 | 5 | 3 | 16 |
| Ordynacja | 6 | 3 | 2 | 11 |
| spoza korpusu | | | | 19 |
| **razem** | | | | **72** |

Spoza korpusu: poza tematem 2, inna ustawa 9, inna data 3, sytuacja indywidualna 2, częściowo w korpusie 3.

## Ograniczenia

- Pytania i wzorce pisał model, sprawdzał inny przebieg tego samego modelu i człowiek bez wykształcenia
  prawniczego (przegląd = zgodność z tekstem ustawy, nie wiedza podatkowa spoza niego). To zestaw do
  porównywania wariantów RAG na tym korpusie, nie wyrocznia prawna.
- 72 pytania → przedziały ufności ok. ±11 pkt proc. dla całego zestawu (D6). Do porównań wyszukiwania
  służy zestaw wyszukiwania (283 pytania); złoty zestaw ocenia odpowiedzi.
- Pytania potoczne (11) są w złotym zestawie nieliczne; warstwa potoczna zestawu wyszukiwania (76) jest
  głównym źródłem wyników „język potoczny”.
