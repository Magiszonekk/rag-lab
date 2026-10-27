import { useEffect, useState } from "react";
import type { ExamplesFile, VariantAnswer, VariantId } from "../lib/types";
import { VARIANTS } from "../lib/types";
import { askStream, ApiError, type ApiState, type StreamEvent } from "../lib/api";
import { setParams, href } from "../lib/route";
import { VARIANT_INFO } from "../lib/labels";
import { AnswerCard, agentAdded } from "../components/AnswerCard";
import { Sources } from "../components/Sources";
import { ExamplePicker, Notice, Switch, VariantPicker } from "../components/Bits";
import { Icon } from "../components/Icon";

export function liveNotice(api: ApiState): string | null {
  if (api.kind === "none") return "Ta wersja demo działa bez serwera: pokazuje zapisane odpowiedzi z ewaluacji. Wybierz przykład.";
  if (api.kind === "down") return "Serwer demo nie odpowiada, więc pytania na żywo są niedostępne. Gotowe przykłady działają normalnie.";
  if (api.kind === "examples-only") return "Pytania na żywo są chwilowo wyłączone. Gotowe przykłady działają normalnie.";
  return null;
}

export function AskScreen({ data, api, params }: { data: ExamplesFile; api: ApiState; params: URLSearchParams }) {
  const exId = params.get("ex") ?? data.examples[1]?.id ?? data.examples[0].id;
  const variant = (VARIANTS.includes(params.get("v") as VariantId) ? params.get("v") : "simple") as VariantId;
  const verify = params.get("verify") === "on"; // sprawdzanie zdanie po zdaniu na żądanie (+~8 s)
  const live = api.kind === "live";

  const [mode, setMode] = useState<"example" | "live">("example");
  const [question, setQuestion] = useState("");
  const [liveAnswer, setLiveAnswer] = useState<VariantAnswer | null>(null);
  const [liveMeta, setLiveMeta] = useState<{ variant: VariantId; verify: boolean } | null>(null);
  const [busy, setBusy] = useState(false);
  const [progress, setProgress] = useState<{ stage: string; text: string; found: number } | null>(null);
  const [err, setErr] = useState<string | null>(null);
  const [open, setOpen] = useState<number | null>(null);

  const ex = data.examples.find((e) => e.id === exId) ?? data.examples[0];
  const showLive = mode === "live" && liveAnswer && liveMeta;
  const answer = showLive ? liveAnswer : ex.variants[variant];
  const shownVariant = showLive ? liveMeta.variant : variant;

  useEffect(() => setOpen(null), [exId, variant, liveAnswer]);

  const upd = (p: Partial<{ ex: string; v: VariantId; verify: boolean }>) =>
    setParams("zapytaj", { ex: p.ex ?? exId, v: p.v ?? variant, verify: (p.verify ?? verify) ? "on" : undefined });

  async function submit(e: React.FormEvent) {
    e.preventDefault();
    const q = question.trim();
    if (!live || q.length < 5 || busy) return;
    setBusy(true);
    setErr(null);
    setProgress({ stage: "Szukam przepisów w ustawach…", text: "", found: 0 });
    const onEvent = (e: StreamEvent) =>
      setProgress((p) => {
        const cur = p ?? { stage: "", text: "", found: 0 };
        if (e.type === "answer") return { ...cur, text: e.text, stage: "Piszę odpowiedź…" };
        if (e.type === "context") return { ...cur, found: e.addresses.length, stage: `Mam ${e.addresses.length} przepisów, piszę odpowiedź…` };
        if (e.type === "step" && e.step === "get") return { ...cur, stage: `Agent dociąga: ${(e.added ?? []).join(", ") || "brakujący przepis"}…` };
        if (e.type === "step" && e.step === "search") return { ...cur, stage: `Agent szuka ponownie: „${e.query ?? ""}”…` };
        if (e.type === "step") return { ...cur, stage: "Agent czyta znalezione przepisy…" };
        if (e.type === "stage" && e.stage === "verify") return { ...cur, stage: "Sprawdzam zdanie po zdaniu…" };
        return cur;
      });
    try {
      const a = await askStream(q, variant, verify, onEvent);
      if (a.error) throw new ApiError(500, a.error);
      setLiveAnswer(a);
      setLiveMeta({ variant, verify });
      setMode("live");
    } catch (x) {
      const status = x instanceof ApiError ? x.status : 0;
      setErr((x as Error).message + (status === 429 || status === 503 ? "" : " Gotowe przykłady poniżej działają bez serwera."));
    } finally {
      setBusy(false);
      setProgress(null);
    }
  }

  const notice = liveNotice(api);
  const added = new Set(agentAdded(answer));

  return (
    <div className="page">
      <section className="ask-hero">
        <h1>Zadaj pytanie o VAT, PIT albo Ordynację podatkową</h1>
        <p className="lead">
          Odpowiedź powstaje wyłącznie z przepisów, które system znalazł w trzech ustawach. Każde twierdzenie ma adres przepisu; kliknij go, żeby zobaczyć tekst ustawy i stan prawny.
        </p>

        <form className="ask-form" onSubmit={submit}>
          <label htmlFor="q" className="sr-only">Pytanie</label>
          <div className="ask-input">
            <textarea
              id="q"
              rows={2}
              maxLength={600}
              placeholder={live ? "Np. Czy jako freelancer muszę mieć kasę fiskalną?" : "Pytania na żywo są tu niedostępne. Wybierz gotowy przykład poniżej."}
              value={live ? question : ""}
              onChange={(e) => setQuestion(e.target.value)}
              disabled={!live || busy}
              onKeyDown={(e) => {
                if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) (e.currentTarget.form as HTMLFormElement).requestSubmit();
              }}
            />
            <button type="submit" className="btn btn-primary" disabled={!live || busy || question.trim().length < 5}>
              {busy ? <><span className="spinner" /> Szukam w ustawach…</> : <>Zapytaj <Icon name="arrow" size={18} /></>}
            </button>
          </div>
          <div className="ask-controls">
            <div className="control">
              <span className="control-label" id="variant-label">Wariant</span>
              <VariantPicker value={variant} onChange={(v) => upd({ v })} />
            </div>
            <Switch checked={verify} onChange={(v) => upd({ verify: v })} label="Sprawdzanie odpowiedzi" hint="usuwa zdania bez oparcia w przepisach" />
          </div>
          <p className="variant-how">{VARIANT_INFO[variant].how}</p>
        </form>

        {notice && <Notice icon="info">{notice}</Notice>}
        {busy && progress && (
          <article className="answer-card" aria-live="polite" aria-busy="true">
            <p className="hint-line"><span className="spinner" /> {progress.stage}</p>
            {progress.text && <div className="answer-text"><p>{progress.text}</p></div>}
          </article>
        )}
        {err && <Notice tone="danger">{err}</Notice>}
      </section>

      <section className="examples-row" aria-labelledby="ex-h">
        <div className="row-head">
          <h2 id="ex-h">Gotowe przykłady</h2>
          <span className="row-hint">9 pytań ze złotego zestawu, odpowiedzi zapisane podczas ewaluacji</span>
        </div>
        <ExamplePicker
          examples={data.examples}
          value={mode === "example" ? ex.id : null}
          onChange={(id) => {
            setMode("example");
            upd({ ex: id });
          }}
        />
      </section>

      <section className="ask-result">
        <div className="question-line">
          <span className="q-label">{showLive ? "Twoje pytanie" : "Pytanie"}</span>
          <p className="q-text">{showLive ? question : ex.question}</p>
          {!showLive && (
            <div className="q-links">
              <a href={href("porownaj", { ex: ex.id })}>Porównaj 4 warianty <Icon name="arrow" size={15} /></a>
              <a href={href("slad", { ex: ex.id, v: variant })}>Ślad tej odpowiedzi <Icon name="arrow" size={15} /></a>
            </div>
          )}
        </div>
        <div className="answer-grid">
          <AnswerCard
            answer={answer}
            variant={shownVariant}
            category={showLive ? "live" : ex.category}
            activeBlock={open}
            onCite={(i) => setOpen(i)}
            showVerify={showLive ? liveMeta.verify : verify}
            live={!!showLive}
          />
          <aside className="sources-panel" aria-labelledby="src-h">
            <div className="panel-head">
              <h2 id="src-h">Przepisy w kontekście</h2>
              <span className="row-hint">{answer.context.length} z wyszukiwania{added.size ? ` i agenta` : ""}</span>
            </div>
            <Sources blocks={answer.context} citations={answer.citations} open={open} onToggle={setOpen} added={added} />
          </aside>
        </div>
      </section>
    </div>
  );
}
