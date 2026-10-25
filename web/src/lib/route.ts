import { useEffect, useState } from "react";

export type Screen = "zapytaj" | "porownaj" | "slad" | "wyniki" | "o-projekcie";
export const SCREENS: { id: Screen; label: string }[] = [
  { id: "zapytaj", label: "Zapytaj" },
  { id: "porownaj", label: "Porównaj" },
  { id: "slad", label: "Ślad" },
  { id: "wyniki", label: "Wyniki" },
  { id: "o-projekcie", label: "Jak to działa" },
];

export interface Route {
  screen: Screen;
  params: URLSearchParams;
}

function parse(): Route {
  const h = window.location.hash.replace(/^#\/?/, "");
  const [path, qs] = h.split("?");
  const screen = (SCREENS.find((s) => s.id === path)?.id ?? "zapytaj") as Screen;
  return { screen, params: new URLSearchParams(qs ?? "") };
}

export function useRoute(): Route {
  const [r, setR] = useState(parse);
  useEffect(() => {
    const on = () => setR(parse());
    window.addEventListener("hashchange", on);
    return () => window.removeEventListener("hashchange", on);
  }, []);
  return r;
}

export function href(screen: Screen, params?: Record<string, string | undefined>): string {
  const p = new URLSearchParams();
  Object.entries(params ?? {}).forEach(([k, v]) => v && p.set(k, v));
  const qs = p.toString();
  return `#/${screen}${qs ? `?${qs}` : ""}`;
}

/** Zmienia parametry w adresie bez nowego wpisu w historii. */
export function setParams(screen: Screen, params: Record<string, string | undefined>) {
  const url = href(screen, params);
  if (window.location.hash !== url) {
    history.replaceState(null, "", url);
    window.dispatchEvent(new HashChangeEvent("hashchange"));
  }
}
