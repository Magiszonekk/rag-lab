export type VariantId = "simple" | "hybrid" | "hyde" | "agentic-strict";
export const VARIANTS: VariantId[] = ["simple", "hybrid", "hyde", "agentic-strict"];

export type Verdict = "correct" | "partial" | "incorrect" | "refusal_ok" | "refusal_missing";
export type Category = "fact" | "multi" | "colloquial" | "out_of_corpus" | string;

export interface ContextBlock {
  address: string;
  status: string | null;
  note: string | null;
  text: string;
}

export interface Step {
  kind: string;
  attrs: Record<string, unknown>;
}

export interface VerifyResult {
  verdict: "pass" | "fix" | "fail" | "error" | string;
  unsupported: string[];
  fixed?: boolean;
  blocked?: boolean;
}

export interface VariantAnswer {
  answer: string;
  citations: string[];
  refused: boolean;
  context: ContextBlock[];
  steps: Step[];
  tokens?: number;
  latency_ms?: number;
  verify: VerifyResult | null;
  judge?: { verdict: Verdict; reason: string } | null;
  // tylko na żywo
  trace_id?: string | null;
  model?: string | null;
  cached?: boolean;
  error?: string | null;
}

export interface Example {
  id: string;
  question: string;
  category: Category;
  reference_answer?: string | null;
  variants: Record<VariantId, VariantAnswer>;
}

export interface ExamplesFile {
  meta: {
    generated: string;
    answer_model: string;
    judge_model: string;
    variants: Record<VariantId, string>;
    disclaimer: string;
  };
  examples: Example[];
}
