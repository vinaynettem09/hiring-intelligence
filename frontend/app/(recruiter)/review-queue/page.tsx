"use client";

import { Inbox, Search } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";

import { QueueFilters } from "@/components/review/queue-filters";
import { QueueItemCard } from "@/components/review/queue-item-card";
import { EmptyState } from "@/components/feedback/empty-state";
import { ErrorState } from "@/components/feedback/error-state";
import { FadeIn, StaggerItem, StaggerList } from "@/components/motion/motion";
import { Button, buttonVariants } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Skeleton } from "@/components/ui/skeleton";
import { ApiError } from "@/lib/api-client";
import { authStore } from "@/lib/auth-store";
import { cn } from "@/lib/utils";
import { ReviewService } from "@/services/review-service";
import type { QueueFilter, ReviewQueueResponse } from "@/types/review";

const LIMIT = 20;

function summarySentence(s: ReviewQueueResponse["summary"]): string {
  if (s.total === 0) return "Candidates appear here as they move through your campaigns.";
  const attention = s.needs_review + s.ready_to_evaluate + s.awaiting_invitation;
  const parts: string[] = [];
  if (attention > 0) parts.push(`${attention} need${attention === 1 ? "s" : ""} your attention`);
  if (s.waiting_on_candidate > 0) parts.push(`${s.waiting_on_candidate} waiting on candidates`);
  if (s.completed > 0) parts.push(`${s.completed} completed`);
  return parts.length ? parts.join(" · ") : "You're all caught up.";
}

export default function ReviewQueuePage() {
  const router = useRouter();
  const [filter, setFilter] = useState<QueueFilter>("all");
  const [searchInput, setSearchInput] = useState("");
  const [search, setSearch] = useState("");
  const [offset, setOffset] = useState(0);
  const [data, setData] = useState<ReviewQueueResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<{ message: string; correlationId: string | null } | null>(
    null,
  );

  // Debounce the search box; searching resets to the first page.
  useEffect(() => {
    const t = setTimeout(() => {
      setSearch(searchInput);
      setOffset(0);
    }, 300);
    return () => clearTimeout(t);
  }, [searchInput]);

  const load = useCallback(() => {
    setLoading(true);
    setError(null);
    ReviewService.getQueue({ filter, search, limit: LIMIT, offset })
      .then((res) => setData(res.data))
      .catch((e: unknown) => {
        if (e instanceof ApiError && e.status === 401) {
          router.replace("/login");
          return;
        }
        setError({
          message: e instanceof Error ? e.message : "Failed to load the review queue",
          correlationId: e instanceof ApiError ? e.body.correlation_id : null,
        });
      })
      .finally(() => setLoading(false));
  }, [filter, search, offset, router]);

  useEffect(() => {
    if (!authStore.getAccess()) {
      router.replace("/login");
      return;
    }
    load();
  }, [load, router]);

  const header = (
    <div className="space-y-1">
      <h1 className="text-2xl font-semibold tracking-tight">Review queue</h1>
      <p className="text-muted-foreground text-sm">
        {data ? summarySentence(data.summary) : "Your evaluation work, in one place."}
      </p>
    </div>
  );

  if (error) {
    return (
      <div className="space-y-6">
        {header}
        <ErrorState
          message={error.message}
          correlationId={error.correlationId}
          action={
            <Button variant="outline" size="sm" onClick={load}>
              Try again
            </Button>
          }
        />
      </div>
    );
  }

  const items = data?.items ?? [];
  const total = data?.total ?? 0;
  const shownFrom = total === 0 ? 0 : offset + 1;
  const shownTo = Math.min(offset + LIMIT, total);

  return (
    <FadeIn className="space-y-6">
      {header}

      {data && <QueueFilters summary={data.summary} active={filter} onChange={(f) => { setFilter(f); setOffset(0); }} />}

      <div className="relative max-w-sm">
        <Search className="text-muted-foreground pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2" aria-hidden />
        <Input
          type="search"
          placeholder="Search by candidate or role…"
          value={searchInput}
          onChange={(e) => setSearchInput(e.target.value)}
          aria-label="Search by candidate name or role"
          className="pl-9"
        />
      </div>

      {loading && !data ? (
        <div className="space-y-3">
          {[0, 1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-20 w-full rounded-xl" />
          ))}
        </div>
      ) : items.length === 0 ? (
        total === 0 && data?.summary.total === 0 ? (
          <EmptyState
            icon={Inbox}
            title="Your review queue is empty"
            description="As candidates are invited, submit work samples, and get evaluated, they'll show up here in priority order."
            action={
              <Link href="/campaigns" className={cn(buttonVariants({ variant: "outline" }))}>
                Go to campaigns
              </Link>
            }
          />
        ) : (
          <EmptyState
            icon={Inbox}
            title="Nothing here"
            description="No items match this view. Try a different filter or clear your search."
          />
        )
      ) : (
        <>
          <StaggerList className="space-y-3">
            {items.map((item) => (
              <StaggerItem key={item.candidate_evaluation_id}>
                <QueueItemCard item={item} />
              </StaggerItem>
            ))}
          </StaggerList>

          {total > LIMIT && (
            <div className="flex items-center justify-between border-t pt-4">
              <p className="text-muted-foreground text-xs tabular-nums">
                Showing {shownFrom}–{shownTo} of {total}
              </p>
              <div className="flex gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  disabled={offset === 0 || loading}
                  onClick={() => setOffset((o) => Math.max(0, o - LIMIT))}
                >
                  Previous
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  disabled={offset + LIMIT >= total || loading}
                  onClick={() => setOffset((o) => o + LIMIT)}
                >
                  Next
                </Button>
              </div>
            </div>
          )}
        </>
      )}
    </FadeIn>
  );
}
