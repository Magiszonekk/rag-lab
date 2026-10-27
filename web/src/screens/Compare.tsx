import { useState } from "react";
import type { Category, ExamplesFile, VariantAnswer, VariantId } from "../lib/types";
import { VARIANTS } from "../lib/types";
import { compare, ApiError, type ApiState } from "../lib/api";
import { setParams, href } from "../lib/route";
import { VARIANT_INFO, verdictLabel } from "../lib/labels";
import { AnswerText } from "../components/AnswerText";
import { agentAdded, Metrics } from "../components/AnswerCard";
import { Disclosure, ExamplePicker, Notice, Switch, VerdictBadge } from "../components/Bits";
import { Icon } from "../components/Icon";
import { Sources } from "../components/Sources";
import { liveNotice } from "./Ask";

function headline(answers: Record<VariantId, VariantAnswer>, category: Category): string | null {
  const ok = (v: VariantId) => verdictLabel(answers[v].judge?.verdict, category).tone === "ok";
  const added = agentAdded(answers["agentic-strict"]);
  const others = VARIANTS.filter((v) => v !== "agentic-strict");
  const failed = others.filter((v) => !ok(v));
  if (category === "out_of_corpus") return "Pytanie spoza korpusu: wszystkie warianty powinny odmówić i żaden nie odpowiada z pamięci modelu.";
  if (added.length && ok("agentic-strict") && failed.length)
    return `${failed.map((v) => VARIANT_INFO[v].name).join(", ")}: kluczowego przepisu nie było w top-5. Agent go dociągnął (${added.slice(0, 3).join(", ")}${added.length > 3 ? "…" : ""}) i odpowiedział.`;
  if (VARIANTS.every(ok)) return "Wszystkie warianty odpowiadają poprawnie; różnią się kosztem i czasem.";
  return null;
}

function Column({
  v,
  a,
  category,
  showVerify,
  best,
  open,
  setOpen,
  live,
}: {
  v: VariantId;
  a: VariantAnswer;
  category: Category;
  showVerify: boolean;
  best: { tokens: number; time: number };
  open: number | null;
  setOpen: (i: number | null) => void;
  live: boolean;
}) {
  const added = agentAdded(a);
  const tone = verdictLabel(a.judge?.verdict, category).tone;
  return (
    <article className={`cmp-col tone-${live ? "none" : tone}${a.refused ? " is-refused" : ""}`}>
      <header className="cmp-head">
        <h3>{VARIANT_INFO[v].name}</h3>
        <span className="answer-sub">{VARIANT_INFO[v].short}</span>
      </header>
      <div className="cmp-verdict">{!live ? <VerdictBadge answer={a} category={category} /> : <span className="chip">na żywo</span>}</div>
      <div className="cmp-metrics">
        <Metrics a={a} compact />
        <span className="cmp-best">
          {a.tokens === best.tokens && <span>najmniej tokenów</span>}
          {a.latency_ms === best.time && <span>najszybszy</span>}
        </span>
      </div>
      <div className="cmp-body">
        {added.length > 0 ? (
          <p className="agent-note">
            <Icon name="get" size={16} />
            <span>Dociągnął: <strong>{added.join(", ")}</strong></span>
          </p>
        ) : (
          <span className="cmp-noagent" aria-hidden="true" />
        )}
        <AnswerText text={a.answer} citations={a.citations} blocks={a.context} activeBlock={open} onCite={(i) => setOpen(i)} />
        {showVerify && a.verify?.verdict === "fix" && (
          <div className="verify-box">
            <h4><Icon name="verify" size={14} /> Usunięte przy sprawdzaniu</h4>
            <ul>{a.verify.unsupported.map((s) => <li key={s}><del>{s}</del></li>)}</ul>
          </div>
        )}
      </div>
      <footer className="cmp-foot">
        {a.judge?.reason && (
          <Disclosure className="judge" summary="Uzasadnienie sędziego">
            <p>{a.judge.reason}</p>
          </Disclosure>
        )}
        <Disclosure key={a.answer.slice(0, 24)} className="judge" summary={`Przepisy w kontekście (${a.context.length})`}>
          <Sources blocks={a.context} citations={a.citations} open={open} onToggle={setOpen} added={new Set(added)} />
        </Disclosure>
      </footer>
    </article>
  );
}

export function CompareScreen({ data, api, params }: { data: ExamplesFile; api: ApiState; params: URLSearchParams }) {
  const exId = params.get("ex") ?? "g-vat-07";
  const verify = params.get("verify") === "on";
  const ex = data.examples.find((e) => e.id === exId) ?? data.examples[0];
  const live = api.kind === "live";
  const [question, setQuestion] = useState("");
  const [liveRes, setLiveRes] = useState<{ q: string; answers: Record<VariantId, VariantAnswer> } | null>(null);
  const [busy, setBusy] = useState(false);
  const [err, setErr] = useState<string | null>(null);
  const [mode, setMode] = useState<"example" | "live">("example");
  const [opens, setOpens] = useState<Record<string, number | null>>({});

  const showLive = mode === "live" && liveRes;
  const answers = showLive ? liveRes.answers : ex.variants;
  const category = showLive ? "live" : ex.category;
  const tokens = VARIANTS.map((v) => answers[v].tokens ?? Infinity);
  const times = VARIANTS.map((v) => answers[v].latency_ms ?? Infinity);
  const best = { tokens: Math.min(...tokens), time: Math.min(...times) };
  const line = showLive ? null : headline(ex.variants, ex.category);

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    const q = question.trim();
    if (!live || q.length < 5 || busy) return;
    setBusy(true);
    setErr(null);
    try {
      const r = await compare(q, verify);
      setLiveRes({ q, answers: r });
      setMode("live");
    } catch (x) {
      setErr((x as Error).message + (x instanceof ApiError && x.status === 429 ? "" : " Gotowe przykłady działają bez serwera."));
    } finally {
      setBusy(false);
    }
  }
  const notice = liveNotice(api);

  return (
    <div className="page page-wide">
      <section className="screen-head">
        <h1>Jedno pytanie, cztery warianty</h1>
        <p className="lead">
          Ten sam model, ten sam prompt i ten sam korpus. Różni się tylko sposób szukania przepisów. Obok odpowiedzi: ocena sędziego (inna rodzina modeli), tokeny i czas.
        </p>
      </section>

      {live && (
        <form className="ask-form is-inline" onSubmit={submit}>
          <label htmlFor="cq" className="sr-only">Pytanie do porównania</label>
          <div className="ask-input">
            <textarea id="cq" rows={1} maxLength={600} placeholder="Wpisz pytanie, żeby porównać warianty na żywo (liczy się jak 4 pytania w limicie)" value={question} onChange={(e) => setQuestion(e.target.value)} disabled={busy} />
            <button type="submit" className="btn btn-primary" disabled={busy || question.trim().length < 5}>
              {busy ? <><span className="spinner" /> Cztery odpowiedzi…</> : <>Porównaj <Icon name="arrow" size={18} /></>}
            </button>
          </div>
        </form>
      )}
      {notice && !live && <Notice icon="info">{notice}</Notice>}
      {err && <Notice tone="danger">{err}</Notice>}

      <div className="cmp-picker">
        <ExamplePicker examples={data.examples} value={showLive ? null : ex.id} onChange={(id) => { setMode("example"); setOpens({}); setParams("porownaj", { ex: id, verify: verify ? "on" : undefined }); }} compact />
        <Switch checked={verify} onChange={(v) => setParams("porownaj", { ex: ex.id, verify: v ? "on" : undefined })} label="Pokaż wynik sprawdzania" />
      </div>

      <div className="question-line">
        <span className="q-label">Pytanie</span>
        <p className="q-text">{showLive ? liveRes.q : ex.question}</p>
        {line && <p className="cmp-headline"><Icon name="info" size={17} />{line}</p>}
      </div>

      <div className="cmp-grid">
        {VARIANTS.map((v) => (
          <Column key={v} v={v} a={answers[v]} category={category} showVerify={verify} best={best} open={opens[v] ?? null} setOpen={(i) => setOpens((o) => ({ ...o, [v]: i }))} live={!!showLive} />
        ))}
      </div>

      {!showLive && ex.reference_answer && (
        <Disclosure key={ex.id} className="reference" summary="Odpowiedź wzorcowa ze złotego zestawu">
          <p>{ex.reference_answer}</p>
        </Disclosure>
      )}
      {!showLive && (
        <p className="next-link">
          <a href={href("slad", { ex: ex.id, v: "agentic-strict" })}>Zobacz krok po kroku, co zrobił agent <Icon name="arrow" size={15} /></a>
        </p>
      )}
    </div>
  );
}
