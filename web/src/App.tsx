import { useEffect, useState } from "react";
import type { ExamplesFile } from "./lib/types";
import { checkHealth, type ApiState } from "./lib/api";
import { useRoute, SCREENS, href } from "./lib/route";
import { Icon } from "./components/Icon";
import { AskScreen } from "./screens/Ask";
import { CompareScreen } from "./screens/Compare";
import { TraceScreen } from "./screens/TraceScreen";
import { ResultsScreen } from "./screens/Results";
import { AboutScreen } from "./screens/About";
import { formatDate } from "./lib/law";

type Theme = "system" | "light" | "dark";

function useTheme(): [Theme, (t: Theme) => void] {
  const [t, setT] = useState<Theme>(() => {
    try {
      const v = localStorage.getItem("raglab.theme");
      return v === "light" || v === "dark" ? v : "system";
    } catch {
      return "system";
    }
  });
  const set = (v: Theme) => {
    setT(v);
    try {
      if (v === "system") localStorage.removeItem("raglab.theme");
      else localStorage.setItem("raglab.theme", v);
    } catch {
      /* prywatny tryb przeglądarki */
    }
    if (v === "system") delete document.documentElement.dataset.theme;
    else document.documentElement.dataset.theme = v;
  };
  return [t, set];
}

function ApiPill({ state }: { state: ApiState }) {
  const map: Record<ApiState["kind"], { text: string; tone: string; title: string }> = {
    none: { text: "gotowe przykłady", tone: "idle", title: "Ta wersja działa bez serwera: pokazuje zapisane odpowiedzi z ewaluacji." },
    checking: { text: "łączenie…", tone: "idle", title: "Sprawdzam, czy serwer demo odpowiada." },
    down: { text: "serwer niedostępny", tone: "warn", title: "Serwer demo nie odpowiada. Działają gotowe przykłady." },
    "examples-only": { text: "na żywo wyłączone", tone: "warn", title: "Serwer działa, ale pytania na żywo są chwilowo wyłączone." },
    live: { text: "na żywo", tone: "live", title: "Pytania trafiają do modelu na serwerze demo." },
  };
  const m = map[state.kind];
  return (
    <span className={`api-pill tone-${m.tone}`} title={m.title}>
      <span className="api-dot" aria-hidden="true" />
      {m.text}
    </span>
  );
}

export function App() {
  const route = useRoute();
  const [theme, setTheme] = useTheme();
  const [data, setData] = useState<ExamplesFile | null>(null);
  const [loadErr, setLoadErr] = useState<string | null>(null);
  const [api, setApi] = useState<ApiState>({ kind: "checking" });

  useEffect(() => {
    fetch("./examples.json")
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(String(r.status)))))
      .then((d: ExamplesFile) => setData(d))
      .catch(() => setLoadErr("Nie udało się wczytać gotowych przykładów (examples.json)."));
    checkHealth().then(setApi);
  }, []);

  useEffect(() => {
    const label = SCREENS.find((s) => s.id === route.screen)?.label;
    document.title = `${label} · RAG Lab`;
    window.scrollTo({ top: 0 });
  }, [route.screen]);

  const nextTheme: Record<Theme, Theme> = { system: "light", light: "dark", dark: "system" };
  const themeLabel: Record<Theme, string> = { system: "Motyw: systemowy", light: "Motyw: jasny", dark: "Motyw: ciemny" };

  return (
    <div className="app">
      <a className="skip" href="#main">Przejdź do treści</a>
      <header className="topbar">
        <div className="topbar-in">
          <a className="brand" href={href("zapytaj")} aria-label="RAG Lab, strona główna">
            <svg className="brand-mark" viewBox="0 0 32 32" aria-hidden="true">
              <rect width="32" height="32" rx="9" />
              <path d="M10 9h7.5a4.5 4.5 0 0 1 0 9H10zm0 9 9 6" />
            </svg>
            <span className="brand-name">RAG Lab</span>
            <span className="brand-sub">VAT · PIT · Ordynacja</span>
          </a>
          <nav className="tabs" aria-label="Ekrany">
            {SCREENS.map((s) => (
              <a key={s.id} href={href(s.id)} aria-current={route.screen === s.id ? "page" : undefined}>
                {s.label}
              </a>
            ))}
          </nav>
          <div className="topbar-tools">
            <ApiPill state={api} />
            <button type="button" className="icon-btn" onClick={() => setTheme(nextTheme[theme])} title={themeLabel[theme]} aria-label={themeLabel[theme]}>
              <Icon name={theme === "system" ? "system" : theme === "light" ? "sun" : "moon"} size={18} />
            </button>
          </div>
        </div>
        <div className="disclaimer" role="note">
          <div className="disclaimer-in">
            <Icon name="scale" size={16} />
            <span>
              <strong>Demo techniczne, nie porada podatkowa.</strong> Odpowiedzi opierają się wyłącznie na trzech ustawach z korpusu; stan prawny jest podany przy każdym przepisie.
            </span>
          </div>
        </div>
      </header>

      <main id="main" className="main">
        {loadErr && <div className="page"><p className="notice notice-danger">{loadErr}</p></div>}
        {!data && !loadErr && <div className="page"><div className="loading" role="status"><span className="spinner" />Wczytuję przykłady…</div></div>}
        {data && route.screen === "zapytaj" && <AskScreen data={data} api={api} params={route.params} />}
        {data && route.screen === "porownaj" && <CompareScreen data={data} api={api} params={route.params} />}
        {data && route.screen === "slad" && <TraceScreen data={data} params={route.params} />}
        {route.screen === "wyniki" && <ResultsScreen />}
        {route.screen === "o-projekcie" && <AboutScreen meta={data?.meta} />}
      </main>

      <footer className="footer">
        <div className="footer-in">
          <span>
            Odpowiada <code>{data?.meta.answer_model ?? "claude-sonnet-5"}</code>, ocenia <code>{data?.meta.judge_model.replace(/:free$/, "").replace(/^[^/]+\//, "") ?? "nemotron-3-ultra"}</code>
            {data && <> · przykłady z {formatDate(data.meta.generated)}</>}
          </span>
          <a href="https://github.com/Magiszonekk/rag-lab" target="_blank" rel="noreferrer">
            <Icon name="github" size={16} /> kod i wyniki na GitHubie
          </a>
        </div>
      </footer>
    </div>
  );
}
