// Wyniki ewaluacji wczytywane przy buildzie z results/*.json (te same pliki co w README i GET /eval/results).
import answers from "../../../results/answers_golden_v1.json";
import retrieval from "../../../results/retrieval_v1.json";
import retrievalRewrite from "../../../results/retrieval_v1_rewrite.json";
import goldenRetrieval from "../../../results/retrieval_golden.json";
import goldenRewrite from "../../../results/retrieval_golden_rewrite.json";
import calibration from "../../../results/judge_calibration_v1.json";
import lawWatch from "../../../results/law_watch.json";

export type Metric = { mean: number; ci95: [number, number]; n: number };

type RetrievalCfg = {
  all: Record<string, unknown> & { "recall@5": number; "recall@1": number; "mrr@20": number; "tokens@5": number; n: number; ci95: Record<string, [number, number]> };
  paraphrased: { "recall@5": number; n: number };
};
type RetrievalFile = { date: string; n: number; configs: Record<string, RetrievalCfg>; "mcnemar_hit@5": Record<string, { only_a: number; only_b: number; p: number }> };
type AnswerCfg = Record<string, Metric> & { tokens_per_question: number; latency_ms_p50: number; latency_ms_p95: number; verdicts: Record<string, number> };
type AnswersFile = { date: string; n: number; answer_models: string[]; judge_models: string[]; configs: Record<string, AnswerCfg> };

export const ANSWERS = answers as unknown as AnswersFile;
export const RETRIEVAL = retrieval as unknown as RetrievalFile;
export const RETRIEVAL_REWRITE = retrievalRewrite as unknown as RetrievalFile;
export const GOLDEN_RETRIEVAL = goldenRetrieval as unknown as RetrievalFile;
export const GOLDEN_REWRITE = goldenRewrite as unknown as RetrievalFile;
export const CALIBRATION = calibration as {
  n: number; n_pairs_both_judged: number; agree: number; judge_agreement: number; judge_kappa: number; reviewed: number;
};
export const LAW_WATCH = lawWatch as unknown as {
  checked: string;
  acts: Record<string, { name: string; corpus_text: string; stale: boolean;
    changes_after_corpus: { eli: string; in_force_from: string; already_in_force: boolean }[] }>;
};
