"use client";

import { Info } from "lucide-react";
import { useState } from "react";

import { cn } from "@/lib/utils";

import {
  CONFIDENCE_EXPLANATION,
  confidenceLevel,
  confidencePresentation,
} from "./presentation";

// Communicates how much to trust the assessment as *evidence reliability* — NOT a
// probability. The dominant message is the semantic level ("High / Moderate / Low evidence
// confidence"); the raw value appears only inside the explanation, as a reliability score
// out of 1.0 — never as "100%". Meaning is not carried by the bar alone (there's a text
// label + an accessible meter role).
export function ConfidenceMeter({
  value,
  emphasizeInsufficiency = false,
}: {
  value: number;
  emphasizeInsufficiency?: boolean;
}) {
  const [showWhy, setShowWhy] = useState(false);
  const { label, barClass, textClass, fill } = confidencePresentation(value);
  const level = confidenceLevel(value);

  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between gap-3">
        <span className={cn("text-sm font-medium", textClass)}>{label}</span>
        <button
          type="button"
          onClick={() => setShowWhy((v) => !v)}
          aria-expanded={showWhy}
          className="text-muted-foreground hover:text-foreground focus-visible:ring-ring inline-flex items-center gap-1 rounded text-xs focus-visible:outline-none focus-visible:ring-2"
        >
          <Info className="size-3.5" aria-hidden />
          What does this mean?
        </button>
      </div>

      <div
        role="meter"
        aria-valuemin={0}
        aria-valuemax={1}
        aria-valuenow={Number(value.toFixed(2))}
        aria-label={label}
        className="bg-muted h-2 w-full overflow-hidden rounded-full"
      >
        <div
          className={cn("h-full rounded-full transition-all", barClass)}
          style={{ width: `${Math.max(4, Math.round(fill * 100))}%` }}
        />
      </div>

      {emphasizeInsufficiency && level === "low" && (
        <p className="text-muted-foreground text-xs">
          The evidence is too thin or inconsistent to support a confident recommendation.
        </p>
      )}

      {showWhy && (
        <div className="text-muted-foreground bg-muted/40 space-y-1 rounded-lg border p-3 text-xs leading-relaxed">
          <p>{CONFIDENCE_EXPLANATION}</p>
          <p className="tabular-nums">
            Evidence-reliability score:{" "}
            <span className="text-foreground font-medium">{value.toFixed(2)}</span> of 1.0
          </p>
        </div>
      )}
    </div>
  );
}
