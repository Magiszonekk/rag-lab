"""Ponowna walidacja zestawu wyszukiwania z kontekstem odesłań (przegląd v1, przypadek VAT art. 145i).

Walidator dostaje pytanie, przepis źródłowy i treść przepisów, do których źródło odsyła, i ocenia, czy
pytanie poprawnie opisuje kontekst (np. „zawiadomienie przy odwrotnym obciążeniu gazu”, a nie „przed KSeF”).
Pytania z `context_ok = false` są generowane od nowa (z odesłaniami w prompcie) — patrz `--fix`.
"""

from __future__ import annotations

import argparse
import json
import sys
from concurrent.futures import ThreadPoolExecutor

from raglab.corpus import iter_units, load_corpus
from raglab.evalsets.retrieval import EVAL_DIR, VALIDATOR_MODELS, refs_block
from raglab.llm import LLM, LLMError, parse_json
from raglab.refs import Resolver

PROMPT = """Sprawdź, czy pytanie testowe poprawnie opisuje sytuację, której dotyczy przepis.
Przepis odsyła do innych przepisów — ich treść podano niżej. Typowy błąd: pytanie nadaje przepisowi
inny kontekst niż ten wynikający z odesłań (np. przepis dotyczy zawiadomienia przy odwrotnym obciążeniu
gazu, a pytanie mówi o zawiadomieniu przed wdrożeniem e-faktur).

Odpowiedz wyłącznie JSON: {{"context_ok": true/false, "note": "krótko, co jest źle (jeśli false)"}}

PYTANIE: {question}

PRZEPIS ({address}):
{text}
{refs}"""


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="raglab.evalsets.recheck")
    ap.add_argument("--version", default="v1")
    ap.add_argument("--workers", type=int, default=6)
    args = ap.parse_args(argv)
    corpus = load_corpus()
    resolvers = {k: Resolver(a) for k, a in corpus.items()}
    index = {loc.address: loc for k, a in corpus.items() for loc in iter_units(a)}
    path = EVAL_DIR / f"retrieval_{args.version}.jsonl"
    items = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    llm = LLM(VALIDATOR_MODELS)

    def check(item: dict[str, object]) -> dict[str, object]:
        loc = index[str(item["source_address"])]
        ctx = resolvers[loc.act].context_for(loc)
        rec: dict[str, object] = {"id": item["id"], "address": loc.address, "origin": item["origin"], "refs": len(ctx)}
        if not ctx:
            rec["context_ok"] = True
            rec["note"] = "brak odesłań"
            return rec
        prompt = PROMPT.format(
            question=item["question"], address=loc.address, text=loc.full_text(), refs=refs_block(ctx)
        )
        try:
            d = parse_json(llm.complete([{"role": "user", "content": prompt}], max_tokens=1500, temperature=0.0).text)
            assert isinstance(d, dict)
            rec["context_ok"] = bool(d.get("context_ok"))
            rec["note"] = d.get("note", "")
        except (LLMError, ValueError, AssertionError) as e:
            rec["context_ok"] = None
            rec["note"] = f"błąd: {e}"[:200]
        return rec

    with ThreadPoolExecutor(args.workers) as ex:
        results = list(ex.map(check, items))
    out = EVAL_DIR / f"retrieval_{args.version}.recheck.jsonl"
    out.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in results), encoding="utf-8")
    bad = [r for r in results if r["context_ok"] is False]
    err = [r for r in results if r["context_ok"] is None]
    print(
        f"sprawdzone {len(results)}, z odesłaniami {sum(1 for r in results if r['refs'])}, "
        f"złe {len(bad)}, błędy {len(err)}",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
