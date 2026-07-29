"use client";

import { ChevronDown, Wrench } from "lucide-react";
import { useState } from "react";

import { cn } from "@/lib/utils";
import type { EvaluationDetail } from "@/types/evaluation";

// Collapsed by default — useful for auditability, but it must not dominate the recruiter's
// experience. Contains provenance + token usage only. NEVER raw prompts, provider
// responses, minimized payloads, keys, or debugging internals.
export function EvaluationTechnicalDetails({ detail }: { detail: EvaluationDetail }) {
  const [open, setOpen] = useState(false);
  const p = detail.provenance;

  const rows: Array<[string, string]> = [
    ["Provider", p.provider],
    ["Model", p.model],
    ["Model version", p.model_version],
    ["Prompt version", p.prompt_version],
    ["Confidence algorithm", p.confidence_algorithm_version],
    ["Generated", new Date(p.generated_at).toLocaleString()],
    ["Input fingerprint", detail.input_fingerprint],
    [
      "Token usage",
      detail.input_tokens != null && detail.output_tokens != null
        ? `${detail.input_tokens} in / ${detail.output_tokens} out`
        : "not reported",
    ],
  ];

  return (
    <div className="rounded-xl border">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        className="hover:bg-muted/30 flex w-full items-center justify-between gap-2 rounded-xl px-5 py-3 text-left transition-colors"
      >
        <span className="text-muted-foreground flex items-center gap-2 text-sm font-medium">
          <Wrench className="size-4" aria-hidden />
          Evaluation details
        </span>
        <ChevronDown
          className={cn("text-muted-foreground size-4 transition-transform", open && "rotate-180")}
          aria-hidden
        />
      </button>
      {open && (
        <dl className="grid gap-x-6 gap-y-2 border-t px-5 py-4 text-sm sm:grid-cols-2">
          {rows.map(([k, v]) => (
            <div key={k} className="flex flex-col gap-0.5">
              <dt className="text-muted-foreground text-xs">{k}</dt>
              <dd className="break-words font-mono text-xs">{v}</dd>
            </div>
          ))}
        </dl>
      )}
    </div>
  );
}
