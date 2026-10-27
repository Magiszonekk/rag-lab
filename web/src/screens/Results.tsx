import { useState } from "react";
import { ANSWERS, CALIBRATION, GOLDEN_REWRITE, RETRIEVAL, RETRIEVAL_REWRITE, type Metric } from "../lib/results";
import { fmt3, fmtCI, fmtInt, fmtSec, pct } from "../lib/format";
import { Segmented } from "../components/Bits";
import { Icon } from "../components/Icon";

/** Przedział ufności jako odcinek na wspólnej skali — widać, które wyniki się nakładają. */
function CIBar({ mean, ci, lo = 0.5, hi = 1, best }: { mean: number; ci: [number, number]; lo?: number; hi?: number; best?: boolean }) {
  const x = (v: number) => `${((Math.min(hi, Math.max(lo, v)) - lo) / (hi - lo)) * 100}%`;
  return (
    <span className={`ci${best ? " is-best" : ""}`} aria-hidden="true">
      <span className="ci-track" />
      <span className="ci-range" style={{ left: x(ci[0]), width: `calc(${x(ci[1])} - ${x(ci[0])})` }} />
      <span className="ci-dot" style={{ left: x(mean) }} />
    </span>
  );
}

function Scale({ lo = 0.5, hi = 1 }: { lo?: number; hi?: number }) {
  const ticks = [lo, (lo + hi) / 2, hi];
  return (
    <span className="ci-scale" aria-hidden="true">
      {ticks.map((t) => (
        <span key={t} style={{ left: `${((t - lo) / (hi - lo)) * 100}%` }}>{t.toFixed(2).replace(".", ",")}</span>
      ))}
    </span>
  );
}

const RET_ROWS: { id: string; label: string; note?: string }[] = [
  { id: "bm25-none", label: "BM25, bez lematyzacji" },
  { id: "bm25-morfeusz2", label: "BM25 + lematy Morfeusz 2" },
  { id: "vec-mmlw-base", label: "wektory (mmlw-roberta-base)" },
  { id: "hybrid-rrf", label: "hybryda BM25 + wektory (RRF)" },
  { id: "fixed-bm25-morfeusz2", label: "okna 400 tokenów + BM25", note: "zamiast podziału na artykuły/ustępy" },
  { id: "fixed-vec-mmlw-base", label: "okna 400 tokenów + wektory", note: "zamiast podziału na artykuły/ustępy" },
];

function RetrievalTable() {
  const best = "hybrid-rrf";
  return (
    <div className="table-wrap">
      <table className="data">
        <caption>Zestaw wyszukiwania v1: {RETRIEVAL.n} pytań (207 wygenerowanych z różnych przepisów + 76 potocznych parafraz)</caption>
        <thead>
          <tr>
            <th scope="col">konfiguracja</th>
            <th scope="col" className="num">recall@5</th>
            <th scope="col" className="ci-col">przedział 95% <Scale /></th>
            <th scope="col" className="num">recall@1</th>
            <th scope="col" className="num">MRR@20</th>
            <th scope="col" className="num">potoczne recall@5</th>
            <th scope="col" className="num">tokeny w top-5</th>
          </tr>
        </thead>
        <tbody>
          {RET_ROWS.map((r) => {
            const c = RETRIEVAL.configs[r.id];
            const ci = c.all.ci95["recall@5"];
            return (
              <tr key={r.id} className={r.id === best ? "is-best" : undefined}>
                <th scope="row">
                  {r.label}
                  {r.note && <span className="row-note">{r.note}</span>}
                </th>
                <td className="num strong">{fmt3(c.all["recall@5"])}</td>
                <td className="ci-col">
                  <CIBar mean={c.all["recall@5"]} ci={ci} best={r.id === best} />
                  <span className="ci-text">{fmtCI(ci)}</span>
                </td>
                <td className="num">{fmt3(c.all["recall@1"])}</td>
                <td className="num">{fmt3(c.all["mrr@20"])}</td>
                <td className="num">{fmt3(c.paraphrased["recall@5"])}</td>
                <td className="num">{fmtInt(c.all["tokens@5"])}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

const RW_ROWS = [
  { id: "hybrid-rrf-demote", label: "hybryda" },
  { id: "hybrid-rewrite", label: "+ przepisanie pytania na język ustawy" },
  { id: "hybrid-hyde", label: "+ HyDE (hipotetyczny przepis)" },
  { id: "hybrid-rewrite-hyde", label: "+ oba" },
];

function RewriteTable() {
  return (
    <div className="table-wrap">
      <table className="data">
        <caption>Przepisywanie pytań: Claude Sonnet 5 przepisuje pytanie przed wyszukiwaniem; wyniki oryginału i wersji przepisanej łączy RRF</caption>
        <thead>
          <tr>
            <th scope="col">wyszukiwanie</th>
            <th scope="col" className="num">zestaw wyszukiwania ({RETRIEVAL_REWRITE.n})</th>
            <th scope="col" className="num">potoczne (76)</th>
            <th scope="col" className="num">złoty zestaw ({GOLDEN_REWRITE.n})</th>
            <th scope="col" className="ci-col">złoty, przedział 95% <Scale /></th>
            <th scope="col" className="num">potoczne (11)</th>
          </tr>
        </thead>
        <tbody>
          {RW_ROWS.map((r) => {
            const a = RETRIEVAL_REWRITE.configs[r.id];
            const g = GOLDEN_REWRITE.configs[r.id];
            const ci = g.all.ci95["recall@5"];
            return (
              <tr key={r.id}>
                <th scope="row">{r.label}</th>
                <td className="num">{fmt3(a.all["recall@5"])}</td>
                <td className="num">{fmt3(a.paraphrased["recall@5"])}</td>
                <td className="num strong">{fmt3(g.all["recall@5"])}</td>
                <td className="ci-col">
                  <CIBar mean={g.all["recall@5"]} ci={ci} />
                  <span className="ci-text">{fmtCI(ci)}</span>
                </td>
                <td className="num">{fmt3(g.paraphrased["recall@5"])}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

const ANS_ROWS = [
  { id: "simple", label: "Prosty (wektory)" },
  { id: "hybrid", label: "Hybrydowy (BM25 + wektory)" },
  { id: "hyde", label: "Hybrydowy + HyDE" },
  { id: "agentic", label: "Agentowy, swobodny", note: "może pobrać dowolny adres, także z pamięci modelu" },
  { id: "agentic-strict", label: "Agentowy, ścisły", note: "wariant w demo" },
];

function AnswersTable() {
  const [verify, setVerify] = useState<"off" | "llm">("off");
  return (
    <>
      <div className="table-tools">
        <span className="control-label">Sprawdzanie odpowiedzi</span>
        <Segmented size="sm" label="Sprawdzanie odpowiedzi" value={verify} onChange={setVerify} options={[{ value: "off", label: "wyłączone" }, { value: "llm", label: "zdanie po zdaniu" }]} />
      </div>
      <div className="table-wrap">
        <table className="data">
          <caption>
            Złoty zestaw v1.1: 53 pytania z odpowiedzią + 19 spoza korpusu. Odpowiada {ANSWERS.answer_models[0]}, wyszukiwanie: Qwen3-Embedding-8B, ocenia Nemotron 3 Ultra (inna rodzina modeli). Ten sam prompt i model dla każdego wariantu.
          </caption>
          <thead>
            <tr>
              <th scope="col">wariant</th>
              <th scope="col" className="num">poprawne</th>
              <th scope="col" className="ci-col">przedział 95% <Scale /></th>
              <th scope="col" className="num">poprawne + częściowe</th>
              <th scope="col" className="num">kluczowe fakty</th>
              <th scope="col" className="num">cytuje właściwy przepis</th>
              <th scope="col" className="num">wierność kontekstowi</th>
              <th scope="col" className="num">słuszne odmowy</th>
              <th scope="col" className="num">fałszywe odmowy</th>
              <th scope="col" className="num">tokeny / pytanie</th>
              <th scope="col" className="num">czas p50</th>
            </tr>
          </thead>
          <tbody>
            {ANS_ROWS.filter((r) => ANSWERS.configs[`${r.id}/verify=${verify}`]).map((r) => {
              const c = ANSWERS.configs[`${r.id}/verify=${verify}`];
              const m = (k: string) => c[k] as Metric;
              const cr = m("correct_refusals");
              return (
                <tr key={r.id} className={r.id === "agentic-strict" ? "is-best" : undefined}>
                  <th scope="row">
                    {r.label}
                    {r.note && <span className="row-note">{r.note}</span>}
                  </th>
                  <td className="num strong">{fmt3(m("answerable_correct").mean)}</td>
                  <td className="ci-col">
                    <CIBar mean={m("answerable_correct").mean} ci={m("answerable_correct").ci95} best={r.id === "agentic-strict"} />
                    <span className="ci-text">{fmtCI(m("answerable_correct").ci95)}</span>
                  </td>
                  <td className="num">{fmt3(m("answerable_correct_or_partial").mean)}</td>
                  <td className="num">{fmt3(m("key_facts").mean)}</td>
                  <td className="num">{fmt3(m("citation_recall").mean)}</td>
                  <td className="num">{fmt3(m("faithful").mean)}</td>
                  <td className="num">{Math.round(cr.mean * cr.n)}/{cr.n}</td>
                  <td className="num">{fmt3(m("false_refusals").mean)}</td>
                  <td className="num">{fmtInt(c.tokens_per_question)}</td>
                  <td className="num">{fmtSec(c.latency_ms_p50)}</td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
      <p className="table-foot">
        Fałszywa odmowa: pytanie ma odpowiedź w korpusie, a system odpowiedział, że nie może. Liczone z treści odpowiedzi, nie tylko z flagi; sama flaga ukrywała większość przypadków (HyDE: 0/53 według flagi, 3/53 w rzeczywistości).
      </p>
    </>
  );
}

// seria Opus 5.5 + Qwen3-Embedding-8B (verify=off); porównanie modeli Sonnet 5.5 vs Opus 5.5 — README
const SIGNIF: { a: string; b: string; ab: string; p: string; sig: boolean }[] = [
  { a: "Agentowy ścisły", b: "Prosty", ab: "4 : 1", p: "0,38", sig: false },
  { a: "Agentowy ścisły", b: "Hybrydowy", ab: "7 : 1", p: "0,070", sig: false },
  { a: "Agentowy ścisły", b: "HyDE", ab: "6 : 1", p: "0,13", sig: false },
  { a: "Prosty", b: "Hybrydowy", ab: "6 : 3", p: "0,51", sig: false },
  { a: "HyDE", b: "Prosty", ab: "2 : 4", p: "0,69", sig: false },
  { a: "Sonnet 5.5 (agent)", b: "Opus 5.5 (agent)", ab: "1 : 2", p: "1,0", sig: false },
];

export function ResultsScreen() {
  return (
    <div className="page page-wide results">
      <section className="screen-head">
        <h1>Wyniki ewaluacji</h1>
        <p className="lead">
          Każde twierdzenie o tym, który wariant jest lepszy, ma liczbę i przedział ufności (bootstrap po pytaniach). Porównania parami: dokładny test McNemara. Liczby pochodzą z plików <code>results/*.json</code> w repozytorium, tych samych co w README.
        </p>
      </section>

      <section className="result-block" aria-labelledby="r1">
        <h2 id="r1">Wyszukiwanie: czy właściwy przepis jest w top-5</h2>
        <p className="block-lead">Trafienie: znaleziony fragment zawiera co najmniej połowę wzorcowego przepisu albo co najmniej połowa fragmentu jest tym przepisem.</p>
        <RetrievalTable />
        <ul className="findings">
          <li><strong>Lematyzacja to największy pojedynczy zysk dla BM25:</strong> +11,7 pp recall@5 (p &lt; 0,0001), +25 pp na pytaniach potocznych. „Podatnik” występuje w samej ustawie o VAT w 9 formach.</li>
          <li><strong>Hybryda wygrywa z BM25</strong> (p = 0,0003), ale z samymi wektorami różnica nie jest istotna (p = 0,064) przy 283 pytaniach. Przedziały na wykresie wyraźnie się nakładają.</li>
          <li><strong>Podział według struktury ustawy ma znaczenie dla wektorów:</strong> ten sam model na stałych oknach traci 16 pp (p &lt; 0,0001). Dla BM25 to remis przy 2,6 raza mniejszym kontekście.</li>
        </ul>
      </section>

      <section className="result-block" aria-labelledby="r2">
        <h2 id="r2">Pytania potoczne: przepisywanie i HyDE</h2>
        <RewriteTable />
        <ul className="findings">
          <li>Na złotym zestawie zysk jest istotny (oba vs hybryda: 10 : 1 pytań rozbieżnych, p = 0,012).</li>
          <li>Na większym zestawie wyszukiwania <strong>nie jest</strong> (HyDE vs hybryda 16 : 7, p = 0,09), choć pytania potoczne poprawiają się konsekwentnie.</li>
          <li>Efekt zależy od modelu przepisującego: z wcześniejszym (GPT-5.6) HyDE był istotny także na dużym zestawie (p = 0,008). Zysk to cecha pary model + wyszukiwarka, nie samej techniki.</li>
        </ul>
      </section>

      <section className="result-block" aria-labelledby="r3">
        <h2 id="r3">Odpowiedzi: poprawność według sędziego</h2>
        <AnswersTable />
        <div className="table-wrap narrow">
          <table className="data">
            <caption>Porównania parami na „poprawne” (pytania, w których wygrał tylko A : tylko B)</caption>
            <thead>
              <tr><th scope="col">A</th><th scope="col">B</th><th scope="col" className="num">A : B</th><th scope="col" className="num">p</th><th scope="col">wniosek</th></tr>
            </thead>
            <tbody>
              {SIGNIF.map((s) => (
                <tr key={s.a + s.b}>
                  <td>{s.a}</td><td>{s.b}</td><td className="num">{s.ab}</td><td className="num">{s.p}</td>
                  <td><span className={`sig ${s.sig ? "is-sig" : "is-not"}`}>{s.sig ? "istotna różnica" : "nieistotna"}</span></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
        <ul className="findings">
          <li><strong>Sonnet 5.5 i Opus 5.5 wypadają tak samo.</strong> Na tym samym embeddingu różnią się w 2–6 pytaniach z 53, w obie strony (McNemar p ≥ 0,69 w każdym wariancie). Gdy model ma tylko przeczytać podane przepisy, większy model nie daje tu mierzalnej przewagi.</li>
          <li><strong>Lepszy embedding robi większość pracy.</strong> Z Qwen3-Embedding-8B sam wariant wektorowy jest w granicach szumu od HyDE i agenta, a dołożenie BM25 nieco szkodzi. Z lokalnym mmlw-roberta-base hybryda i HyDE dawały wyraźny zysk.</li>
          <li><strong>Pozostałe błędy to braki wyszukiwania, nie halucynacje.</strong> Odmowy przy pytaniach, na które jest odpowiedź, dotyczą przepisów, które nie trafiły do top-5. Agent naprawia te przypadki, dociągając brakujący ustęp albo przepis, do którego tekst odsyła.</li>
          <li><strong>Agent czy pamięć modelu?</strong> W wariancie swobodnym 6 z 25 pobranych adresów pochodziło z wiedzy modelu o ustawie. Wariant ścisły może pobrać tylko inną jednostkę artykułu z kontekstu albo przepis, do którego tekst odsyła. Wynik jest ten sam (1 : 1, p = 1,0), więc zysk to nawigacja po strukturze ustawy.</li>
          <li><strong>Sprawdzanie zdanie po zdaniu nie zablokowało żadnej poprawnej odpowiedzi</strong>, przycięło 6–7 odpowiedzi na wariant i zmieniło wynik o 0 do +2 pp. Wersja deterministyczna (liczby z odpowiedzi muszą być w cytowanym tekście) szkodzi: zablokowała 6 odpowiedzi HyDE, z czego 5 poprawnych.</li>
        </ul>
      </section>

      <section className="result-block" aria-labelledby="r4">
        <h2 id="r4">Kalibracja sędziego</h2>
        <div className="calib">
          <dl className="calib-figures">
            <div><dt>par ocenionych przez obu sędziów</dt><dd>{CALIBRATION.n_pairs_both_judged}<span> z {CALIBRATION.n}</span></dd></div>
            <div><dt>zgodność</dt><dd>{pct(CALIBRATION.judge_agreement)}<span> {CALIBRATION.agree}/{CALIBRATION.n_pairs_both_judged}</span></dd></div>
            <div><dt>kappa Cohena</dt><dd>{CALIBRATION.judge_kappa.toFixed(2).replace(".", ",")}<span> znaczna</span></dd></div>
            <div><dt>sporów przejrzanych ręcznie</dt><dd>{CALIBRATION.reviewed}<span> graniczne, w obie strony</span></dd></div>
          </dl>
          <div className="calib-text">
            <p>Drugi sędzia (Claude Opus 5.5) ocenił te same odpowiedzi HyDE i agenta obu serii (Sonnet 5.5 i Opus 5.5) co główny sędzia Nemotron 3 Ultra.</p>
            <ul className="findings">
              <li><strong>Preferencję własnego modelu zmierzyliśmy, a nie założyliśmy:</strong> Opus jako sędzia ocenił odpowiedzi Opusa dokładnie tak jak Nemotron (0,925 i 0,925), a odpowiedzi Sonneta o 0,9 pp wyżej. Nie widać faworyzowania własnego modelu.</li>
              <li><strong>Błąd głównego sędziego:</strong> szczere „tego przepisu nie mam w kontekście” ocenia jako słuszną odmowę, nawet gdy odpowiedź jest w korpusie. Dlatego fałszywe odmowy liczymy z treści odpowiedzi, a w przykładach takie odmowy mają osobną etykietę „odmowa (pominięty przepis)”.</li>
              <li><strong>Przegląd sporów znalazł błąd we wzorcu, nie w modelach:</strong> wzorzec dla pytania o KSeF pomijał przepis epizodyczny (art. 145m VAT, faktury papierowe do 10 000 zł miesięcznie do końca 2026 r.). Oba modele podały go poprawnie, a sędzia trzymał się wzorca. Wzorzec poprawiony (zestaw v1.1).</li>
            </ul>
          </div>
        </div>
      </section>

      <section className="result-block caveats" aria-labelledby="r5">
        <h2 id="r5"><Icon name="alert" size={20} /> Czego te liczby nie mówią</h2>
        <ul>
          <li><strong>53 pytania to mało.</strong> Najlepsze warianty mają 0,96–0,98 poprawnych, więc złoty zestaw jest bliski nasycenia; do rozdzielenia najlepszych wariantów potrzebny jest trudniejszy zestaw (etap M2b).</li>
          <li><strong>Recenzentem sporów był model</strong> (Claude, ta sama rodzina co model odpowiadający), sprawdzający z tekstem ustawy, a nie doradca podatkowy.</li>
          <li><strong>Liczb z różnych serii nie mieszamy.</strong> Tabela to seria Opus 5.5 + Qwen3-Embedding-8B; Sonnet 5.5 daje te same wnioski (agent 0,962, HyDE 0,925, prosty 0,887). Starsze serie (Sonnet 5 / GPT-5.6, embedding mmlw) są w repozytorium.</li>
          <li><strong>Pytania na żywo w demo</strong> obsługuje Claude Sonnet 5.5 (przy jego niedostępności darmowy model zapasowy), a nie Opus — tabela wyżej pokazuje, że różnica jest w granicach szumu.</li>
          <li><strong>Korpus to trzy ustawy</strong> w tekstach jednolitych z określonym stanem prawnym. Zmiany ogłoszone później nie są w nim uwzględnione (zakładka „Jak to działa”).</li>
        </ul>
      </section>
    </div>
  );
}
