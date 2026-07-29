"use client";

import { History } from "lucide-react";
import { useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import type { EvaluationRunSummary } from "@/types/evaluation";

import { confidenceLevel, recommendationShortLabel } from "./presentation";

// Evaluation runs are immutable; a rerun is a NEW run and never overwrites a prior one.
// History makes that visible: every run is listed, the latest is marked, none are merged.
// Provider/model live in technical details, not here.
export function EvaluationHistory({
  runs,
  latestRunNumber,
}: {
  runs: EvaluationRunSummary[];
  latestRunNumber: number;
}) {
  const [open, setOpen] = useState(false);
  if (runs.length <= 1) return null; // nothing to compare yet

  return (
    <Card className="p-5">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        className="flex w-full items-center justify-between gap-2 text-left"
      >
        <span className="flex items-center gap-2 text-sm font-semibold">
          <History className="text-muted-foreground size-4" aria-hidden />
          Evaluation history
          <span className="text-muted-foreground font-normal">
            ({runs.length} runs, immutable)
          </span>
        </span>
        <span className="text-muted-foreground text-xs">{open ? "Hide" : "View history"}</span>
      </button>

      {open && (
        <ul className="mt-4 space-y-2">
          {runs.map((run) => {
            const level = confidenceLevel(run.confidence);
            return (
              <li
                key={run.id}
                className="flex flex-wrap items-center gap-x-3 gap-y-1 rounded-lg border px-3 py-2 text-sm"
              >
                <span className="font-medium tabular-nums">Run {run.run_number}</span>
                {run.run_number === latestRunNumber && (
                  <Badge variant="primary" className="normal-case">
                    latest
                  </Badge>
                )}
                <span className="text-muted-foreground">
                  {recommendationShortLabel(run.recommendation)}
                </span>
                <span
                  className={cn(
                    "text-xs",
                    level === "high"
                      ? "text-foreground"
                      : level === "moderate"
                        ? "text-warning"
                        : "text-muted-foreground",
                  )}
                >
                  {level} evidence confidence
                </span>
                <span className="text-muted-foreground ml-auto text-xs tabular-nums">
                  {new Date(run.created_at).toLocaleString()}
                </span>
              </li>
            );
          })}
        </ul>
      )}
    </Card>
  );
}
