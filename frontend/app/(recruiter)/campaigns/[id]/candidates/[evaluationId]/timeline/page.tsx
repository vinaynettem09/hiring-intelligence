"use client";

import { ArrowLeft } from "lucide-react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";

import { useBreadcrumbLabels } from "@/components/layout/breadcrumbs";
import { ErrorState } from "@/components/feedback/error-state";
import { FadeIn } from "@/components/motion/motion";
import { TimelineView } from "@/components/timeline/timeline-view";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { ApiError } from "@/lib/api-client";
import { authStore } from "@/lib/auth-store";
import { TimelineService } from "@/services/timeline-service";
import type { HiringTimelineResponse } from "@/types/timeline";

export default function TimelinePage() {
  const router = useRouter();
  const { id, evaluationId } = useParams<{ id: string; evaluationId: string }>();
  const [timeline, setTimeline] = useState<HiringTimelineResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<{ message: string; correlationId: string | null } | null>(
    null,
  );

  const load = useCallback(() => {
    setLoading(true);
    setError(null);
    TimelineService.getTimeline(evaluationId)
      .then((res) => setTimeline(res.data))
      .catch((e: unknown) => {
        if (e instanceof ApiError && e.status === 401) {
          router.replace("/login");
          return;
        }
        setError({
          message: e instanceof Error ? e.message : "Failed to load the audit trail",
          correlationId: e instanceof ApiError ? e.body.correlation_id : null,
        });
      })
      .finally(() => setLoading(false));
  }, [evaluationId, router]);

  useEffect(() => {
    if (!authStore.getAccess()) {
      router.replace("/login");
      return;
    }
    load();
  }, [load, router]);

  useBreadcrumbLabels(
    timeline ? { [id]: timeline.role_title, [evaluationId]: timeline.candidate_name } : {},
  );

  const back = (
    <Link
      href={`/campaigns/${id}/candidates/${evaluationId}`}
      className="text-muted-foreground hover:text-foreground inline-flex items-center gap-1 text-sm transition-colors lg:hidden"
    >
      <ArrowLeft className="size-4" aria-hidden />
      Back to evaluation
    </Link>
  );

  if (loading) {
    return (
      <div className="space-y-6">
        {back}
        <Skeleton className="h-8 w-72" />
        <Skeleton className="h-64 w-full rounded-xl" />
      </div>
    );
  }

  if (error || !timeline) {
    return (
      <div className="space-y-6">
        {back}
        <ErrorState
          message={error?.message ?? "Could not load the audit trail"}
          correlationId={error?.correlationId}
          action={
            <Button variant="outline" size="sm" onClick={load}>
              Try again
            </Button>
          }
        />
      </div>
    );
  }

  return (
    <FadeIn className="space-y-6">
      {back}
      <div className="space-y-1">
        <h1 className="text-2xl font-semibold tracking-tight">History &amp; audit trail</h1>
        <p className="text-muted-foreground text-sm">
          {timeline.candidate_name} · {timeline.role_title} — exactly what happened, in order.
        </p>
      </div>
      <TimelineView timeline={timeline} />
    </FadeIn>
  );
}
