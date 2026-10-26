import type { ExamplesFile, VariantId } from "../lib/types";
import { VARIANTS } from "../lib/types";
import { setParams, href } from "../lib/route";
import { VARIANT_INFO } from "../lib/labels";
import { ExamplePicker, VariantPicker, VerdictBadge } from "../components/Bits";
import { Trace } from "../components/Trace";
import { Metrics } from "../components/AnswerCard";
import { stripCitationTail } from "../components/AnswerText";
import { Icon } from "../components/Icon";

export function TraceScreen({ data, params }: { data: ExamplesFile; params: URLSearchParams }) {
  const exId = params.get("ex") ?? "g-vat-26";
  const variant = (VARIANTS.includes(params.get("v") as VariantId) ? params.get("v") : "agentic-strict") as VariantId;
  const ex = data.examples.find((e) => e.id === exId) ?? data.examples[0];
  const a = ex.variants[variant];
  const upd = (p: { ex?: string; v?: VariantId }) => setParams("slad", { ex: p.ex ?? ex.id, v: p.v ?? variant });

  return (
    <div className="page">
      <section className="screen-head">
        <h1>Ślad odpowiedzi</h1>
        <p className="lead">
          Każdy krok, który system wykonał: co znalazła wyszukiwarka, o co poprosił agent i dlaczego, co trafiło do modelu, ile to kosztowało i co usunęła weryfikacja.
        </p>
      </section>

      <div className="trace-controls">
        <ExamplePicker examples={data.examples} value={ex.id} onChange={(id) => upd({ ex: id })} compact />
        <div className="control">
          <span className="control-label">Wariant</span>
          <VariantPicker value={variant} onChange={(v) => upd({ v })} />
        </div>
      </div>

      <div className="trace-layout">
        <div className="trace-main">
          <div className="question-line">
            <span className="q-label">Pytanie</span>
            <p className="q-text">{ex.question}</p>
          </div>
          <Trace answer={a} />
        </div>
        <aside className="trace-side">
          <div className="side-card">
            <div className="side-head">
              <h2>{VARIANT_INFO[variant].name}</h2>
              <VerdictBadge answer={a} category={ex.category} />
            </div>
            <Metrics a={a} />
            <h3>Odpowiedź końcowa</h3>
            <p className="side-answer">{stripCitationTail(a.answer)}</p>
            <a className="side-link" href={href("zapytaj", { ex: ex.id, v: variant })}>Otwórz z przepisami <Icon name="arrow" size={15} /></a>
          </div>
        </aside>
      </div>
    </div>
  );
}
