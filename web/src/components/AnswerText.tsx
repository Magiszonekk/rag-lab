import { Fragment, type ReactNode } from "react";
import type { ContextBlock } from "../lib/types";
import { findBlock } from "../lib/law";

/** Usuwa dopisek „(cytaty: …)”, który model dokleja na końcu — cytaty pokazujemy osobno. */
export function stripCitationTail(text: string): string {
  return text.replace(/\n?\s*\(cytaty:[^)]*\)\s*$/i, "").trim();
}

const ACT_WORD = /(VAT|PIT|Ordynacj[ai])\s+(?=art\.)/;
const REF = /((?:VAT|PIT|Ordynacja)\s+)?art\.\s*\d+[a-z]*(?:\s+(?:ust\.|§)\s*\d+[a-z]*)?(?:\s+pkt\s*\d+[a-z]*)?(?:\s+lit\.\s*[a-z]\b)?/g;

function defaultAct(citations: string[], blocks: ContextBlock[]): string | null {
  const acts = new Set([...citations, ...blocks.map((b) => b.address)].map((a) => a.split(/\s+/)[0]));
  return acts.size === 1 ? [...acts][0] : null;
}

/**
 * Tekst odpowiedzi z klikalnymi odwołaniami do przepisów, które są w kontekście.
 * Odwołanie bez nazwy ustawy przypisujemy ustawie, jeśli cały kontekst dotyczy jednej.
 */
export function AnswerText({
  text,
  citations,
  blocks,
  activeBlock,
  onCite,
}: {
  text: string;
  citations: string[];
  blocks: ContextBlock[];
  activeBlock: number | null;
  onCite: (blockIndex: number) => void;
}) {
  const clean = stripCitationTail(text);
  const fallbackAct = defaultAct(citations, blocks);
  const paragraphs = clean.split(/\n+/).filter(Boolean);

  const renderPara = (p: string, pi: number) => {
    const out: ReactNode[] = [];
    let last = 0;
    for (const m of p.matchAll(REF)) {
      const start = m.index ?? 0;
      const raw = m[0];
      let addr = raw.replace(/\s+/g, " ").replace(/^Ordynacji?\s/, "Ordynacja ");
      if (!m[1]) {
        const before = p.slice(Math.max(0, start - 16), start);
        const named = before.match(ACT_WORD);
        const act = named ? named[1].replace(/^Ordynacj[ai]$/, "Ordynacja") : fallbackAct;
        if (!act) continue;
        addr = `${act} ${addr}`;
      }
      const idx = findBlock(addr, blocks);
      if (idx < 0) continue;
      out.push(p.slice(last, start));
      out.push(
        <button
          key={`${pi}-${start}`}
          type="button"
          className={`cite-inline${activeBlock === idx ? " is-active" : ""}`}
          onClick={() => onCite(idx)}
          title={`Pokaż przepis: ${blocks[idx].address}`}
        >
          {raw}
        </button>,
      );
      last = start + raw.length;
    }
    out.push(p.slice(last));
    return <p key={pi}>{out.map((x, i) => (typeof x === "string" ? <Fragment key={i}>{x}</Fragment> : x))}</p>;
  };

  return <div className="answer-text">{paragraphs.map(renderPara)}</div>;
}
