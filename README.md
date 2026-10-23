# RAG Lab — transparent RAG on Polish tax law

> 🇵🇱 Przejrzysty RAG na polskich ustawach podatkowych (VAT, PIT, Ordynacja podatkowa): kilka wariantów
> wyszukiwania na tych samych danych, porównanych liczbami, z podglądem każdego kroku. Projekt w budowie.

**Status: M1 done (retrieval + test sets); M2 in progress (answering variants, verification, judge).** Not tax advice — a technical demo.

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

## First results — retrieval (M1)

Retrieval test set v1: 283 questions over 3 tax acts (207 generated from distinct provisions + 76 colloquial
paraphrases). A hit means the retrieved chunk contains ≥ 50% of the gold provision, or ≥ 50% of the chunk *is*
the gold provision (a looser "chunk touches the provision" metric favours long windows and is reported in
`results/`). 95% CIs: bootstrap over questions; pairwise comparisons: exact McNemar test on hit@5.

| configuration | recall@5 (95% CI) | recall@1 | MRR@20 | colloquial recall@5 | context tokens in top-5 |
|---|---|---|---|---|---|
| BM25, no lemmatization | 0.689 (0.63–0.74) | 0.396 | 0.517 | 0.447 | 723 |
| BM25 + Morfeusz 2 lemmas | 0.806 (0.76–0.85) | 0.587 | 0.682 | 0.697 | 774 |
| vectors (`sdadas/mmlw-roberta-base`, CPU) | 0.841 (0.80–0.88) | 0.601 | 0.707 | **0.803** | 734 |
| **hybrid (BM25 + vectors, RRF)** | **0.876 (0.84–0.92)** | **0.625** | **0.735** | 0.789 | 751 |
| fixed 400-token windows + BM25 | 0.802 (0.76–0.85) | 0.519 | 0.643 | 0.684 | 2005 |
| fixed 400-token windows + vectors | 0.682 (0.63–0.74) | 0.367 | 0.508 | 0.632 | 2005 |

What the numbers say (and don't):
- **Lemmatization is the biggest single win for BM25**: +11.7 pp recall@5 (McNemar p < 0.0001), +25 pp on
  colloquial questions. Polish inflection matters — "podatnik" appears in 9 forms in the VAT act alone.
  Morfeusz 2 with two general disambiguation rules beat spaCy `pl_core_news_md` on legal vocabulary (70/70 vs
  62/70 forms, 22/22 vs 16/20 held-out inflection groups) and is 80× faster ([benchmark](data/eval/lemma_bench.json)).
- **Hybrid beats BM25** (p = 0.0003) but **not significantly vectors alone** (p = 0.064) on 283 questions.
- **Chunking by legal structure matters for vectors**: same model, fixed windows lose 16 pp (p < 0.0001); for
  BM25 it is a tie on recall, at 2.6× less context.
- On the 53 hand-checked golden questions (harder: multi-provision and colloquial) every configuration
  drops (hybrid recall@5 0.755, BM25 0.566) — see `results/retrieval_golden.json`.
- Embedding the corpus (5.2k chunks) takes ~14 min on 4 CPU cores once; a query embedding ~130 ms (p50).

**CI gate**: every PR rebuilds the corpus and runs the BM25 configurations on the retrieval set (no LLM,
no keys, deterministic); the build fails if recall@5 drops more than 2 pp below `results/retrieval_baseline.json`.

## First results — answers (M2, in progress)

Golden set v1: 53 answerable questions + 19 out-of-corpus. Same answering model, prompt and context builder for
every variant — only retrieval differs. Judge: a model from a different family than the answerer, with a fixed
scale (correct / partial / incorrect / refusal_ok / refusal_missing) and a reason; 15 verdicts spot-checked by hand.

| variant | correct (95% CI) | correct + partial | key facts | cites gold provision | faithful to context | correct refusals | false refusals | p50 latency |
|---|---|---|---|---|---|---|---|---|
| simple (vectors) | 0.698 (0.57–0.81) | 0.811 | 0.623 | 0.714 | 0.958 | 13/13 | 0.151 | 2.8 s |
| **hybrid (BM25 + vectors)** | **0.755 (0.64–0.87)** | **0.830** | **0.642** | **0.758** | 0.958 | 13/13 | **0.094** | 3.3 s |
| hybrid + `verify=cite` | 0.755 | 0.811 | 0.623 | 0.758 | 0.944 | 13/13 | 0.113 | 3.3 s |

- **Refusals work**: all 13 questions about other acts / non-tax topics were refused; the other 6 out-of-corpus
  cases (other dates, individual advice, partial coverage) were handled as expected in 15/19 overall.
- **Most errors are retrieval misses, not hallucinations**: of the hybrid's 5 wrong answers, 4 are refusals where
  the right provision wasn't in the top-5 (mostly colloquial questions: 6/11 correct vs 21/26 for factual).
- **Transitional provisions matter**: art. 41 VAT still says 22%; the 23% rate lives in a transitional article.
  The context builder attaches overriding transitional provisions with an explicit note — without it the system
  cites the right article and gives the wrong rate, which no citation check can catch.
- **`verify=cite` is cheap but blunt**: it blocked 1 answer per variant, both false positives (a derived sum
  "2 × 92.67 = 185.34 zł"; a citation to a paragraph the model knew but wasn't in context). It costs ~2 pp of
  false refusals and catches nothing on this set — LLM-level verification (`verify=llm`) is next.
- Cost: ~3k tokens per question.

## Test sets

- `data/eval/retrieval_v1.jsonl` — 283 retrieval questions; generation, validation and review notes in
  [`retrieval_v1.REVIEW.md`](data/eval/retrieval_v1.REVIEW.md).
- `data/eval/golden/golden_v1.jsonl` — 72 answer-quality questions with reference answers, key facts and
  verbatim evidence: fact / multi-provision / colloquial, plus 19 **out-of-corpus** questions (other tax acts,
  other dates, individual advice, partial answers) where the system must refuse. Drafted by sub-agents with a
  corpus lookup tool, then reviewed by hand against the statute: 9 of 72 (12%) had substantive errors despite
  passing automatic citation checks — [`GOLDEN_v1.REVIEW.md`](data/eval/golden/GOLDEN_v1.REVIEW.md).

## Run

```bash
uv sync
uv run python -m raglab.ingest fetch      # download PDFs, verify SHA-256
uv run python -m raglab.ingest build      # build data/corpus/*.json
uv run python -m raglab.ingest show vat 86
uv run pytest -q
uv run python -m raglab.search.evaluate   # retrieval metrics → results/retrieval_v1.json
uv run python -m raglab.rag.evaluate      # answers + judge on the golden set (needs LLM_* in .env)
uv run python -m raglab.lookup show "VAT art. 146ef ust. 1"
docker compose up -d                      # Postgres + pgvector on 127.0.0.1:5436
```

LLM steps (test-set generation) use any OpenAI-compatible endpoint: set `LLM_BASE_URL` and `LLM_API_KEY`
in `.env` (see `.env.example`).

## Roadmap

- **M1** ✅ retrieval baseline: chunking by legal structure, BM25 on lemmas vs. vectors vs. hybrid,
  recall@k / MRR with confidence intervals, CI gate on retrieval metrics; golden answer set.
- **M2** — answering variants (simple, hybrid + reranker, agentic with LangGraph), answer checking
  (citations / key facts / LLM judge calibrated against human labels), tracing.
- **M2b** — scaling the corpus from 3 to 19 tax acts and measuring retrieval degradation.
- **M3** — public demo with comparison mode and trace viewer.
- **M4** — the same stack deployed to Azure from code (Bicep, Container Apps, PostgreSQL Flexible,
  Azure OpenAI), deploy → evaluate → destroy.

## License

Code: MIT. Statutory texts are not protected by copyright (Polish Copyright Act, art. 4).
