# web — frontend demo RAG Lab

Statyczna aplikacja (SPA), budowana do `web/dist`. Hosting jeszcze nie wybrany: Azure Static Web Apps albo
serwer domowy. Dlatego nic nie może zależeć od konkretnego hosta.

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
