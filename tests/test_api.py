"""Testy API demo: przykłady, limity, filtr tematów, brak pytań na żywo bez bramki demo."""

import importlib

import pytest
from fastapi.testclient import TestClient


@pytest.fixture()
def api(monkeypatch):  # type: ignore[no-untyped-def]
    monkeypatch.setenv("RAGLAB_LIVE_ENABLED", "0")
    import raglab.api as m

    return importlib.reload(m)


def test_health_and_examples(api) -> None:  # type: ignore[no-untyped-def]
    c = TestClient(api.app)
    assert c.get("/health").json()["ok"] is True
    ex = c.get("/examples").json()
    assert len(ex["examples"]) >= 5 and "agentic-strict" in ex["examples"][0]["variants"]


def test_live_disabled_returns_503(api) -> None:  # type: ignore[no-untyped-def]
    r = TestClient(api.app).post("/ask", json={"question": "Jaka jest stawka VAT na usługi?"})
    assert r.status_code == 503


def test_live_without_demo_gateway_is_503(monkeypatch, api) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setattr(api, "LIVE", True)
    for k in ("LLM_DEMO_BASE_URL", "LLM_DEMO_API_KEY", "LLM_DEMO_MODEL"):
        monkeypatch.delenv(k, raising=False)
    r = TestClient(api.app).post("/ask", json={"question": "Jaka jest stawka VAT na usługi?"})
    assert r.status_code == 503  # nigdy nie spada na klucz ewaluacji


def test_off_topic_refused_without_model(monkeypatch, api) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setattr(api, "LIVE", True)
    r = TestClient(api.app).post("/ask", json={"question": "Podaj przepis na pierogi z kapustą"})
    assert r.status_code == 200 and r.json()["refused"] is True


def test_rate_limit_per_ip(monkeypatch, api) -> None:  # type: ignore[no-untyped-def]
    monkeypatch.setattr(api, "PER_IP_HOUR", 2)
    api._ip_hits.clear()
    api._check_limits("1.2.3.4")
    api._check_limits("1.2.3.4")
    with pytest.raises(api.HTTPException) as e:
        api._check_limits("1.2.3.4")
    assert e.value.status_code == 429


def test_bad_variant_and_long_question(api) -> None:  # type: ignore[no-untyped-def]
    c = TestClient(api.app)
    assert c.post("/ask", json={"question": "Stawka VAT?", "variant": "x"}).status_code == 400
    assert c.post("/ask", json={"question": "VAT " * 300}).status_code == 422


def test_mask_personal_data() -> None:
    from raglab.traces import mask

    s = mask("PESEL 85010112345, NIP 123-456-78-90, mail jan@x.pl, tel. +48 600 700 800")
    assert "85010112345" not in s and "jan@x.pl" not in s and "600 700 800" not in s and "123-456-78-90" not in s


def test_law_watch_logic_with_fake_api(monkeypatch) -> None:  # type: ignore[no-untyped-def]
    from datetime import date

    import raglab.law_watch as lw

    acts = {
        "DU/2026/1263": {"announcementDate": "2026-09-01", "references": {"Tekst jednolity dla aktu": [{"id": "B"}]}},
        "B": {"references": {
            "Inf. o tekście jednolitym": [{"id": "DU/2026/1263"}],
            "Akty zmieniające": [{"id": "OLD", "date": "2026-08-01"}, {"id": "NEW", "date": "2026-10-01"},
                                 {"id": "FUT", "date": "2027-01-01"}]}},
        "NEW": {"announcementDate": "2026-09-20", "title": "nowela"},
        "FUT": {"announcementDate": "2026-09-04", "title": "przyszła"},
        "OLD": {"announcementDate": "2026-07-01", "title": "stara"},
    }  # fmt: skip
    monkeypatch.setattr(lw, "_get", lambda client, eli: acts[eli])
    monkeypatch.setattr(
        lw.tomllib, "loads", lambda s: {"source": [{"key": "vat", "eli": "DU/2026/1263", "name": "VAT"}]}
    )
    rep = lw.watch(today=date(2026, 10, 25))["acts"]["vat"]
    assert [c["eli"] for c in rep["changes_after_corpus"]] == ["NEW", "FUT"]
    assert rep["changes_after_corpus"][0]["already_in_force"] and not rep["changes_after_corpus"][1]["already_in_force"]
    assert rep["stale"] is True


def test_demo_path_uses_only_demo_model(monkeypatch, api, tmp_path) -> None:  # type: ignore[no-untyped-def]
    """Każde wywołanie modelu w ścieżce /ask idzie przez klienta bramki demo (HyDE, odpowiedź, weryfikacja)."""
    import raglab.llm as L

    calls: list[str] = []

    def fake_complete(self, messages, **kw):  # type: ignore[no-untyped-def]
        calls.append(self.models[0])
        txt = messages[-1]["content"]
        if "hipotetyczny" in txt or "fragment polskiej ustawy" in txt:
            body = '{"query": "Zwrot różnicy podatku następuje w terminie dni od złożenia rozliczenia"}'
        elif "Sprawdzasz odpowiedź" in txt:
            body = '{"claims": [], "verdict": "pass", "fixed_answer": null}'
        else:
            body = '{"answer": "Termin wynosi 40 dni.", "citations": ["VAT art. 87 ust. 2"], "refused": false}'
        return L.Completion(text=body, requested_model=self.models[0], served_model=self.models[0],
                            prompt_tokens=1, completion_tokens=1, latency_ms=1)  # fmt: skip

    monkeypatch.setattr(L.LLM, "complete", fake_complete)
    # cache przepisań i weryfikacji → pliki tymczasowe (nie zaśmiecać prawdziwych wyników ewaluacji)
    import raglab.rag.verify_llm as VL
    import raglab.search.rewrite as RW

    monkeypatch.setattr(RW, "CACHE", tmp_path / "rewrite.jsonl")
    monkeypatch.setattr(RW, "_mem", None)
    monkeypatch.setattr(VL, "CACHE", tmp_path / "verify.jsonl")
    monkeypatch.setattr(VL, "_mem", None)
    # bez embeddingów (w CI ich nie ma — liczenie korpusu na CPU trwa kilkanaście minut): obie „nogi” hybrydy = BM25
    import raglab.rag.variants as V
    from raglab.corpus import load_corpus
    from raglab.search.chunking import structural
    from raglab.search.index import BM25Index
    from raglab.search.normalize import get_normalizer

    bm = BM25Index([c for a in load_corpus().values() for c in structural(a)], get_normalizer("morfeusz2"))
    monkeypatch.setattr(V, "_indexes", lambda: (bm, bm))
    monkeypatch.setenv("LLM_BASE_URL", "http://example.invalid/v1")  # w CI nie ma .env
    monkeypatch.setenv("LLM_API_KEY", "x")
    demo = L.LLM(["demo-answer"])
    q = "Ile dni ma urząd na zwrot nadwyżki VAT? (test izolacji modeli demo)"
    a = api._answer(q, "hyde", "llm", demo)
    assert calls and set(calls) == {"demo-answer"}, calls
    assert a.get("error") is None and a["llm_check"]["verdict"] == "pass"
    assert L.system_llm() is None  # kontekst wyczyszczony po odpowiedzi


def test_embedding_fallback_to_local_when_api_fails() -> None:
    from raglab.rag.variants import FallbackVector
    from raglab.search.chunking import Chunk  # noqa: F401
    from raglab.search.index import Hit

    class Broken:
        def search(self, q: str, k: int = 20) -> list[Hit]:
            raise RuntimeError("OpenRouter 503")

    class Local:
        def search(self, q: str, k: int = 20) -> list[Hit]:
            return []

    fb = FallbackVector(Broken(), [])  # type: ignore[arg-type]
    fb._backup = Local()  # type: ignore[assignment]
    assert fb.search("stawka VAT") == [] and fb.last_used.startswith("mmlw")


def test_topic_filter_passes_every_eval_question() -> None:
    import json

    from raglab.api import looks_like_tax
    from raglab.ingest.sources import REPO_ROOT

    qs = [json.loads(x)["question"] for x in (REPO_ROOT / "data/eval/retrieval_v1.jsonl").read_text().splitlines()]
    gold = [json.loads(x) for x in (REPO_ROOT / "data/eval/golden/golden_v1.jsonl").read_text().splitlines()]
    qs += [g["question"] for g in gold if g["category"] != "out_of_corpus"]
    assert [q for q in qs if not looks_like_tax(q)] == []
    assert looks_like_tax("Czy fryzjer musi mieć kasę fiskalną?")
    assert not looks_like_tax("Podaj przepis na sernik")


def test_partial_answer_from_unfinished_json() -> None:
    from raglab.llm import partial_answer

    assert partial_answer("") == ""
    assert partial_answer('{"answer": "Termin wyn') == "Termin wyn"
    assert partial_answer('{"answer": "Stawka \\"8%\\" i\\nnowa linia') == 'Stawka "8%" i\nnowa linia'
    assert partial_answer('{"answer": "pół\\u00') == "pół"  # niedokończona sekwencja \u — czekamy na resztę
    assert partial_answer('{"answer": "\\u017c", "citations": ["VAT art. 87"]}') == "ż"
    assert partial_answer('```json\n{"answer": "x"}') == "x"


def test_stream_endpoint_emits_progress_text_and_final(monkeypatch, api) -> None:  # type: ignore[no-untyped-def]
    """/ask/stream: kontekst → tekst odpowiedzi narastająco → done z tym samym wynikiem co /ask."""
    import json

    import raglab.llm as L

    def fake_answer(question, variant, verify, llm, on_verify=None):  # type: ignore[no-untyped-def]
        L.progress("context", context=[{"address": "VAT art. 87 ust. 2"}])
        cb = L.answer_stream()
        assert cb is not None
        raw = '{"answer": "Termin wynosi 40 dni.", "citations": ["VAT art. 87 ust. 2"]}'
        for i in range(10, len(raw) + 1, 10):
            cb(raw[:i])
        return {"answer": "Termin wynosi 40 dni.", "citations": ["VAT art. 87 ust. 2"], "refused": False,
                "context": [], "served_model": "demo-answer"}  # fmt: skip

    monkeypatch.setattr(api, "LIVE", True)
    monkeypatch.setattr(api, "_answer", fake_answer)
    monkeypatch.setattr(api, "_demo_llm", lambda: object())
    monkeypatch.setattr(api.traces, "save", lambda *a, **k: None)
    monkeypatch.setattr(api, "_check_limits", lambda ip: None)
    r = TestClient(api.app).post("/ask/stream", json={"question": "Ile dni na zwrot nadwyżki VAT? (stream)"})
    ev = [json.loads(x) for x in r.text.splitlines() if x.strip()]
    kinds = [e["type"] for e in ev]
    assert kinds[0] == "stage" and "context" in kinds and kinds[-1] == "done"
    texts = [e["text"] for e in ev if e["type"] == "answer"]
    assert texts and texts[-1] == "Termin wynosi 40 dni."
    assert ev[-1]["result"]["answer"] == "Termin wynosi 40 dni."
    assert L._progress.get() is None  # kontekst postępu nie wycieka poza wątek zapytania


def test_eval_path_does_not_stream() -> None:
    """Bez słuchacza postępu (ewaluacja) answer_stream() = None → zwykłe zapytania, wyniki bez zmian."""
    from raglab.llm import answer_stream

    assert answer_stream() is None


def test_search_bm25_without_llm(api) -> None:  # type: ignore[no-untyped-def]
    # /search: sam BM25 — działa bez kluczy i bez embeddingów (test wdrożenia w klastrze, helm test)
    client = TestClient(api.app)
    r = client.get("/search", params={"q": "stawka podatku na usługi", "k": 3})
    assert r.status_code == 200
    d = r.json()
    assert d["mode"] == "bm25" and len(d["hits"]) == 3
    assert all(h["id"] and h["header"] for h in d["hits"])
    assert client.get("/search", params={"q": "a"}).status_code == 400
