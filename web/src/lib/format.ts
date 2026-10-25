const nf = new Intl.NumberFormat("pl-PL");
export const fmtInt = (n: number | undefined | null) => (n == null ? "—" : nf.format(Math.round(n)));
export function fmtSec(ms: number | undefined | null): string {
  if (ms == null) return "—";
  const s = ms / 1000;
  return `${s < 10 ? s.toFixed(1) : Math.round(s)} s`.replace(".", ",");
}
export const fmt3 = (x: number) => x.toFixed(3).replace(".", ",");
export const pct = (x: number) => `${Math.round(x * 100)}%`;
export const fmtCI = (ci: [number, number]) => `${fmt3(ci[0])}–${fmt3(ci[1])}`;
