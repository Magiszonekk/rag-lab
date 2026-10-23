"""Przeglądanie korpusu z linii poleceń (dla ludzi i agentów piszących zestawy testowe).

uv run python -m raglab.lookup show "VAT art. 86 ust. 2"      # treść jednostki z kontekstem
uv run python -m raglab.lookup article vat 146ef               # cały artykuł
uv run python -m raglab.lookup grep vat "stawka podatku wynosi" # wyszukiwanie tekstu (regex, bez wielkości liter)
uv run python -m raglab.lookup toc pit                         # spis działów/rozdziałów z zakresem artykułów
uv run python -m raglab.lookup status vat 146ef                # etykieta czasowa (in_force / historical / …)
"""

from __future__ import annotations

import argparse
import re
import sys

from raglab.annotate_temporal import load_labels
from raglab.corpus import iter_units, load_corpus, render_unit


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="raglab.lookup")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("show")
    s.add_argument("address")
    a = sub.add_parser("article")
    a.add_argument("act")
    a.add_argument("number")
    g = sub.add_parser("grep")
    g.add_argument("act")
    g.add_argument("pattern")
    g.add_argument("--max", type=int, default=30)
    t = sub.add_parser("toc")
    t.add_argument("act")
    st = sub.add_parser("status")
    st.add_argument("act")
    st.add_argument("number")
    args = ap.parse_args(argv)

    corpus = load_corpus()
    labels = load_labels()

    if args.cmd == "show":
        index = {loc.address: loc for act in corpus.values() for loc in iter_units(act)}
        loc = index.get(args.address)
        if loc is None:
            near = [k for k in index if k.startswith(args.address.rsplit(" ", 2)[0])][:10]
            print(f"brak adresu {args.address!r}; podobne: {near}", file=sys.stderr)
            return 1
        lab = labels.get((loc.act, loc.article.number or ""), "in_force")
        act = corpus[loc.act]
        print(f"[{loc.address}] stan prawny {act.state_date}, status: {lab}, ścieżka: {' / '.join(loc.article.path)}")
        if loc.unit.version:
            print(f"UWAGA: jednostka dwuwersyjna: {loc.unit.version} {loc.unit.effective_from or ''}")
        print(loc.full_text())
        return 0
    if args.cmd == "article":
        act = corpus[args.act]
        art = act.article(args.number)
        lab = labels.get((args.act, args.number), "in_force")
        print(f"[art. {art.number}] status: {lab}, ścieżka: {' / '.join(art.path)}")
        print(render_unit(art))
        return 0
    if args.cmd == "grep":
        act = corpus[args.act]
        rx = re.compile(args.pattern, re.I)
        n = 0
        for loc in iter_units(act):
            if loc.unit.children:
                continue  # tylko liście, żeby nie powtarzać
            text = " ".join([u.text for u in loc.chain if u.text] + ([loc.unit.tail] if loc.unit.tail else []))
            if m := rx.search(text):
                start = max(0, m.start() - 120)
                print(f"{loc.address}: …{text[start : m.end() + 160]}…")
                n += 1
                if n >= args.max:
                    break
        return 0
    if args.cmd == "toc":
        act = corpus[args.act]
        last: tuple[str, ...] = ()
        first_num = prev = ""
        for art in act.articles:
            path = tuple(art.path)
            if path != last:
                if last:
                    print(f"  art. {first_num}–{prev}")
                print(" / ".join(path))
                first_num = art.number or ""
                last = path
            prev = art.number or ""
        print(f"  art. {first_num}–{prev}")
        return 0
    if args.cmd == "status":
        print(labels.get((args.act, args.number), "in_force (brak etykiety: artykuł spoza rozdziałów przejściowych)"))
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
