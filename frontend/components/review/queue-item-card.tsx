"use client";

import Link from "next/link";

import {
  confidencePresentation,
  recommendationShortLabel,
} from "@/components/ai/presentation";
import { decisionPresentation } from "@/components/decisions/decision-presentation";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import type { ReviewQueueItem } from "@/types/review";

import { activityLabel, queueHref, queuePresentation } from "./queue-presentation";

// One queue item as a responsive card (works on desktop and one-handed on mobile). The
// situation is understandable without opening it: who, role, stage, recommendation +
// evidence confidence if evaluated, last activity, and exactly ONE contextual action.
export function QueueItemCard({ item }: { item: ReviewQueueItem }) {
  const p = queuePresentation(item);
  const href = queueHref(item);
  // AI output is SECONDARY to the recruiter's attention reason — shown small + muted below
  // the stage, never at equal weight. The queue optimizes for work, not for the AI verdict.
  const recommendationLabel =
    item.recommendation != null ? recommendationShortLabel(item.recommendation) : null;

  return (
    <div
      className={cn(
        "bg-card flex flex-col gap-3 rounded-xl border p-4 shadow-subtle transition-colors sm:flex-row sm:items-center sm:gap-4",
        p.quiet && "opacity-80",
        !p.quiet && "border-l-2",
        !p.quiet && (p.icon === "text-warning" ? "border-l-warning/50" : "border-l-primary/50"),
      )}
    >
      <div className="min-w-0 flex-1 space-y-1.5">
        <div className="flex flex-wrap items-center gap-x-2 gap-y-1">
          <span className="truncate font-medium">{item.candidate_name}</span>
          <span className="text-muted-foreground truncate text-sm">· {item.role_title}</span>
        </div>
        {/* The attention reason is the dominant signal on the row; a recorded human
            decision (if any) sits beside it as a resolved-outcome badge. */}
        <div className="flex flex-wrap items-center gap-2">
          <span
            className={cn(
              "inline-flex items-center gap-1.5 rounded-full px-2.5 py-1 text-sm font-medium",
              p.chip,
            )}
          >
            <p.Icon className={cn("size-4", p.icon)} aria-hidden />
            {p.stageLabel}
          </span>
          {item.decision && (
            <Badge variant={decisionPresentation(item.decision).badge} className="normal-case">
              Decided: {decisionPresentation(item.decision).label}
            </Badge>
          )}
        </div>
        {/* AI recommendation + evidence confidence — secondary, muted, never equal weight. */}
        {recommendationLabel && (
          <p className="text-muted-foreground text-xs">
            Recommendation: {recommendationLabel} ·{" "}
            {confidencePresentation(item.confidence ?? 0).label}
          </p>
        )}
      </div>

      <div className="flex items-center justify-between gap-3 sm:justify-end">
        <span className="text-muted-foreground text-xs tabular-nums">{activityLabel(item)}</span>
        <Link href={href}>
          <Button variant={p.quiet ? "ghost" : "outline"} size="sm">
            {p.actionLabel}
          </Button>
        </Link>
      </div>
    </div>
  );
}
