import type { ExamplesFile } from "../lib/types";
import { ACTS, formatDate } from "../lib/law";
import { LAW_WATCH } from "../lib/results";
import { href } from "../lib/route";
import { Icon } from "../components/Icon";

const PIPE = [
  { icon: "book", t: "Ustawy", d: "Teksty jednolite z API ELI Sejmu, przypięte sumą SHA-256. PDF dzielony na artykuł → ustęp/§ → punkt → literę; przypisy rozpoznawane po kroju i położeniu, nie regexem." },
  { icon: "hourglass", t: "Stan prawny", d: "Przepisy przejściowe oznaczone jako obowiązujące, historyczne albo warunkowe. Art. 41 VAT nadal mówi 22%; obowiązujące 23% jest w art. 146ef i dołączane jest z adnotacją." },
  { icon: "search", t: "Wyszukiwanie", d: "BM25 na lematach (Morfeusz 2) i wektory mmlw-roberta-base, łączone przez RRF. HyDE dodaje wyszukiwanie hipotetycznym przepisem napisanym przez model." },
  { icon: "get", t: "Agent", d: "Pętla LangGraph: model widzi zebrane przepisy i może pobrać brakujący ustęp albo szukać inaczej, najwyżej 3 razy. W trybie ścisłym tylko adresy wynikające z tekstu." },
  { icon: "generate", t: "Odpowiedź", d: "Ten sam model i prompt dla każdego wariantu. Odpowiada tylko z kontekstu, każde twierdzenie z adresem przepisu; gdy przepisu brak, odmawia." },
  { icon: "verify", t: "Sprawdzanie", d: "Osobny model dzieli odpowiedź na twierdzenia i sprawdza każde z tekstem przepisów. Zdania bez oparcia są usuwane; bez oparcia dla głównej tezy odpowiedź staje się odmową." },
];

export function AboutScreen({ meta }: { meta?: ExamplesFile["meta"] }) {
  return (
    <div className="page about">
      <section className="screen-head">
        <h1>Jak to działa</h1>
        <p className="lead">
          To nie jest kolejny „czat z PDF-em”. Cztery warianty RAG działają na tym samym korpusie, z tym samym modelem i na tych samych zestawach testowych, a różnią się tylko sposobem szukania przepisów. Każde twierdzenie o tym, który jest lepszy, ma liczbę i przedział ufności.
        </p>
      </section>

      <ol className="pipeline">
        {PIPE.map((p) => (
          <li key={p.t}>
            <span className="pipe-icon"><Icon name={p.icon} size={20} /></span>
            <h2>{p.t}</h2>
            <p>{p.d}</p>
          </li>
        ))}
      </ol>

      <section className="about-grid">
        <div className="about-block">
          <h2>Korpus</h2>
          <div className="table-wrap flush"><table className="data corpus">
            <thead>
              <tr><th scope="col">ustawa</th><th scope="col">tekst jednolity</th><th scope="col">stan prawny</th><th scope="col">późniejsze zmiany</th></tr>
            </thead>
            <tbody>
              {ACTS.map((a) => {
                const w = LAW_WATCH.acts[a.key];
                const later = w?.changes_after_corpus ?? [];
                const inForce = later.filter((c) => c.already_in_force).length;
                return (
                  <tr key={a.key}>
                    <th scope="row">{a.title}</th>
                    <td>{a.dzu}</td>
                    <td className="num">{formatDate(a.stateDate)}</td>
                    <td>
                      {inForce > 0 ? (
                        <span className="law-flag is-stale" title={later.filter((c) => c.already_in_force).map((c) => `${c.eli} od ${formatDate(c.in_force_from)}`).join(", ")}>
                          <Icon name="hourglass" size={14} />
                          {inForce} już w mocy
                        </span>
                      ) : (
                        <span className="law-flag">brak zmian w mocy</span>
                      )}
                      {later.length - inForce > 0 && <span className="law-later">+{later.length - inForce} zapowiedziane</span>}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table></div>
          <p className="block-foot">
            Strażnik zmian sprawdza co tydzień API ELI (ostatnio {formatDate(LAW_WATCH.checked)}). Zmiany ogłoszone po dacie tekstu jednolitego nie są w korpusie, dlatego przy każdym przepisie jest jego stan prawny.
          </p>
        </div>
        <div className="about-block">
          <h2>Uczciwie o ograniczeniach</h2>
          <ul className="findings">
            <li>To demo techniczne, nie porada podatkowa. Nie zna rozporządzeń, interpretacji ani orzecznictwa.</li>
            <li>System nie ocenia, czy przepis pasuje do Twojej sytuacji. Jedyny pozostały błąd merytoryczny w ewaluacji to właśnie źle dopasowane zwolnienie.</li>
            <li>Zestaw testowy to 72 pytania sprawdzone ręcznie z ustawą; 9 z nich miało błędy mimo automatycznych kontroli cytatów i zostało poprawionych.</li>
          </ul>
          <h2>Modele</h2>
          <dl className="models">
            <div><dt>odpowiada</dt><dd><code>{meta?.answer_model ?? "claude-sonnet-5"}</code></dd></div>
            <div><dt>ocenia (sędzia)</dt><dd><code>{(meta?.judge_model ?? "nvidia/nemotron-3-ultra").replace(/:free$/, "")}</code></dd></div>
            <div><dt>embeddingi</dt><dd><code>sdadas/mmlw-roberta-base</code> (CPU)</dd></div>
            <div><dt>lematyzacja</dt><dd><code>Morfeusz 2</code></dd></div>
          </dl>
        </div>
      </section>

      <p className="next-link">
        <a href={href("porownaj", { ex: "g-vat-07" })}>Zobacz przykład, w którym agent dociąga brakujący przepis <Icon name="arrow" size={15} /></a>
      </p>
    </div>
  );
}
