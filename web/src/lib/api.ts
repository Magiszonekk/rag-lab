import type { VariantAnswer, VariantId } from "./types";

/** Adres API z VITE_API_URL. Brak = tylko gotowe przykłady (demo działa bez backendu). */
export const API_URL: string | null = (import.meta.env.VITE_API_URL as string | undefined)?.replace(/\/$/, "") || null;

export type ApiState =
  | { kind: "none" } // nie skonfigurowano API
  | { kind: "checking" }
  | { kind: "down" } // API nie odpowiada
  | { kind: "examples-only" } // API działa, live=false
  | { kind: "live" };

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

async function call<T>(path: string, init?: RequestInit, timeoutMs = 90_000): Promise<T> {
  if (!API_URL) throw new ApiError(0, "Brak adresu API.");
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const r = await fetch(API_URL + path, { ...init, signal: ctrl.signal, headers: { "content-type": "application/json" } });
    if (!r.ok) {
      let detail = `Błąd serwera (${r.status}).`;
      try {
        const j = await r.json();
        if (typeof j?.detail === "string") detail = j.detail;
      } catch {
        /* treść nie jest JSON-em */
      }
      throw new ApiError(r.status, detail);
    }
    return (await r.json()) as T;
  } catch (e) {
    if (e instanceof ApiError) throw e;
    if ((e as Error).name === "AbortError") throw new ApiError(0, "Serwer nie odpowiedział na czas.");
    throw new ApiError(0, "Nie udało się połączyć z serwerem demo.");
  } finally {
    clearTimeout(t);
  }
}

export async function checkHealth(): Promise<ApiState> {
  if (!API_URL) return { kind: "none" };
  try {
    const h = await call<{ ok: boolean; live: boolean }>("/health", undefined, 5000);
    return h.ok && h.live ? { kind: "live" } : { kind: "examples-only" };
  } catch {
    return { kind: "down" };
  }
}

export const ask = (question: string, variant: VariantId, verify: boolean) =>
  call<VariantAnswer>("/ask", { method: "POST", body: JSON.stringify({ question, variant, verify: verify ? "llm" : "off" }) });

export type StreamEvent =
  | { type: "stage"; stage: "search" | "verify" }
  | { type: "context"; addresses: string[] }
  | { type: "step"; step: "retrieve" | "get" | "search"; added?: string[]; query?: string; why?: string }
  | { type: "answer"; text: string }
  | { type: "done"; result: VariantAnswer };

/** /ask/stream (NDJSON): postęp i tekst odpowiedzi na bieżąco; zwraca wynik końcowy taki jak /ask. */
export async function askStream(
  question: string,
  variant: VariantId,
  verify: boolean,
  onEvent: (e: StreamEvent) => void,
  timeoutMs = 240_000,
): Promise<VariantAnswer> {
  if (!API_URL) throw new ApiError(0, "Brak adresu API.");
  const ctrl = new AbortController();
  const t = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const r = await fetch(API_URL + "/ask/stream", {
      method: "POST",
      signal: ctrl.signal,
      headers: { "content-type": "application/json" },
      body: JSON.stringify({ question, variant, verify: verify ? "llm" : "off" }),
    });
    if (!r.ok || !r.body) {
      let detail = `Błąd serwera (${r.status}).`;
      try {
        const j = await r.json();
        if (typeof j?.detail === "string") detail = j.detail;
      } catch {
        /* treść nie jest JSON-em */
      }
      throw new ApiError(r.status, detail);
    }
    const reader = r.body.getReader();
    const dec = new TextDecoder();
    let buf = "";
    let result: VariantAnswer | null = null;
    for (;;) {
      const { value, done } = await reader.read();
      if (done) break;
      buf += dec.decode(value, { stream: true });
      let nl: number;
      while ((nl = buf.indexOf("\n")) >= 0) {
        const line = buf.slice(0, nl).trim();
        buf = buf.slice(nl + 1);
        if (!line) continue; // podtrzymanie połączenia
        const e = JSON.parse(line) as StreamEvent;
        if (e.type === "done") result = e.result;
        else onEvent(e);
      }
    }
    if (!result) throw new ApiError(0, "Połączenie przerwane przed końcem odpowiedzi.");
    return result;
  } catch (e) {
    if (e instanceof ApiError) throw e;
    if ((e as Error).name === "AbortError") throw new ApiError(0, "Serwer nie odpowiedział na czas.");
    throw new ApiError(0, "Nie udało się połączyć z serwerem demo.");
  } finally {
    clearTimeout(t);
  }
}

export const compare = (question: string, verify: boolean) =>
  call<Record<VariantId, VariantAnswer>>("/compare", { method: "POST", body: JSON.stringify({ question, verify: verify ? "llm" : "off" }) }, 240_000);
