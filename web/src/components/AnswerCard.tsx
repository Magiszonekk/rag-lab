import type { Category, VariantAnswer, VariantId } from "../lib/types";
import { VARIANT_INFO } from "../lib/labels";
import { fmtInt, fmtSec } from "../lib/format";
import { findBlock } from "../lib/law";
import { AnswerText } from "./AnswerText";
import { Disclosure, VerdictBadge } from "./Bits";
import { Icon } from "./Icon";

export function agentAdded(a: VariantAnswer): string[] {
  return a.steps.filter((s) => s.kind === "get" || s.kind === "search").flatMap((s) => (Array.isArray(s.attrs.added) ? (s.attrs.added as string[]) : []));
}

export function Metrics({ a, compact = false }: { a: VariantAnswer; compact?: boolean }) {
  return (
    <dl className={`metrics${compact ? " is-compact" : ""}`}>
      <div title="Tokeny wejścia + wyjścia (z pętlą agenta)">
        <dt><Icon name="tokens" size={14} />tokeny</dt>
        <dd>{fmtInt(a.tokens)}</dd>
      </div>
      <div title="Czas od pytania do odpowiedzi (bez weryfikacji)">
        <dt><Icon name="clock" size={14} />czas</dt>
        <dd>{fmtSec(a.latency_ms)}</dd>
      </div>
      <div title="Przepisy, które model dostał w kontekście">
        <dt><Icon name="context" size={14} />przepisy</dt>
        <dd>{a.context.length}</dd>
      </div>
    </dl>
  );
}

export function AnswerCard({
  answer,
  variant,
  category,
  activeBlock,
  onCite,
  showVerify,
  live,
}: {
  answer: VariantAnswer;
  variant: VariantId;
  category: Category;
  activeBlock: number | null;
  onCite: (i: number) => void;
  showVerify: boolean;
  live?: boolean;
}) {
  const added = agentAdded(answer);
  const v = answer.verify;
  return (
    <article className={`answer-card${answer.refused ? " is-refused" : ""}`} aria-live="polite">
      <header className="answer-head">
        <div className="answer-title">
          <h2>{VARIANT_INFO[variant].name}</h2>
          <span className="answer-sub">{VARIANT_INFO[variant].short}</span>
        </div>
        {!live && <VerdictBadge answer={answer} category={category} />}
        {live && answer.cached && <span className="chip">z pamięci podręcznej</span>}
      </header>

      {answer.refused && (
        <p className="refusal-note">
          <Icon name="refuse" size={16} />
          System odmówił odpowiedzi: w kontekście nie było przepisu, który by na nią pozwalał.
        </p>
      )}

      <AnswerText text={answer.answer} citations={answer.citations} blocks={answer.context} activeBlock={activeBlock} onCite={onCite} />

      {answer.citations.length > 0 && (
        <div className="cites">
          <h3>Cytowane przepisy</h3>
          <ul>
            {answer.citations.map((c) => {
              const i = findBlock(c, answer.context);
              return (
                <li key={c}>
                  {i >= 0 ? (
                    <button type="button" className={`cite-chip${activeBlock === i ? " is-active" : ""}`} onClick={() => onCite(i)}>
                      <span className="cite-n">{i + 1}</span>
                      {c}
                    </button>
                  ) : (
                    <span className="cite-chip is-missing" title="Tego adresu nie ma w kontekście">{c}</span>
                  )}
                </li>
              );
            })}
          </ul>
        </div>
      )}

      {added.length > 0 && (
        <p className="agent-note">
          <Icon name="get" size={16} />
          <span>
            Agent dociągnął: <strong>{added.join(", ")}</strong>
          </span>
        </p>
      )}

      {showVerify && v && v.verdict === "fix" && v.unsupported.length > 0 && (
        <div className="verify-box">
          <h3><Icon name="verify" size={15} /> Weryfikacja usunęła {v.unsupported.length === 1 ? "zdanie" : "zdania"} bez oparcia w przepisach</h3>
          <ul>
            {v.unsupported.map((s) => (
              <li key={s}><del>{s}</del></li>
            ))}
          </ul>
        </div>
      )}
      {showVerify && v && v.verdict === "pass" && (
        <p className="verify-ok"><Icon name="verify" size={15} /> Weryfikacja: każde zdanie ma oparcie w przytoczonych przepisach.</p>
      )}

      <footer className="answer-foot">
        <Metrics a={answer} />
        {answer.judge?.reason && (
          <Disclosure className="judge" summary="Uzasadnienie sędziego">
            <p>{answer.judge.reason}</p>
          </Disclosure>
        )}
      </footer>
    </article>
  );
}
