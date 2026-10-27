import type { Category, Verdict, VariantId } from "./types";

export const VARIANT_INFO: Record<VariantId, { name: string; short: string; how: string }> = {
  simple: { name: "Prosty", short: "wektory", how: "Top-5 fragmentów z wyszukiwania wektorowego (Qwen3-Embedding-8B; gotowe przykłady: mmlw-roberta-base)." },
  hybrid: { name: "Hybrydowy", short: "BM25 + wektory", how: "BM25 na lematach (Morfeusz 2) i wektory, łączone przez RRF." },
  hyde: { name: "HyDE", short: "hybryda + hipotetyczny przepis", how: "Model pisze hipotetyczny przepis, szukamy nim i pytaniem jednocześnie." },
  "agentic-strict": { name: "Agentowy", short: "HyDE + do 3 kroków get/search", how: "Agent widzi zebrane przepisy i może dociągnąć brakujący ustęp albo szukać ponownie. Tylko adresy wynikające z kontekstu." },
};

export const VERDICT: Record<string, { label: string; tone: "ok" | "partial" | "bad" | "refuse-ok" }> = {
  correct: { label: "poprawna", tone: "ok" },
  partial: { label: "częściowo", tone: "partial" },
  incorrect: { label: "błędna", tone: "bad" },
  refusal_ok: { label: "odmowa", tone: "refuse-ok" },
  refusal_missing: { label: "brak odmowy", tone: "bad" },
};

export function verdictLabel(v: Verdict | string | undefined, category: Category): { label: string; tone: string; title: string } {
  if (!v) return { label: "bez oceny", tone: "none", title: "Odpowiedź na żywo nie jest oceniana przez sędziego." };
  // Sędzia ocenia odmowę przy pytaniu, na które jest odpowiedź w korpusie, jako „refusal_ok” (znany błąd sędziego, README).
  if (v === "refusal_ok" && category !== "out_of_corpus")
    return { label: "odmowa (pominięty przepis)", tone: "miss", title: "Pytanie ma odpowiedź w korpusie, a wariant odmówił, bo kluczowy przepis nie trafił do kontekstu. Sędzia liczy to jako słuszną odmowę; w wynikach to fałszywa odmowa." };
  if (v === "refusal_ok") return { label: "słuszna odmowa", tone: "refuse-ok", title: "Pytanie spoza korpusu: system powinien odmówić i odmówił." };
  const x = VERDICT[v] ?? { label: v, tone: "none" };
  return { ...x, title: `Werdykt sędziego: ${x.label}` };
}

export const CATEGORY: Record<string, string> = {
  fact: "fakt",
  multi: "kilka przepisów",
  colloquial: "potocznie",
  out_of_corpus: "spoza korpusu",
};

/** Krótki tytuł przykładu do listy. */
export const EXAMPLE_TITLE: Record<string, string> = {
  "g-vat-01": "Podstawowa stawka VAT",
  "g-vat-07": "Samochód firmowo-prywatny: ile VAT odliczę?",
  "g-vat-16": "Kancelaria prawna a zwolnienie z VAT",
  "g-vat-26": "Kasa fiskalna w warsztacie",
  "g-pit-02": "Skala podatkowa PIT",
  "g-pit-15": "Alimenty dla byłej żony a PIT",
  "g-op-07": "Korekta deklaracji w trakcie postępowania",
  "g-ooc-01": "Przepis na jajecznicę",
  "g-ooc-06": "Darowizna od rodzica (inna ustawa)",
};
