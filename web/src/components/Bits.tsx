import { useId, useState, type ReactNode } from "react";
import type { Category, VariantAnswer, VariantId } from "../lib/types";
import { VARIANTS } from "../lib/types";
import { VARIANT_INFO, verdictLabel, CATEGORY, EXAMPLE_TITLE } from "../lib/labels";
import { Icon } from "./Icon";
import type { Example } from "../lib/types";

export function VerdictBadge({ answer, category }: { answer: VariantAnswer; category: Category }) {
  const v = verdictLabel(answer.judge?.verdict, category);
  const icon = v.tone === "ok" ? "check" : v.tone === "bad" ? "x" : v.tone === "partial" ? "alert" : v.tone === "none" ? "info" : "refuse";
  return (
    <span className={`verdict tone-${v.tone}`} title={v.title}>
      <Icon name={icon} size={15} />
      {v.label}
    </span>
  );
}

export function Segmented<T extends string>({
  value,
  options,
  onChange,
  label,
  size = "md",
}: {
  value: T;
  options: { value: T; label: ReactNode; hint?: string }[];
  onChange: (v: T) => void;
  label: string;
  size?: "sm" | "md";
}) {
  return (
    <div className={`segmented seg-${size}`} role="radiogroup" aria-label={label}>
      {options.map((o) => (
        <button
          key={o.value}
          type="button"
          role="radio"
          aria-checked={value === o.value}
          className={value === o.value ? "is-on" : undefined}
          onClick={() => onChange(o.value)}
          title={o.hint}
        >
          {o.label}
        </button>
      ))}
    </div>
  );
}

export function VariantPicker({ value, onChange }: { value: VariantId; onChange: (v: VariantId) => void }) {
  return (
    <Segmented
      label="Wariant"
      value={value}
      onChange={onChange}
      options={VARIANTS.map((v) => ({ value: v, label: VARIANT_INFO[v].name, hint: VARIANT_INFO[v].how }))}
    />
  );
}

export function Switch({ checked, onChange, label, hint }: { checked: boolean; onChange: (v: boolean) => void; label: string; hint?: string }) {
  return (
    <label className="switch">
      <input type="checkbox" role="switch" checked={checked} onChange={(e) => onChange(e.target.checked)} />
      <span className="switch-track" aria-hidden="true">
        <span className="switch-thumb" />
      </span>
      <span className="switch-text">
        <span className="switch-label">{label}</span>
        {hint && <span className="switch-hint">{hint}</span>}
      </span>
    </label>
  );
}

export function ExamplePicker({
  examples,
  value,
  onChange,
  compact = false,
}: {
  examples: Example[];
  value: string | null;
  onChange: (id: string) => void;
  compact?: boolean;
}) {
  return (
    <div className={`example-picker${compact ? " is-compact" : ""}`} role="listbox" aria-label="Gotowe przykłady">
      {examples.map((e) => (
        <button
          key={e.id}
          type="button"
          role="option"
          aria-selected={value === e.id}
          className={value === e.id ? "is-on" : undefined}
          onClick={() => onChange(e.id)}
          title={e.question}
        >
          <span className="ex-title">{EXAMPLE_TITLE[e.id] ?? e.question}</span>
          <span className="ex-cat">{CATEGORY[e.category] ?? e.category}</span>
        </button>
      ))}
    </div>
  );
}

export function Notice({ tone = "info", children, icon }: { tone?: "info" | "warn" | "danger"; children: ReactNode; icon?: string }) {
  return (
    <div className={`notice notice-${tone}`} role={tone === "danger" ? "alert" : "status"}>
      <Icon name={icon ?? (tone === "info" ? "info" : "alert")} size={18} />
      <div>{children}</div>
    </div>
  );
}

/** Rozwijany blok: treść renderowana dopiero po otwarciu (zamknięty <details> i tak jest układany przez przeglądarkę). */
export function Disclosure({ summary, children, className }: { summary: ReactNode; children: ReactNode; className?: string }) {
  const [open, setOpen] = useState(false);
  const id = useId();
  return (
    <div className={`disclosure${open ? " is-open" : ""}${className ? ` ${className}` : ""}`}>
      <button type="button" className="disclosure-btn" aria-expanded={open} aria-controls={id} onClick={() => setOpen((o) => !o)}>
        {summary}
      </button>
      {open && <div id={id} className="disclosure-body">{children}</div>}
    </div>
  );
}
