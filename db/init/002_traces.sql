-- Ślady (koncept D9): ślad → kroki → atrybuty. Źródło dla /trace/<id> i trybu porównania.
CREATE TABLE IF NOT EXISTS traces (
    id            TEXT PRIMARY KEY,               -- identyfikator pokazywany w UI (ten sam w Langfuse)
    created_at    TIMESTAMPTZ NOT NULL DEFAULT now(),
    source        TEXT NOT NULL,                  -- 'example' | 'live' | 'eval'
    variant       TEXT NOT NULL,
    verify        TEXT NOT NULL,
    question      TEXT NOT NULL,                  -- po maskowaniu PESEL/NIP/e-mail/telefonu
    answer        TEXT,
    refused       BOOLEAN,
    citations     JSONB,
    model         TEXT,                           -- model opisany ogólnie (nazwa publiczna), nie endpoint
    served_model  TEXT,
    prompt_tokens INTEGER,
    completion_tokens INTEGER,
    latency_ms    JSONB,
    error         TEXT
);
CREATE INDEX IF NOT EXISTS traces_created ON traces (created_at DESC);

CREATE TABLE IF NOT EXISTS trace_steps (
    trace_id  TEXT NOT NULL REFERENCES traces(id) ON DELETE CASCADE,
    seq       INTEGER NOT NULL,
    kind      TEXT NOT NULL,                      -- retrieve | plan | get | search | context | generate | verify
    attrs     JSONB NOT NULL,                     -- fragmenty, adresy, tokeny, czas, decyzje agenta
    PRIMARY KEY (trace_id, seq)
);
