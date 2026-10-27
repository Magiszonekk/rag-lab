# RAG Lab — transparent RAG on Polish tax law

> 🇵🇱 Przejrzysty RAG na polskich ustawach podatkowych (VAT, PIT, Ordynacja podatkowa): kilka wariantów
> wyszukiwania na tych samych danych, porównanych liczbami, z podglądem każdego kroku. Projekt w budowie.

**Status: M1–M3 done. Live demo: https://rag.cikowice.pl.** Next: scaling to 19 acts (M2b), Azure as code (M4). Not tax advice — a technical demo.

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

## Query rewriting for colloquial questions

Colloquial questions were the weak spot (hybrid recall@5 0.79 vs 0.90 for statute-like questions). Before
retrieval an LLM rewrites the question; results for the original and rewritten query are fused with RRF. The
rewriter never sees test data and article numbers are stripped from its output (otherwise we would be measuring
the model's memory of the statute, not retrieval).

Rewriter: Claude Sonnet 5.

| retrieval | recall@5, retrieval set (283) | colloquial (76) | recall@5, golden (53) | colloquial (11) |
|---|---|---|---|---|
| hybrid | 0.880 (0.84–0.92) | 0.789 | 0.755 (0.64–0.87) | 0.455 |
| + rewrite to statute language | 0.905 | 0.882 | 0.830 | 0.636 |
| **+ HyDE** (hypothetical provision) | **0.912 (0.88–0.94)** | 0.895 | 0.868 (0.77–0.94) | 0.818 |
| + both | 0.912 | 0.908 | **0.925 (0.85–0.98)** | **1.000** |

- On the golden set the gain is significant (both vs hybrid: 10 : 1 discordant questions, McNemar p = 0.012).
- On the larger retrieval set it is **not** (HyDE vs hybrid 16 : 7, p = 0.09), although colloquial questions
  improve consistently.
- **The effect depends on the rewriter.** With an earlier rewriter (GPT-5.6, kept as `*.gpt56luna.*` in
  `results/`) HyDE was significant on the retrieval set too (p = 0.008). A query-rewriting gain is a property
  of the rewriter + retriever pair, not of the technique.

## First results — answers (M2, in progress)

Golden set v1: 53 answerable questions + 19 out-of-corpus. Same answering model, prompt and context builder for
every variant; only retrieval differs. **Answerer: Claude Sonnet 5. Judge: Nemotron 3 Ultra** (a different
model family), with a fixed scale (correct / partial / incorrect / refusal_ok / refusal_missing) and a reason.

| variant | correct (95% CI) | correct + partial | key facts | cites gold provision | faithful | correct refusals | false refusals* | p50 latency |
|---|---|---|---|---|---|---|---|---|
| simple (vectors) | 0.755 (0.64–0.87) | 0.774 | 0.698 | 0.704 | 0.986 | 12/13 | 0.226 | 6.2 s |
| hybrid (BM25 + vectors) | 0.811 (0.70–0.91) | 0.849 | 0.698 | 0.758 | 0.986 | 13/13 | 0.151 | 6.2 s |
| **hybrid + HyDE** | **0.906 (0.81–0.98)** | **0.925** | **0.792** | **0.843** | 0.972 | 13/13 | **0.057** | 10.2 s |
| hybrid + HyDE + `verify=cite` | 0.830 | 0.849 | 0.726 | 0.843 | 0.889 | 13/13 | 0.132 | |
| hybrid + HyDE + `verify=llm` | 0.906 | 0.925 | 0.792 | 0.843 | 0.958 | 13/13 | 0.057 | +5–40 s |
| agentic (LangGraph) | 0.981 (0.94–1.00) | 0.981 | 0.896 | 0.925 | 0.944 | 12/13 | 0.000 | 10.2 s |
| **agentic, strict navigation** | **0.981 (0.94–1.00)** | **1.000** | 0.849 | 0.925 | **0.986** | 13/13 | **0.000** | 10.2 s |
| agentic strict + `verify=llm` | 1.000 | 1.000 | 0.849 | 0.925 | 0.986 | 13/13 | 0.000 | |

\*A false refusal is an answerable question where the system said it couldn't answer — either with the refusal
flag or in plain words ("the provision isn't in my materials"). Counting only the flag hid most of them (HyDE:
0/53 by flag, 3/53 in fact); found while reviewing judge disagreements.

- **HyDE vs simple is significant** (10 : 2 on "correct", p = 0.039); **HyDE vs hybrid is not yet**
  (6 : 1, p = 0.13) — 53 questions are too few to separate them.
- **Refusals work**: the questions about other acts / non-tax topics were refused, with no answers from the
  model's own knowledge.
- **The remaining errors are retrieval misses, not hallucinations.** All 3 HyDE false refusals are questions
  whose key provision (art. 86a ust. 1 — 50% for mixed-use cars; art. 113 ust. 13; art. 111 ust. 1) didn't
  reach the top-5; the system says so instead of guessing. One real substantive error remains: a KSeF question
  where the model applies an exemption for EU-established taxpayers (art. 113a ust. 1) to a Polish freelancer.
- **Transitional provisions matter**: art. 41 VAT still says 22%; the 23% rate lives in a transitional article.
  The context builder attaches overriding transitional provisions with an explicit note. Without it the system
  cites the right article and gives the wrong rate, which no citation check can catch.

### Answer model comparison: Sonnet 5.5 vs Opus 5.5 (embedding Qwen3-8B)

Retrieval embedding switched to `qwen/qwen3-embedding-8b` (OpenRouter, provider pinned): alone it finds the gold
provision in the top-5 for 94% of retrieval questions vs 84% for the local `mmlw-roberta-base` (32 : 4,
p < 0.0001). The same model answers, rewrites (HyDE), plans the agent and verifies; judge: Nemotron 3 Ultra.
Golden set v1.1 (one reference answer fixed, see below). Results in `results/series/`.

| variant | Sonnet 5.5 | Opus 5.5 | Sonnet : Opus (McNemar) |
|---|---|---|---|
| simple (vectors) | 0.887 (0.79–0.96) | 0.925 (0.85–0.98) | 2 : 4, p = 0.69 |
| hybrid (BM25 + vectors) | 0.868 (0.76–0.94) | 0.868 (0.76–0.94) | 1 : 1, p = 1.0 |
| hybrid + HyDE | 0.925 (0.85–0.98) | 0.887 (0.79–0.96) | 4 : 2, p = 0.69 |
| **agentic, strict** | **0.962 (0.91–1.00)** | **0.981 (0.94–1.00)** | 1 : 2, p = 1.0 |

- **No measurable difference between Sonnet 5.5 and Opus 5.5** on this task: they disagree on 2–6 of 53
  questions, in both directions. When the model only has to read the provisions it was given, the larger model buys
  nothing measurable here.
- **A better embedding does most of the work the retrieval tricks used to do.** With Qwen3-8B the plain vector
  variant is within noise of HyDE and the agent; adding BM25 (hybrid) is slightly *worse* and refuses more often
  (11% vs 2–4% false refusals). With `mmlw-roberta-base`, hybrid and HyDE were clear wins.
- Correct refusals: 13/13 in every variant of both series. Sonnet 5.5 often refuses in words without setting the
  refusal flag, so correct refusals are now counted from the judge verdict too (the flag alone gave 10/13).

**Second judge (Opus 5.5) on the HyDE and agentic answers of both series**: agreement with Nemotron 90% / 87%,
Cohen's κ = 0.76 / 0.70 — clearly better than the earlier GPT-OSS calibration (κ = 0.52). **Self-preference was
measured, not assumed**: Opus-as-judge rated Opus's own answers exactly as Nemotron did (0.925 vs 0.925) and
Sonnet's answers 0.9 pp higher — no sign it favours its own model. The 13 correct/partial disagreements were
reviewed against the statute: borderline calls in both directions (an omitted condition vs extra detail), no
systematic bias of either judge.

**Golden set v1.1**: reviewing these disagreements showed the reference answer for the KSeF question was wrong. It
said "no exception covers a freelancer" and missed the temporary provision art. 145m VAT (paper invoices allowed
until 31.12.2026 for up to 10 000 zł a month). Both models cited it correctly and the judge marked them wrong
for it. The reference was fixed (`golden_build.py`, v1.1) and only that question was re-judged.

### Agentic variant

A LangGraph loop: `retrieve` (hybrid + HyDE, as above) → `plan` ⇄ `tools` → `answer`. In `plan` the model sees
the collected provisions and picks one action (JSON protocol, no native tool calling): **get** provisions by
address, **search** again with a different wording, or **answer**. At most 3 tool steps; the final answer uses
the same prompt as the other variants.

- It fixes exactly the retrieval misses above: it sees art. 86a ust. 2–5 and fetches ust. 1 (the 50% rule);
  follows "o którym mowa w art. 113 ust. 13" to the exemption exclusion; fetches art. 111 ust. 1 (the cash
  register duty). 56 of 72 questions need no extra step, so the median cost equals HyDE.
- **Is it the system or the model's memory?** In the free variant 6 of 25 fetched addresses came from the model
  knowing where things are in the VAT act (nothing in the context pointed there; once even an act outside the
  corpus). The **strict** variant may fetch only another unit of an article already in context or a provision
  the text refers to. It scores the same (strict vs free 1 : 1, p = 1.0) — the gain is navigation of the
  statute's structure, not recall. Strict is the variant for the demo.
- vs hybrid: 10 : 1 (p = 0.012); vs simple: 12 : 0 (p = 0.0005); **vs HyDE: 4 : 0, p = 0.125 — not
  significant** on 53 questions. With ~48/53 already correct for HyDE, the golden set is close to saturated; a
  harder test set is needed to separate the best variants (M2b).
- Cost: median 9.6k tokens per question vs 4.8k for HyDE; p95 latency 30 s vs 22 s.

### Answer verification

- **`verify=cite` (deterministic) hurts**: numbers in the answer must appear in the cited text. It blocked 6
  HyDE answers, 5 of them correct — derived or restated numbers ("2 × 92.67 = 185.34 zł", "5 lat", "180 dni").
- **`verify=llm` (sentence by sentence)**: a verifier model splits the answer into claims and checks each against
  the context (arithmetic and paraphrase allowed); unsupported sentences are removed, an unsupported main thesis
  turns the answer into a refusal. It blocked **no** correct answer, trimmed 6–7 answers per variant (e.g. "so the
  ex-wife must pay tax on 200 zł" — the statute only says the excess isn't exempt) and changed the score by
  0 to +2 pp. It does **not** catch a misapplied provision (the KSeF case): the claim *is* in the cited text; the
  error is that it doesn't fit the user's facts. It is the default guard for the demo; `cite` stays off.

### Judge calibration

A second judge from a third model family (GPT-OSS-120B; answerer is Claude, main judge Nemotron) scored the same
72 HyDE answers; 41 pairs completed before its free-tier daily limit. Agreement 85% (35/41), Cohen's κ = 0.52
on collapsed classes (ok / partial / wrong / correct refusal). All 6 disagreements were reviewed by hand against
the statute (`data/eval/golden/judge_review_v1.jsonl`): each judge was right in 3.

- **Main judge's systematic error**: it rated honest "the provision isn't in my context" answers as correct
  refusals, even when the answer *is* in the corpus. By the scale that is a failure (a retrieval miss). This is
  why false refusals are now counted from the answer text, not only the flag (table above).
- **Second judge's errors**: it penalised correct extra details (calling the real 8% transitional rate "alleged")
  and was too lenient on the misapplied KSeF exemption.
- The "human" reviewer here is the author's assistant model (Claude), checking against the statute text — the
  answerer's family. A review by a tax professional is out of scope; treat κ = 0.52 as moderate agreement.

**Same conclusions on a second series** (GPT-5.6 answering, Claude judging; `results/*.gpt56luna.*`): HyDE
0.849, hybrid 0.792, simple 0.717. Numbers from different answerer/judge pairs are not mixed in one table.
An earlier judge version saw only the first 2,500 characters of each context block and marked citations of later
paragraphs as "not in context" (−2 to −4 pp for every variant); fixed before all numbers above.

## Live demo

**https://rag.cikowice.pl**: ready-made examples (all variants side by side, traces, results) plus live questions.
Live answers: retrieval with Qwen3-Embedding-8B (local `mmlw-roberta-base` as automatic fallback when the
embedding API fails), answering with Claude Sonnet 5.5 behind the gateway, falling back to free models (Gemini 3
Flash, DeepSeek V4.1 Flash) on errors or rate limits. The default variant is the plain vector one; the agent is one
click away. Answers stream as they are written (`POST /ask/stream`, NDJSON: retrieved provisions, agent steps,
answer text, final result), so the first words appear after ~5 s instead of waiting for the whole answer.
Sentence-by-sentence verification is opt-in (it is a second full model call, about +8 s). Limits: 100 questions a day, 10 an hour per IP,
plus RPM/TPM and a USD budget on the gateway key. The ready-made examples work without the backend.

## Demo backend (M3)

- **API** (`src/raglab/api.py`, FastAPI): `/examples`, `/ask`, `/compare`, `/trace/<id>`, `/corpus`, `/eval/results`.
  Ready-made examples (`web/public/examples.json`, 9 questions × 4 variants with traces and judge verdicts) work
  without the backend. Live questions: per-IP and daily limits, answer cache, question length limit, a topic
  filter, CORS only for the frontend domain.
- **Model gateway (LiteLLM, pinned)** between the backend and any model: a demo key restricted to models billed by
  API key (no consumer subscriptions), with a USD budget and RPM/TPM limits; a separate key for evaluation.
  Checked before any public traffic (`python -m raglab.gateway test`): the demo key is refused for a model outside
  its list (403), works for its own (200), an exhausted budget is refused (422 `budget_exceeded`), the RPM limit
  returns 429. **Pitfall found**: LiteLLM doesn't know prices of models behind an OpenAI-compatible gateway, counts
  their cost as 0, and the budget never triggers. Explicit `model_info` prices fix it.
- **Every model call on the demo path goes through the demo key**: query rewriting, answering, agent planning and
  verification. A test asserts this, so a helper step can't silently fall back to evaluation models.
- **Traces** (`traces`, `trace_steps` in Postgres): retrieval, agent decisions, context, generation, verification;
  personal data (PESEL, NIP, e-mail, phone) masked before saving; no gateway addresses in traces or responses.
- **Law watch** (`python -m raglab.law_watch`, weekly GitHub Action): asks the Sejm ELI API whether a newer
  consolidated text or an amendment that is already in force appeared after the corpus date; opens an issue,
  never changes the corpus. First run: VAT up to date (next change 2027-01-01); PIT and the Tax Ordinance each
  have 3 amendments in force since their consolidated texts (shown in `/corpus`).

## Kubernetes (Helm chart)

`deploy/helm/raglab` installs the whole stack in a cluster. CI runs it in [kind](https://kind.sigs.k8s.io/) on
every push, and M4 reuses the same chart on AKS.

| component | kind | notes |
|---|---|---|
| API | Deployment + Service (+ Ingress) | readiness = a BM25 query works (corpus loaded), not just a live process; `Recreate` because the data volume is RWO |
| Postgres + pgvector | StatefulSet | traces + the LiteLLM database; init SQL shared with Docker Compose; can be switched off for a managed Postgres (`postgres.enabled=false`) |
| LiteLLM gateway | Deployment | the same `config.yaml` as Docker Compose (one file) |
| corpus ingest | Job per release revision | downloads the statutes from the Sejm API (SHA-256 checked) and builds the corpus on the data volume; the API init container waits for it |
| law watch | CronJob | daily check for amendments in force after the corpus date; `/corpus` reads its report |
| answer evaluation | Job, on demand | `--set eval.enabled=true`; golden set → variants → judge, results on the volume |

Without any keys the release serves BM25 search, ready-made examples, results and the corpus, while live
questions return 503. Keys come from an existing Secret (`secrets.existingSecret`, on AKS from Key Vault) and are
never in values. Hardening: non-root UID, read-only root filesystem, dropped capabilities, `RuntimeDefault`
seccomp, resource requests and limits on every pod, no service-account token. NetworkPolicies let only the API
take traffic from outside the release. Checked in kind: a stray pod reaches the API but times out on Postgres and
LiteLLM.

```bash
docker build -t raglab-api:dev .
kind create cluster --name raglab && kind load docker-image raglab-api:dev --name raglab
helm install raglab deploy/helm/raglab -n raglab --create-namespace \
  --set image.repository=raglab-api --set image.tag=dev --set image.pullPolicy=Never --wait --wait-for-jobs
helm test raglab -n raglab --logs     # health + BM25 query + 3-act corpus + examples
```

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
- **M2** ✅ (variants incl. agentic, HyDE, verification, judge calibration) — answering variants (simple, hybrid + reranker, agentic with LangGraph), answer checking
  (citations / key facts / LLM judge calibrated against human labels), tracing.
- **M2b** — scaling the corpus from 3 to 19 tax acts and measuring retrieval degradation.
- **M3** ✅ public demo with comparison mode, trace viewer and streamed answers.
- **M3b** ✅ Helm chart (API, Postgres + pgvector, LiteLLM, ingest Job, law-watch CronJob, eval Job),
  installed and tested in kind in CI.
- **M4** — the same chart on Azure, provisioned with Terraform: AKS, ACR, Key Vault, workload identity, state in
  Azure Storage; GitHub Actions with OIDC (plan on PR → approval → apply → evaluate → destroy). Models stay behind
  the LiteLLM gateway, because swapping the provider is configuration.

## License

Code: MIT. Statutory texts are not protected by copyright (Polish Copyright Act, art. 4).
