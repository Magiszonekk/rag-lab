"""CLI ingestu.

uv run python -m raglab.ingest fetch          # pobiera PDF-y i sprawdza sha256
uv run python -m raglab.ingest build          # buduje data/corpus/<key>.json + raport
uv run python -m raglab.ingest show vat 86    # wyświetla artykuł z numeracją
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter

from raglab.ingest import build_act
from raglab.ingest.sources import REPO_ROOT, fetch, get_source, load_sources
from raglab.models import Act, Unit

CORPUS_DIR = REPO_ROOT / "data" / "corpus"


def _label(u: Unit) -> str:
    n = u.number or ""
    return {
        "article": f"Art. {n}.",
        "paragraph": f"{n}." if n.startswith("§") else f"ust. {n}.",
        "point": f"{n})",
        "letter": f"{n})",
    }[u.kind]


def render(u: Unit, depth: int = 0) -> str:
    pad = "  " * depth
    body = "(uchylony)" if u.repealed else u.text
    lines = [f"{pad}{_label(u)} {body}".rstrip()]
    for c in u.children:
        lines.append(render(c, depth + 1))
    if u.tail:
        lines.append(f"{pad}  {u.tail}")
    return "\n".join(lines)


def report(act: Act) -> dict[str, object]:
    kinds = Counter(u.kind for a in act.articles for u in a.walk())
    return {
        "key": act.source.key,
        "eli": act.source.eli,
        "state_date": str(act.state_date),
        "articles": len(act.articles),
        "repealed_articles": sum(a.repealed for a in act.articles),
        "units": dict(kinds),
        "footnotes": len(act.footnotes),
        "footnotes_max": max(act.footnotes, default=0),
        "annexes": len(act.annexes),
        "annex_rows": sum(len(a.rows) for a in act.annexes),
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="raglab.ingest")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("fetch")
    b = sub.add_parser("build")
    b.add_argument("keys", nargs="*")
    s = sub.add_parser("show")
    s.add_argument("key")
    s.add_argument("article")
    args = p.parse_args(argv)

    if args.cmd == "fetch":
        for src in load_sources():
            print(f"{src.key}: {fetch(src)} OK (sha256)")
        return 0
    if args.cmd == "build":
        CORPUS_DIR.mkdir(parents=True, exist_ok=True)
        for src in load_sources():
            if args.keys and src.key not in args.keys:
                continue
            act = build_act(src)
            # zapis atomowy: API w klastrze może czytać korpus w trakcie przebudowy (Job ingestu przy upgrade)
            out = CORPUS_DIR / f"{src.key}.json"
            tmp = out.with_suffix(".json.part")
            tmp.write_text(act.model_dump_json(indent=1), encoding="utf-8")
            tmp.replace(out)
            rep = report(act)
            if rep["footnotes"] != rep["footnotes_max"]:
                print(
                    f"BŁĄD {src.key}: wykryto {rep['footnotes']} przypisów, najwyższy numer {rep['footnotes_max']}",
                    file=sys.stderr,
                )
                return 1
            print(json.dumps(rep, ensure_ascii=False))
        return 0
    act = build_act(get_source(args.key))
    print(render(act.article(args.article)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
