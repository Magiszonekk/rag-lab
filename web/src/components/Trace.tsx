import type { Step, VariantAnswer } from "../lib/types";
import { addressFromChunk } from "../lib/law";
import { fmtInt, fmtSec } from "../lib/format";
import { Icon } from "./Icon";

const arr = (x: unknown): string[] => (Array.isArray(x) ? x.map(String) : []);
const num = (x: unknown): number | undefined => (typeof x === "number" ? x : undefined);

const KIND: Record<string, { title: string; icon: string }> = {
  retrieve: { title: "Wyszukiwanie", icon: "search" },
  get: { title: "Agent: pobierz po adresie", icon: "get" },
  search: { title: "Agent: szukaj ponownie", icon: "research" },
  context: { title: "Kontekst dla modelu", icon: "context" },
  generate: { title: "Generowanie odpowiedzi", icon: "generate" },
  verify: { title: "Weryfikacja zdanie po zdaniu", icon: "verify" },
};

function Addrs({ items, tone }: { items: string[]; tone?: "add" | "miss" }) {
  if (!items.length) return null;
  return (
    <ul className={`addr-list${tone ? ` tone-${tone}` : ""}`}>
      {items.map((a) => (
        <li key={a}>{a}</li>
      ))}
    </ul>
  );
}

function StepBody({ step }: { step: Step }) {
  const a = step.attrs;
  switch (step.kind) {
    case "retrieve": {
      const added = arr(a.added);
      const retrieved = arr(a.retrieved).map((id) => addressFromChunk(id).address);
      const list = added.length ? added : retrieved;
      return (
        <>
          <p className="step-lead">Top-{list.length} fragmentów z wyszukiwarki, zanim model cokolwiek zobaczy.</p>
          <Addrs items={list} />
        </>
      );
    }
    case "get":
    case "search": {
      const asked = arr(a.asked);
      const added = arr(a.added);
      const missing = arr(a.not_found);
      return (
        <>
          {typeof a.why === "string" && <blockquote className="step-why">{a.why}</blockquote>}
          {step.kind === "search" && typeof a.query === "string" && (
            <p className="step-kv"><span>zapytanie</span><code>{a.query}</code></p>
          )}
          {step.kind === "get" && asked.length > 0 && (
            <p className="step-kv"><span>prosi o</span><code>{asked.join(", ")}</code></p>
          )}
          {added.length > 0 && <p className="step-sub">Dodane do kontekstu</p>}
          <Addrs items={added} tone="add" />
          {missing.length > 0 && <p className="step-sub">Odrzucone przez tryb ścisły</p>}
          <Addrs items={missing} tone="miss" />
        </>
      );
    }
    case "context": {
      const blocks = Array.isArray(a.blocks) ? (a.blocks as { address: string; note?: string; chars?: number }[]) : [];
      const total = blocks.reduce((s, b) => s + (b.chars ?? 0), 0);
      return (
        <>
          <p className="step-lead">
            {blocks.length} {blocks.length === 1 ? "przepis" : blocks.length < 5 ? "przepisy" : "przepisów"}, {fmtInt(total)} znaków. Przepisy przejściowe dołączane są z adnotacją.
          </p>
          <ul className="ctx-bars">
            {blocks.map((b) => (
              <li key={b.address}>
                <span className="ctx-addr">{b.address}</span>
                <span className="ctx-bar" aria-hidden="true">
                  <span style={{ width: `${Math.max(4, Math.round(((b.chars ?? 0) / Math.max(1, ...blocks.map((x) => x.chars ?? 0))) * 100))}%` }} />
                </span>
                <span className="ctx-chars">{fmtInt(b.chars)} zn.</span>
                {b.note && <span className="ctx-note"><Icon name="hourglass" size={13} />{b.note}</span>}
              </li>
            ))}
          </ul>
        </>
      );
    }
    case "generate": {
      const lat = (a.latency_ms ?? {}) as Record<string, number>;
      const LAT: Record<string, string> = { retrieval: "wyszukiwanie", agent: "pętla agenta", generation: "generowanie" };
      return (
        <dl className="step-dl">
          <div><dt>model</dt><dd><code>{String(a.model ?? "—")}</code></dd></div>
          <div><dt>tokeny wejścia</dt><dd>{fmtInt(num(a.prompt_tokens))}</dd></div>
          <div><dt>tokeny wyjścia</dt><dd>{fmtInt(num(a.completion_tokens))}</dd></div>
          {Object.entries(lat).map(([k, v]) => (
            <div key={k}><dt>{LAT[k] ?? k}</dt><dd>{fmtSec(v)}</dd></div>
          ))}
        </dl>
      );
    }
    case "verify": {
      const uns = arr(a.unsupported);
      const v = String(a.verdict ?? "");
      return (
        <>
          <p className="step-lead">
            {v === "pass" && "Każde zdanie ma oparcie w przepisach z kontekstu. Odpowiedź bez zmian."}
            {v === "fix" && `Usunięte ${uns.length === 1 ? "zdanie" : "zdania"} bez oparcia w kontekście. Reszta odpowiedzi zostaje.`}
            {v === "fail" && "Główna teza bez oparcia w kontekście: odpowiedź zamieniona na odmowę."}
            {v === "error" && "Weryfikator niedostępny, odpowiedź pokazana bez sprawdzenia."}
          </p>
          {uns.length > 0 && (
            <ul className="removed">
              {uns.map((s) => (
                <li key={s}><del>{s}</del></li>
              ))}
            </ul>
          )}
        </>
      );
    }
    default:
      return <pre className="step-raw">{JSON.stringify(a, null, 2)}</pre>;
  }
}

function stepTag(step: Step): { text: string; tone?: string } | null {
  if (step.kind === "verify") {
    const v = String(step.attrs.verdict);
    if (v === "pass") return { text: "bez zmian", tone: "ok" };
    if (v === "fix") return { text: "przycięta", tone: "warn" };
    if (v === "fail") return { text: "zablokowana", tone: "bad" };
  }
  if (step.kind === "get" || step.kind === "search") {
    const n = arr(step.attrs.added).length;
    return { text: `+${n}`, tone: "add" };
  }
  return null;
}

export function Trace({ answer, verifyOff }: { answer: VariantAnswer; verifyOff?: boolean }) {
  const steps = answer.steps;
  const hasVerify = steps.some((s) => s.kind === "verify");
  return (
    <ol className="trace">
      {steps.map((s, i) => {
        const k = KIND[s.kind] ?? { title: s.kind, icon: "spark" };
        const tag = stepTag(s);
        const agent = s.kind === "get" || s.kind === "search";
        return (
          <li key={i} className={`trace-step kind-${s.kind}${agent ? " is-agent" : ""}`}>
            <span className="trace-dot" aria-hidden="true"><Icon name={k.icon} size={16} /></span>
            <div className="trace-card">
              <h4>
                {k.title}
                {tag && <span className={`step-tag tone-${tag.tone}`}>{tag.text}</span>}
              </h4>
              <StepBody step={s} />
            </div>
          </li>
        );
      })}
      {!hasVerify && (
        <li className="trace-step kind-verify is-skipped">
          <span className="trace-dot" aria-hidden="true"><Icon name="verify" size={16} /></span>
          <div className="trace-card">
            <h4>Weryfikacja</h4>
            <p className="step-lead">
              {verifyOff ? "Wyłączona przełącznikiem." : answer.refused ? "Pominięta: odmowy nie są weryfikowane, nie ma czego sprawdzać." : "Nie uruchomiono."}
            </p>
          </div>
        </li>
      )}
    </ol>
  );
}
