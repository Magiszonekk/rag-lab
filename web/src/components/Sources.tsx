import { useEffect, useRef } from "react";
import type { ContextBlock } from "../lib/types";
import { actOf, formatDate, isTransitional, statusLabel, findBlock } from "../lib/law";
import { Icon } from "./Icon";

/** Lista przepisów z kontekstu: adres, stan prawny, status, adnotacja; tekst przepisu po rozwinięciu. */
export function Sources({
  blocks,
  citations,
  open,
  onToggle,
  added,
}: {
  blocks: ContextBlock[];
  citations: string[];
  open: number | null;
  onToggle: (i: number | null) => void;
  /** adresy dociągnięte przez agenta (get/search) */
  added?: Set<string>;
}) {
  const refs = useRef<(HTMLLIElement | null)[]>([]);
  const cited = new Set(citations.map((c) => findBlock(c, blocks)).filter((i) => i >= 0));

  useEffect(() => {
    if (open == null) return;
    const el = refs.current[open];
    if (!el) return;
    const r = el.getBoundingClientRect();
    if (r.top < 80 || r.top > window.innerHeight - 120) el.scrollIntoView({ block: "start", behavior: "smooth" });
  }, [open]);

  if (!blocks.length)
    return <p className="empty">Brak przepisów w kontekście. Pytanie zostało odrzucone przed wyszukiwaniem.</p>;

  return (
    <ol className="sources">
      {blocks.map((b, i) => {
        const act = actOf(b.address);
        const isOpen = open === i;
        const trans = isTransitional(b.note);
        return (
          <li key={b.address + i} ref={(el) => { refs.current[i] = el; }} className={`source${isOpen ? " is-open" : ""}${cited.has(i) ? " is-cited" : ""}`} id={`src-${i}`}>
            <button type="button" className="source-head" aria-expanded={isOpen} onClick={() => onToggle(isOpen ? null : i)}>
              <span className="source-n" aria-hidden="true">{i + 1}</span>
              <span className="source-main">
                <span className="source-addr">{b.address}</span>
                <span className="source-meta">
                  <span className={`status status-${b.status ?? "unknown"}`}>{statusLabel(b.status)}</span>
                  {act && <span>stan prawny {formatDate(act.stateDate)}</span>}
                  {cited.has(i) && <span className="tag-cited">cytowany</span>}
                  {added?.has(b.address) && <span className="tag-added">dociągnięty przez agenta</span>}
                </span>
                {b.note && (
                  <span className={`source-note${trans ? " is-transitional" : ""}`}>
                    {trans && <Icon name="hourglass" size={14} />}
                    {b.note}
                  </span>
                )}
              </span>
              <Icon name="chevron" size={18} className="source-chev" />
            </button>
            {isOpen && (
              <div className="source-body">
                <div className="law-text">{b.text}</div>
                {act && (
                  <p className="source-foot">
                    {act.title}, tekst jednolity {act.dzu}
                  </p>
                )}
              </div>
            )}
          </li>
        );
      })}
    </ol>
  );
}
