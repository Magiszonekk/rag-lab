// Jeden zestaw ikon: obrys 1.75, zaokrąglone końce, siatka 24.
const P: Record<string, string> = {
  search: "M11 4a7 7 0 1 0 0 14 7 7 0 0 0 0-14zm9 16-4.2-4.2",
  get: "M5 12h11m-4-4 4 4-4 4M19 5v14",
  research: "M4 7h9M4 12h6M4 17h5m6-6a3.5 3.5 0 1 0 0 7 3.5 3.5 0 0 0 0-7zm2.5 6 2.5 2.5",
  context: "M7 3h7l5 5v13H7zM14 3v5h5M10 12h6M10 16h6",
  generate: "M4 20h4L19 9l-4-4L4 16zM13.5 6.5l4 4",
  verify: "M12 3 5 6v5c0 4.5 3 8.4 7 10 4-1.6 7-5.5 7-10V6zm-3 9 2 2 4-4",
  check: "m5 12.5 4.5 4.5L19 7.5",
  x: "M6 6l12 12M18 6 6 18",
  alert: "M12 4 2.8 19.5h18.4zM12 10v4.5m0 2.8v.2",
  info: "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zm0 8v5m0-8.2v.2",
  clock: "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zm0 4.5V12l3 2",
  tokens: "M4 8.5h16M4 15.5h16M9.5 4 8 20m8-16-1.5 16",
  chevron: "m6 9 6 6 6-6",
  external: "M14 4h6v6m0-6-9 9M18 14v6H4V6h6",
  sun: "M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8zm0-5v2m0 14v2M3 12h2m14 0h2M5.6 5.6 7 7m10 10 1.4 1.4M5.6 18.4 7 17M17 7l1.4-1.4",
  moon: "M20 14.5A8 8 0 0 1 9.5 4 8 8 0 1 0 20 14.5z",
  system: "M3 5h18v11H3zM8 20h8m-4-4v4",
  book: "M4 5.5C6.5 4 9.5 4 12 6c2.5-2 5.5-2 8-.5V19c-2.5-1.5-5.5-1.5-8 .5-2.5-2-5.5-2-8-.5z M12 6v13.5",
  hourglass: "M7 3h10M7 21h10M8 3c0 4 8 5 8 9s-8 5-8 9M16 3c0 4-8 5-8 9s8 5 8 9",
  refuse: "M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM5.6 5.6l12.8 12.8",
  scale: "M12 4v16M5 20h14M6 8h12M6 8l-3 6a3 3 0 0 0 6 0zm12 0-3 6a3 3 0 0 0 6 0z",
  github: "M9 19c-4 1.3-4-2-6-2.5M15 21v-3.4a3 3 0 0 0-.8-2.3c2.7-.3 5.5-1.3 5.5-6a4.6 4.6 0 0 0-1.3-3.2 4.3 4.3 0 0 0-.1-3.2s-1-.3-3.4 1.3a11.6 11.6 0 0 0-6 0C6.6 2.6 5.6 2.9 5.6 2.9a4.3 4.3 0 0 0-.1 3.2A4.6 4.6 0 0 0 4.2 9.3c0 4.6 2.8 5.7 5.5 6a3 3 0 0 0-.8 2.3V21",
  arrow: "M5 12h14m-5-5 5 5-5 5",
  spark: "M12 3v4m0 10v4M3 12h4m10 0h4",
};

export function Icon({ name, size = 18, className }: { name: keyof typeof P | string; size?: number; className?: string }) {
  return (
    <svg
      className={className ? `icon ${className}` : "icon"}
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth={1.75}
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d={P[name] ?? P.info} />
    </svg>
  );
}
