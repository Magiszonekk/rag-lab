import type { ContextBlock } from "./types";

/** Akty w korpusie: stan prawny i tekst jednolity (z data/corpus/*.json i results/law_watch.json). */
export interface ActInfo {
  key: "vat" | "pit" | "op";
  label: string;
  title: string;
  dzu: string;
  stateDate: string;
}

export const ACTS: ActInfo[] = [
  { key: "vat", label: "VAT", title: "Ustawa o podatku od towarów i usług", dzu: "Dz.U. 2026 poz. 1263", stateDate: "2026-08-26" },
  { key: "pit", label: "PIT", title: "Ustawa o podatku dochodowym od osób fizycznych", dzu: "Dz.U. 2026 poz. 592", stateDate: "2026-04-01" },
  { key: "op", label: "Ordynacja", title: "Ordynacja podatkowa", dzu: "Dz.U. 2026 poz. 622", stateDate: "2026-04-21" },
];

export function actOf(address: string): ActInfo | undefined {
  const first = address.trim().split(/\s+/)[0];
  return ACTS.find((a) => a.label === first);
}

export function formatDate(iso: string): string {
  const [y, m, d] = iso.split("-");
  return `${d}.${m}.${y}`;
}

const STATUS_LABEL: Record<string, string> = {
  in_force: "obowiązuje",
  historical: "historyczny",
  conditional: "warunkowy",
};
export function statusLabel(s: string | null | undefined): string {
  if (!s) return "status nieznany";
  return STATUS_LABEL[s] ?? s;
}

/** Adnotacja o przepisie przejściowym albo wartości zastąpionej: jedyne miejsce, gdzie używamy miodu. */
export function isTransitional(note: string | null | undefined): boolean {
  if (!note) return false;
  const n = note.toLowerCase();
  return n.includes("przejściow") || n.startsWith("uwaga") || n.includes("zastąpion");
}

// ── dopasowanie cytatu do bloku kontekstu ────────────────────────────────
// Cytat bywa dokładniejszy niż blok („VAT art. 146ef ust. 1 pkt 1” → blok „VAT art. 146ef”)
// albo trafia w zakres („PIT art. 21 ust. 1 pkt 127 lit. b” → blok „PIT art. 21 ust. 1 pkt 125–129a”).

type Part = { label: string; value: string };

function parse(address: string): { act: string; parts: Part[] } {
  const toks = address.trim().split(/\s+/);
  const act = toks[0] ?? "";
  const parts: Part[] = [];
  for (let i = 1; i < toks.length - 1; i += 2) parts.push({ label: toks[i], value: toks[i + 1] });
  return { act, parts };
}

function key(v: string): [number, string] {
  const m = v.match(/^(\d+)([a-z]*)$/i);
  return m ? [Number(m[1]), m[2].toLowerCase()] : [Number.NaN, v.toLowerCase()];
}
function cmp(a: string, b: string): number {
  const [an, as] = key(a);
  const [bn, bs] = key(b);
  if (Number.isNaN(an) || Number.isNaN(bn)) return a.localeCompare(b);
  return an !== bn ? an - bn : as.localeCompare(bs);
}
function inRange(blockValue: string, citeValue: string): boolean {
  const range = blockValue.split(/[–-]/);
  if (range.length === 2) return cmp(citeValue, range[0]) >= 0 && cmp(citeValue, range[1]) <= 0;
  return blockValue === citeValue;
}

/** Ile poziomów adresu się zgadza (−1 = nie pasuje). */
function matchDepth(block: string, cite: string): number {
  const b = parse(block);
  const c = parse(cite);
  if (b.act !== c.act) return -1;
  let depth = 0;
  for (let i = 0; i < b.parts.length; i++) {
    const bp = b.parts[i];
    const cp = c.parts[i];
    if (!cp) return depth; // blok dokładniejszy niż cytat: cytat obejmuje blok
    if (bp.label !== cp.label || !inRange(bp.value, cp.value)) return -1;
    depth++;
  }
  return depth;
}

export function findBlock(cite: string, blocks: ContextBlock[]): number {
  let best = -1;
  let bestDepth = -1;
  blocks.forEach((blk, i) => {
    const d = matchDepth(blk.address, cite);
    if (d > bestDepth) {
      best = i;
      bestDepth = d;
    }
  });
  return bestDepth >= 1 ? best : -1;
}

/** Adres z identyfikatora fragmentu wyszukiwarki: „pit:PIT art. 27f ust. 4:933” → „PIT art. 27f ust. 4”. */
export function addressFromChunk(id: string): { address: string; chunk?: string } {
  const m = id.match(/^[a-z]+:(.+):(\d+)$/);
  return m ? { address: m[1], chunk: m[2] } : { address: id };
}
