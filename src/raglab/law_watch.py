"""Strażnik zmian w prawie (koncept D1): czy po dacie stanu korpusu pojawiło się coś nowego.

Dla każdego aktu z `data/sources.toml` pyta API Sejmu (ELI) o akt bazowy (ten, którego tekst jednolity mamy) i
sprawdza:
- **nowszy tekst jednolity** niż ten w korpusie (lista „Inf. o tekście jednolitym”);
- **akty zmieniające** ogłoszone po obwieszczeniu tekstu jednolitego z korpusu — z datą wejścia w życie;
  osobno te, które JUŻ weszły w życie (korpus jest w tym miejscu nieaktualny), i zapowiedziane.

Niczego nie podmienia (odświeżenie korpusu = świadoma decyzja + nowa wersja zestawów testowych). Zapisuje
`results/law_watch.json`, który czyta UI („istnieją zmiany późniejsze niż stan korpusu”).

    uv run python -m raglab.law_watch            # raport
    uv run python -m raglab.law_watch --check    # kod 1, gdy coś już weszło w życie albo jest nowszy tekst
"""

from __future__ import annotations

import argparse
import json
import sys
import tomllib
from datetime import date
from typing import Any

import httpx

from raglab.ingest.sources import REPO_ROOT

API = "https://api.sejm.gov.pl/eli/acts"
OUT = REPO_ROOT / "results" / "law_watch.json"


def _get(client: httpx.Client, eli: str) -> dict[str, Any]:
    r = client.get(f"{API}/{eli}", timeout=30)
    r.raise_for_status()
    d: dict[str, Any] = r.json()
    return d


def watch(today: date | None = None) -> dict[str, Any]:
    today = today or date.today()
    sources = tomllib.loads((REPO_ROOT / "data" / "sources.toml").read_text(encoding="utf-8"))["source"]
    out: dict[str, Any] = {"checked": str(today), "acts": {}}
    with httpx.Client(headers={"User-Agent": "raglab-law-watch"}) as client:
        for s in sources:
            tj = _get(client, s["eli"])  # obwieszczenie tekstu jednolitego z korpusu
            base_eli = tj["references"]["Tekst jednolity dla aktu"][0]["id"]
            base = _get(client, base_eli)
            refs = base.get("references", {})
            tj_list = [x["id"] for x in refs.get("Inf. o tekście jednolitym", [])]
            announced = tj.get("announcementDate") or ""
            # akty zmieniające ogłoszone po obwieszczeniu (rok/pozycja z ELI; data ogłoszenia z API aktu)
            changes = []
            for x in refs.get("Akty zmieniające", []):
                eff = x.get("date") or ""
                if eff and eff <= announced:
                    continue  # weszło w życie przed obwieszczeniem → jest w tekście jednolitym
                a = _get(client, x["id"])
                ann = a.get("announcementDate") or ""
                if ann and ann <= announced:
                    continue  # ogłoszone przed obwieszczeniem → ujęte (jako brzmienie przyszłe albo obowiązujące)
                changes.append({"eli": x["id"], "title": a.get("title", "")[:200], "announced": ann,
                                "in_force_from": eff, "already_in_force": bool(eff) and eff <= str(today)})  # fmt: skip
            changes.sort(key=lambda c: c["in_force_from"] or "9999")
            newer_tj = [e for e in tj_list if e != s["eli"] and e > s["eli"]]
            out["acts"][s["key"]] = {
                "name": s["name"],
                "corpus_text": s["eli"],
                "corpus_announced": announced,
                "base_act": base_eli,
                "newer_consolidated_text": newer_tj,
                "changes_after_corpus": changes,
                "stale": bool(newer_tj) or any(c["already_in_force"] for c in changes),
            }
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="raglab.law_watch")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args(argv)
    rep = watch()
    OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, a in rep["acts"].items():
        ch = a["changes_after_corpus"]
        live = [c for c in ch if c["already_in_force"]]
        print(f"{k}: tekst {a['corpus_text']} (obwieszczenie {a['corpus_announced']}); nowszy tekst jednolity: "
              f"{a['newer_consolidated_text'] or 'brak'}; zmiany po korpusie: {len(ch)} "
              f"(już obowiązują: {len(live)})", file=sys.stderr)  # fmt: skip
        for c in ch:
            print(f"   {c['in_force_from'] or '?':10} {c['eli']:14} {'OBOWIĄZUJE' if c['already_in_force'] else ''} "
                  f"{c['title'][:90]}", file=sys.stderr)  # fmt: skip
    return 1 if args.check and any(a["stale"] for a in rep["acts"].values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())
