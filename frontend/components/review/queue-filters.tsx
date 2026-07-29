"use client";

import { cn } from "@/lib/utils";
import type { QueueFilter, ReviewQueueSummary } from "@/types/review";

// Compact filter chips (not four giant KPI cards) that double as the at-a-glance summary:
// each chip carries a whole-queue count. Selecting one scopes the list server-side.
export function QueueFilters({
  summary,
  active,
  onChange,
}: {
  summary: ReviewQueueSummary;
  active: QueueFilter;
  onChange: (f: QueueFilter) => void;
}) {
  const needsAttention =
    summary.needs_review + summary.ready_to_evaluate + summary.awaiting_invitation;

  // "Needs attention" leads and is visually primary — a recruiter should instantly read
  // "I have N things to do." Everything else is secondary.
  const chips: Array<{ key: QueueFilter; label: string; count: number; primary?: boolean }> = [
    { key: "needs_attention", label: "Needs attention", count: needsAttention, primary: true },
    { key: "all", label: "All", count: summary.total },
    { key: "ready", label: "Ready to evaluate", count: summary.ready_to_evaluate },
    { key: "waiting", label: "Waiting on candidates", count: summary.waiting_on_candidate },
    { key: "completed", label: "Completed", count: summary.completed },
  ];

  return (
    <div role="tablist" aria-label="Filter review queue" className="flex flex-wrap gap-2">
      {chips.map((c) => {
        const selected = active === c.key;
        const primaryLoud = c.primary && c.count > 0;
        return (
          <button
            key={c.key}
            role="tab"
            aria-selected={selected}
            onClick={() => onChange(c.key)}
            className={cn(
              "focus-visible:ring-ring inline-flex items-center gap-2 rounded-full border px-3 py-1.5 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2",
              selected
                ? "border-primary bg-primary/10 text-primary"
                : primaryLoud
                  ? "border-primary/50 text-foreground hover:bg-primary/5"
                  : "text-muted-foreground hover:text-foreground hover:bg-muted",
            )}
          >
            {c.label}
            <span
              className={cn(
                "min-w-5 rounded-full px-1.5 text-center text-xs font-semibold tabular-nums",
                selected
                  ? "bg-primary/20"
                  : primaryLoud
                    ? "bg-primary text-primary-foreground"
                    : "bg-muted text-muted-foreground",
              )}
            >
              {c.count}
            </span>
          </button>
        );
      })}
    </div>
  );
}
