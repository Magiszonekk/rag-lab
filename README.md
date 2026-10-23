# RAG Lab — transparent RAG on Polish tax law

> 🇵🇱 Przejrzysty RAG na polskich ustawach podatkowych (VAT, PIT, Ordynacja podatkowa): kilka wariantów
> wyszukiwania na tych samych danych, porównanych liczbami, z podglądem każdego kroku. Projekt w budowie.

**Status: work in progress (milestone M1).** Not tax advice — a technical demo.

## Idea

Not another "chat with a PDF". Several RAG variants run on the same corpus, the same model and the same
test sets, and differ only in retrieval. Every claim about which one is better comes with a number and
a confidence interval.

## What works today

- **Ingest** of the official consolidated texts (Dz.U.) of three Polish tax acts from the Sejm ELI API,
  pinned by SHA-256: VAT (DU/2026/1263), PIT (DU/2026/592), Tax Ordinance (DU/2026/622).
  - PDF → structure (article → paragraph/§ → point → letter) with PyMuPDF; footnotes are detected by font
    size and position, not by regex, and kept as metadata (40/40, 57/57, 52/52 footnotes recovered);
  - annex tables (e.g. VAT reduced-rate lists) via pdfplumber, one row = one record;
  - units with two wordings in the consolidated text (current vs. future, from footnotes) are flagged;
  - transitional provisions labelled `in_force` / `historical` / `conditional` relative to the legal
    state date (model labels + manual corrections — e.g. the current 23% VAT rate lives in a transitional
    article, while art. 41 still says 22%).
- **Retrieval test set v1**: 283 questions (207 generated from 207 distinct provisions + 76 colloquial
  paraphrases). Generator and validator are from different model families; questions copying the
  statute or naming article numbers are filtered; a second pass checks questions against the provisions
  the source cross-references. Manual review notes: [`data/eval/retrieval_v1.REVIEW.md`](data/eval/retrieval_v1.REVIEW.md).

## Run

```bash
uv sync
uv run python -m raglab.ingest fetch      # download PDFs, verify SHA-256
uv run python -m raglab.ingest build      # build data/corpus/*.json
uv run python -m raglab.ingest show vat 86
uv run pytest -q
docker compose up -d                      # Postgres + pgvector on 127.0.0.1:5436
```

LLM steps (test-set generation) use any OpenAI-compatible endpoint: set `LLM_BASE_URL` and `LLM_API_KEY`
in `.env` (see `.env.example`).

## Roadmap

- **M1** — retrieval baseline: chunking by legal structure, BM25 on lemmas vs. vectors vs. hybrid,
  recall@k / MRR with confidence intervals, CI gate on retrieval metrics; golden answer set.
- **M2** — answering variants (simple, hybrid + reranker, agentic with LangGraph), answer checking
  (citations / key facts / LLM judge calibrated against human labels), tracing.
- **M2b** — scaling the corpus from 3 to 19 tax acts and measuring retrieval degradation.
- **M3** — public demo with comparison mode and trace viewer.
- **M4** — the same stack deployed to Azure from code (Bicep, Container Apps, PostgreSQL Flexible,
  Azure OpenAI), deploy → evaluate → destroy.

## License

Code: MIT. Statutory texts are not protected by copyright (Polish Copyright Act, art. 4).
