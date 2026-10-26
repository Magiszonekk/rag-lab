# web — frontend demo RAG Lab

Statyczna aplikacja (SPA), budowana do `web/dist`. Hosting jeszcze nie wybrany: Azure Static Web Apps albo
serwer domowy. Dlatego nic nie może zależeć od konkretnego hosta.

## Uruchomienie

```bash
cd web
npm ci
npm run dev        # http://localhost:5173 (ten origin jest domyślnie w RAGLAB_CORS_ORIGINS)
npm run build      # tsc + vite build → web/dist
```

- `VITE_API_URL=https://… npm run build` włącza pytania na żywo (Zapytaj, Porównaj). Bez tej zmiennej aplikacja
  pokazuje tylko gotowe przykłady i mówi o tym w interfejsie.
- `base: "./"` i routing po hashu (`#/porownaj?ex=g-vat-07`): `dist/` działa z dowolnej ścieżki i bez reguł
  przepisywania adresów na serwerze. Na Azure SWA nie trzeba `navigationFallback`.
- Wyniki (zakładki „Wyniki” i „Jak to działa”) są wczytywane **przy buildzie** z `../results/*.json`
  (`answers_golden_v1`, `retrieval_v1`, `retrieval_v1_rewrite`, `retrieval_golden_rewrite`, `judge_calibration_v1`,
  `law_watch`). Po nowej ewaluacji przebuduj frontend.
- Fonty są lokalne (`@fontsource`), bez Google Fonts: Manrope (nagłówki), Figtree (tekst), Source Serif 4 (tekst
  ustaw), DM Mono (kod).

## Ekrany

| hash | co pokazuje |
|---|---|
| `#/zapytaj?ex=&v=&verify=off` | pole pytania, wariant, przełącznik sprawdzania; odpowiedź z klikalnymi cytatami i panelem przepisów (adres, status, stan prawny, adnotacja o przepisie przejściowym) |
| `#/porownaj?ex=` | 4 warianty obok siebie: werdykt sędziego, tokeny, czas, co dociągnął agent, zdania usunięte przy sprawdzaniu |
| `#/slad?ex=&v=` | kroki: wyszukiwanie, decyzje agenta get/search (z `why`, `not_found`), kontekst, generowanie, weryfikacja |
| `#/wyniki` | tabele z README z przedziałami ufności, testy McNemara, kalibracja sędziego, zastrzeżenia |
| `#/o-projekcie` | jak to działa, korpus ze stanem prawnym i zmianami po dacie tekstu jednolitego |

Odmowa przy pytaniu, na które jest odpowiedź w korpusie, ma etykietę „odmowa (pominięty przepis)”, choć sędzia
ocenia ją jako `refusal_ok` (znany błąd sędziego, opisany w README). Przy pytaniach `out_of_corpus` ta sama
ocena to „słuszna odmowa”.

## Dane

- `public/examples.json`: gotowe przykłady (9 pytań × 4 warianty), generowane przez
  `uv run python -m raglab.export_examples`. **Muszą działać bez backendu**, bo to podstawa demo.
  Struktura: `{meta: {variants: {id: etykieta}, answer_model, judge_model, disclaimer}, examples: [{id,
  question, category, reference_answer, variants: {simple|hybrid|hyde|agentic-strict: {answer, citations,
  refused, context: [{address, status, note, text}], steps: [{kind, attrs}], tokens, latency_ms, verify,
  judge: {verdict, reason}}}}]}`.
- API (opcjonalne, adres z `VITE_API_URL`, domyślnie brak, czyli tylko przykłady):
  - `GET /health` → `{ok, live}`; gdy `live=false`, pole pytania na żywo jest wyłączone z informacją;
  - `POST /ask {question, variant, verify}` → jak wariant w przykładach + `trace_id`, `model`, `cached`;
    `429` = limit (komunikat w `detail`), `503` = pytania na żywo wyłączone;
  - `POST /compare {question, verify}` → `{wariant: odpowiedź}` dla 4 wariantów;
  - `GET /trace/<id>`, `GET /corpus`, `GET /eval/results` (tabele wyników).
- Wyniki ewaluacji do zakładki „Wyniki”: `GET /eval/results` albo statycznie z `results/*.json`.
