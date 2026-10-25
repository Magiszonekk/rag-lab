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

export const compare = (question: string, verify: boolean) =>
  call<Record<VariantId, VariantAnswer>>("/compare", { method: "POST", body: JSON.stringify({ question, verify: verify ? "llm" : "off" }) }, 240_000);
