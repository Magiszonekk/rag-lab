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
