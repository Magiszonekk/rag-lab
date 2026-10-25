"""Wariant agentowy (koncept, wariant 3): model sam decyduje, czego jeszcze szukać, zanim odpowie.

Pętla w LangGraph:  retrieve (hybryda + HyDE, jak wariant `hyde`) → plan ⇄ tools → answer.

W kroku `plan` model widzi pytanie i dotychczas zebrane przepisy i wybiera JEDNĄ akcję (protokół JSON, bez
natywnego tool-callingu — działa z każdym modelem przez bramkę OpenAI-compatible):
- {"action": "get", "addresses": ["VAT art. 86a ust. 1", ...]}  — pobierz przepisy po adresie (najczęściej
  ustęp, do którego odsyła tekst, albo brakujący ustęp artykułu, którego fragmenty już są);
- {"action": "search", "query": "..."}                          — dodatkowe wyszukiwanie innym sformułowaniem;
- {"action": "answer"}                                          — kontekst wystarcza (albo nic więcej nie znajdę).

Limity: najwyżej MAX_STEPS kroków narzędzi, 4 adresy na krok, budżet kontekstu. Model nigdy nie odpowiada
z pamięci — adresy, które poda, muszą istnieć w korpusie (inaczej zwracamy „nie ma takiego przepisu”), a
odpowiedź końcową pisze ten sam prompt co w pozostałych wariantach.
"""

from __future__ import annotations

import time
from typing import Any, TypedDict

from langgraph.graph import END, StateGraph

from raglab.llm import LLM, LLMError, parse_json
from raglab.rag.context import Block, attach_overrides, block_for, build_context
from raglab.rag.variants import RETRIEVERS, SYSTEM_PROMPT, Answer, render_context
from raglab.search.chunking import est_tokens

MAX_STEPS = 3
MAX_ADDRESSES = 4
BUDGET = 9000  # tokenów kontekstu (wariant `hyde`: 6000 + przepisy przejściowe)

PLAN_PROMPT = """Odpowiadasz na pytanie o polskie prawo podatkowe wyłącznie na podstawie przepisów (VAT, PIT,
Ordynacja podatkowa). Zanim odpowiesz, sprawdź, czy zebrane przepisy wystarczają.

Typowe braki:
- tekst odsyła do innego przepisu („o którym mowa w art. 113 ust. 13”, „zgodnie z ust. 1”), który rozstrzyga
  pytanie, a nie ma go niżej;
- są fragmenty artykułu (np. ust. 2–5), ale brakuje ustępu z zasadą ogólną (często ust. 1);
- pytanie dotyczy wyjątku lub limitu, a jest tylko zasada (albo odwrotnie).

Wybierz JEDNĄ akcję i odpowiedz wyłącznie JSON:
{{"action": "get", "addresses": ["VAT art. 86a ust. 1"], "why": "krótko"}}   — pobierz przepisy po adresie
   (najwyżej {max_addr}; adres w formie „VAT|PIT|Ordynacja art. N [ust. N|§ N] [pkt N]”);
{{"action": "search", "query": "sformułowanie w języku ustawy", "why": "krótko"}}  — wyszukaj jeszcze raz;
{{"action": "answer", "why": "krótko"}}  — przepisy wystarczają albo dalsze szukanie nic nie da.

Nie podawaj odpowiedzi na pytanie. Kroków zostało: {left}.

PYTANIE: {question}

ZEBRANE PRZEPISY:
{context}

DOTYCHCZASOWE KROKI:
{log}"""


class State(TypedDict):
    question: str
    blocks: list[Block]
    seen: set[tuple[str, str]]
    log: list[dict[str, Any]]
    steps: int
    action: dict[str, Any]
    tokens: list[int]  # [prompt, completion]


def _addr_key(b: Block) -> str:
    return b.address


def _merge(state: State, new: list[Block]) -> list[str]:
    have = {_addr_key(b) for b in state["blocks"]}
    covered = {u for b in state["blocks"] for u in b.units}
    added = []
    used = sum(est_tokens(b.text) for b in state["blocks"])
    for b in new:
        if _addr_key(b) in have or (b.units and b.units <= covered):
            continue
        if used + est_tokens(b.text) > BUDGET:
            break
        state["blocks"].append(b)
        state["seen"].add((b.act, b.article))
        used += est_tokens(b.text)
        added.append(b.address)
    return added


class Agent:
    def __init__(self, llm: LLM) -> None:
        self.llm = llm
        g = StateGraph(State)
        g.add_node("retrieve", self.retrieve)
        g.add_node("plan", self.plan)
        g.add_node("tools", self.tools)
        g.set_entry_point("retrieve")
        g.add_edge("retrieve", "plan")
        g.add_conditional_edges("plan", self.route, {"tools": "tools", "answer": END})
        g.add_edge("tools", "plan")
        self.graph = g.compile()

    # --- węzły ---
    def retrieve(self, state: State) -> State:
        hits = RETRIEVERS["hyde"](state["question"])
        state["blocks"] = build_context(hits, k=5)
        state["seen"] = {(b.act, b.article) for b in state["blocks"]}
        state["log"].append({"step": "retrieve", "added": [b.address for b in state["blocks"]]})
        return state

    def plan(self, state: State) -> State:
        if state["steps"] >= MAX_STEPS:
            state["action"] = {"action": "answer", "why": "limit kroków"}
            return state
        prompt = PLAN_PROMPT.format(
            max_addr=MAX_ADDRESSES,
            left=MAX_STEPS - state["steps"],
            question=state["question"],
            context=render_context(state["blocks"]),
            log="\n".join(f"- {e}" for e in state["log"][1:]) or "(brak)",
        )
        try:
            c = self.llm.complete([{"role": "user", "content": prompt}], max_tokens=3000, temperature=0.0)
            state["tokens"][0] += c.prompt_tokens
            state["tokens"][1] += c.completion_tokens
            d = parse_json(c.text)
            if not isinstance(d, dict) or d.get("action") not in ("get", "search", "answer"):
                raise ValueError("zła akcja")
            state["action"] = d
        except (LLMError, ValueError) as e:
            state["action"] = {"action": "answer", "why": f"błąd planowania: {e}"[:120]}
        return state

    def route(self, state: State) -> str:
        return "tools" if state["action"].get("action") in ("get", "search") else "answer"

    def tools(self, state: State) -> State:
        a = state["action"]
        state["steps"] += 1
        if a["action"] == "get":
            found: list[Block] = []
            missing: list[str] = []
            for addr in [str(x) for x in (a.get("addresses") or [])][:MAX_ADDRESSES]:
                b = block_for(addr)
                if b is None:
                    missing.append(addr)
                else:
                    found.append(b)
            added = _merge(state, found)
            state["log"].append({"step": "get", "asked": a.get("addresses"), "added": added,
                                 "not_found": missing, "why": a.get("why")})  # fmt: skip
        else:
            q = str(a.get("query") or state["question"])
            hits = RETRIEVERS["hybrid"](q)
            added = _merge(state, build_context(hits, k=3))
            state["log"].append({"step": "search", "query": q, "added": added, "why": a.get("why")})
        return state


def run(question: str, llm: LLM) -> Answer:
    t0 = time.monotonic()
    agent = Agent(llm)
    init: State = {"question": question, "blocks": [], "seen": set(), "log": [], "steps": 0,
                   "action": {}, "tokens": [0, 0]}  # fmt: skip
    st: State = agent.graph.invoke(init)  # type: ignore[assignment]
    blocks = attach_overrides(st["blocks"], st["seen"], sum(est_tokens(b.text) for b in st["blocks"]), BUDGET)
    t1 = time.monotonic()
    user = f"PRZEPISY:\n\n{render_context(blocks)}\n\nPYTANIE UŻYTKOWNIKA:\n{question}"
    ctx = [{"address": b.address, "status": b.status, "note": b.note, "text": b.text} for b in blocks]
    base: dict[str, Any] = dict(variant="agentic", question=question, context=ctx,
                                retrieved=[b.address for b in blocks])  # fmt: skip
    try:
        c = llm.complete([{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": user}],
                         max_tokens=6000, temperature=0.0)  # fmt: skip
        d = parse_json(c.text)
        if not isinstance(d, dict):
            raise ValueError("odpowiedź nie jest obiektem JSON")
        t2 = time.monotonic()
        ans = Answer(**base, answer=str(d.get("answer", "")), citations=[str(x) for x in d.get("citations") or []],
                     refused=bool(d.get("refused")), pointer=d.get("pointer"), model=c.requested_model,
                     served_model=c.served_model, prompt_tokens=c.prompt_tokens + st["tokens"][0],
                     completion_tokens=c.completion_tokens + st["tokens"][1],
                     latency_ms={"agent": int((t1 - t0) * 1000), "generation": int((t2 - t1) * 1000)})  # fmt: skip
    except (LLMError, ValueError) as e:
        err = f"{type(e).__name__}: {e}"[:300]
        ans = Answer(**base, answer="", citations=[], refused=False, pointer=None, model=llm.models[0],
                     served_model="", prompt_tokens=0, completion_tokens=0, error=err)  # fmt: skip
    ans.trace = [{k: (sorted(v) if isinstance(v, set) else v) for k, v in e.items()} for e in st["log"]]
    return ans
