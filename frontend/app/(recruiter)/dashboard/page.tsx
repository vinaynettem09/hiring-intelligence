"use client";

import { ArrowRight, CheckCircle2, FilePlus2, Flag, Sparkles, UserPlus, Users } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";

import { ErrorState } from "@/components/feedback/error-state";
import { Stat } from "@/components/layout/stat";
import { FadeIn } from "@/components/motion/motion";
import { StatusBadge } from "@/components/status-badge";
import { Button, buttonVariants } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { ApiError } from "@/lib/api-client";
import { authStore } from "@/lib/auth-store";
import { cn } from "@/lib/utils";
import { DashboardService } from "@/services/dashboard-service";
import { ReviewService } from "@/services/review-service";
import type { DashboardResponse } from "@/types/dashboard";
import type { ReviewQueueSummary } from "@/types/review";

function greeting(): string {
  const hour = new Date().getHours();
  if (hour < 12) return "Good morning";
  if (hour < 18) return "Good afternoon";
  return "Good evening";
}

function contextMessage(d: DashboardResponse): string {
  const m = d.metrics;
  if (m.total_campaigns === 0) return "Let’s set up your first evaluation campaign.";
  if (m.active_campaigns === 0) {
    return `${m.draft_campaigns} draft ${m.draft_campaigns === 1 ? "campaign" : "campaigns"} ready to activate.`;
  }
  const campaigns = `${m.active_campaigns} active ${m.active_campaigns === 1 ? "campaign" : "campaigns"}`;
  const candidates = `${m.total_candidates} ${m.total_candidates === 1 ? "candidate" : "candidates"}`;
  return `${campaigns}, ${candidates} in your pipeline.`;
}

function primaryCta(d: DashboardResponse): { label: string; href: string } {
  const m = d.metrics;
  if (m.total_campaigns === 0) return { label: "Create campaign", href: "/campaigns/new" };
  if (m.active_campaigns === 0) return { label: "Review campaigns", href: "/campaigns" };
  const activeRecent = d.recent_campaigns.find((c) => c.status === "active");
  if (activeRecent && d.attention.active_campaigns_without_candidates > 0) {
    return { label: "Add candidates", href: `/campaigns/${activeRecent.id}/candidates` };
  }
  if (activeRecent) return { label: "Open campaign", href: `/campaigns/${activeRecent.id}` };
  return { label: "View campaigns", href: "/campaigns" };
}

export default function DashboardPage() {
  const router = useRouter();
  const [data, setData] = useState<DashboardResponse | null>(null);
  const [queue, setQueue] = useState<ReviewQueueSummary | null>(null);
  const [error, setError] = useState<{ message: string; correlationId: string | null } | null>(null);
  const [loading, setLoading] = useState(true);

  const load = useCallback(() => {
    setLoading(true);
    setError(null);
    DashboardService.get()
      .then((res) => setData(res.data))
      .catch((e: unknown) => {
        if (e instanceof ApiError && e.status === 401) {
          router.replace("/login");
          return;
        }
        setError({
          message: e instanceof Error ? e.message : "Failed to load your dashboard",
          correlationId: e instanceof ApiError ? e.body.correlation_id : null,
        });
      })
      .finally(() => setLoading(false));
    // Supplementary: queue-driven next actions. Best-effort — never breaks the dashboard.
    ReviewService.getQueue({ limit: 1 })
      .then((res) => setQueue(res.data.summary))
      .catch(() => undefined);
  }, [router]);

  useEffect(() => {
    if (!authStore.getAccess()) {
      router.replace("/login");
      return;
    }
    load();
  }, [load, router]);

  if (loading) {
    return (
      <div className="space-y-8">
        <Skeleton className="h-9 w-72" />
        <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
          {[0, 1, 2, 3].map((i) => (
            <Skeleton key={i} className="h-20 rounded-xl" />
          ))}
        </div>
        <Skeleton className="h-48 w-full rounded-xl" />
      </div>
    );
  }

  if (error || !data) {
    return (
      <ErrorState
        message={error?.message ?? "Could not load your dashboard"}
        correlationId={error?.correlationId}
        action={
          <Button variant="outline" size="sm" onClick={load}>
            Try again
          </Button>
        }
      />
    );
  }

  // Brand-new tenant: a welcoming, purposeful first-run state — not a wall of zeros.
  if (data.metrics.total_campaigns === 0) {
    return (
      <FadeIn className="mx-auto flex min-h-[70vh] max-w-xl flex-col items-center justify-center gap-6 text-center">
        <span className="bg-primary/10 text-primary flex size-14 items-center justify-center rounded-2xl">
          <Sparkles className="size-7" aria-hidden />
        </span>
        <div className="space-y-2">
          <h1 className="text-2xl font-semibold tracking-tight">{greeting()}</h1>
          <p className="text-muted-foreground">
            Hiring Intelligence evaluates candidates on evidence of how they work. A campaign is
            where you set that up — start with one.
          </p>
        </div>
        <ol className="text-muted-foreground grid w-full gap-2 text-left text-sm sm:grid-cols-2">
          {[
            "Define the role's competencies and hiring bar",
            "Design a structured work sample",
            "Invite candidates to submit real work",
            "Review evidence-cited AI assessments — you decide",
          ].map((step, i) => (
            <li key={i} className="bg-card/50 flex items-center gap-2 rounded-lg border px-3 py-2">
              <span className="bg-secondary text-primary flex size-5 shrink-0 items-center justify-center rounded-full text-xs font-semibold tabular-nums">
                {i + 1}
              </span>
              {step}
            </li>
          ))}
        </ol>
        <Link href="/campaigns/new" className={cn(buttonVariants({ size: "lg" }))}>
          Create your first campaign
          <ArrowRight className="size-4" aria-hidden />
        </Link>
      </FadeIn>
    );
  }

  const cta = primaryCta(data);
  const attention = buildAttention(data, queue);

  return (
    <FadeIn className="space-y-8">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div className="space-y-1">
          <h1 className="text-2xl font-semibold tracking-tight">{greeting()}</h1>
          <p className="text-muted-foreground">{contextMessage(data)}</p>
        </div>
        <Link href={cta.href} className={cn(buttonVariants(), "shrink-0")}>
          {cta.label}
          <ArrowRight className="size-4" aria-hidden />
        </Link>
      </div>

      <div className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        <Stat label="Campaigns" value={data.metrics.total_campaigns} />
        <Stat label="Active" value={data.metrics.active_campaigns} />
        <Stat label="Candidates" value={data.metrics.total_candidates} />
        <Stat label="Missing résumé" value={data.metrics.candidates_missing_resume} tone="attention" />
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Needs attention</CardTitle>
        </CardHeader>
        <CardContent>
          {attention.length === 0 ? (
            <p className="text-muted-foreground flex items-center gap-2 text-sm">
              <CheckCircle2 className="text-success size-4" aria-hidden />
              You’re all caught up.
            </p>
          ) : (
            <ul className="space-y-2">
              {attention.map((item) => (
                <li key={item.key} className="flex items-center justify-between gap-3 text-sm">
                  <span className="flex items-center gap-2">
                    <item.icon className="text-warning size-4 shrink-0" aria-hidden />
                    {item.text}
                  </span>
                  {item.href && (
                    <Link
                      href={item.href}
                      className="text-primary shrink-0 text-xs font-medium hover:underline"
                    >
                      {item.action}
                    </Link>
                  )}
                </li>
              ))}
            </ul>
          )}
        </CardContent>
      </Card>

      <div className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader className="flex-row items-center justify-between">
            <div>
              <CardTitle className="text-base">Recent campaigns</CardTitle>
              <CardDescription>Pick up where you left off.</CardDescription>
            </div>
            <Link
              href="/campaigns"
              className="text-muted-foreground hover:text-foreground text-xs font-medium"
            >
              View all
            </Link>
          </CardHeader>
          <CardContent className="space-y-1">
            {data.recent_campaigns.length === 0 ? (
              <p className="text-muted-foreground text-sm">No campaigns yet.</p>
            ) : (
              data.recent_campaigns.map((c) => (
                <Link
                  key={c.id}
                  href={`/campaigns/${c.id}`}
                  className="hover:bg-muted/50 -mx-2 flex items-center justify-between gap-3 rounded-md px-2 py-2"
                >
                  <span className="truncate text-sm font-medium">{c.role_title}</span>
                  <StatusBadge status={c.status} />
                </Link>
              ))
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="text-base">Recently added candidates</CardTitle>
            <CardDescription>The latest people in your pipeline.</CardDescription>
          </CardHeader>
          <CardContent className="space-y-1">
            {data.recent_candidates.length === 0 ? (
              <p className="text-muted-foreground text-sm">No candidates yet.</p>
            ) : (
              data.recent_candidates.map((c) => (
                <Link
                  key={c.evaluation_id}
                  href={`/campaigns/${c.campaign_id}/candidates`}
                  className="hover:bg-muted/50 -mx-2 flex items-center justify-between gap-3 rounded-md px-2 py-2"
                >
                  <span className="min-w-0">
                    <span className="block truncate text-sm font-medium">{c.name}</span>
                    <span className="text-muted-foreground block truncate text-xs">
                      {c.campaign_role_title}
                    </span>
                  </span>
                  <ArrowRight className="text-muted-foreground/50 size-4 shrink-0" aria-hidden />
                </Link>
              ))
            )}
          </CardContent>
        </Card>
      </div>
    </FadeIn>
  );
}

interface AttentionItem {
  key: string;
  icon: typeof UserPlus;
  text: string;
  action?: string;
  href?: string;
}

// Only conditions that actually exist (count > 0) become items. Queue-driven evaluation
// work leads — it's the most operationally urgent — then campaign-setup items follow.
function buildAttention(d: DashboardResponse, q: ReviewQueueSummary | null): AttentionItem[] {
  const items: AttentionItem[] = [];
  if (q && q.needs_review > 0) {
    items.push({
      key: "needs-review",
      icon: Flag,
      text: `${q.needs_review} ${q.needs_review === 1 ? "evaluation needs" : "evaluations need"} your review`,
      action: "Review",
      href: "/review-queue",
    });
  }
  if (q && q.ready_to_evaluate > 0) {
    items.push({
      key: "ready-eval",
      icon: Sparkles,
      text: `${q.ready_to_evaluate} ${q.ready_to_evaluate === 1 ? "submission is" : "submissions are"} ready to evaluate`,
      action: "Evaluate",
      href: "/review-queue",
    });
  }
  const a = d.attention;
  if (a.draft_campaigns > 0) {
    items.push({
      key: "drafts",
      icon: FilePlus2,
      text: `${a.draft_campaigns} draft ${a.draft_campaigns === 1 ? "campaign is" : "campaigns are"} waiting for activation`,
      action: "Review",
      href: "/campaigns",
    });
  }
  if (a.active_campaigns_without_candidates > 0) {
    items.push({
      key: "empty-active",
      icon: UserPlus,
      text: `${a.active_campaigns_without_candidates} active ${a.active_campaigns_without_candidates === 1 ? "campaign has" : "campaigns have"} no candidates yet`,
      action: "Open",
      href: "/campaigns",
    });
  }
  if (a.candidates_missing_resume > 0) {
    items.push({
      key: "missing-resume",
      icon: Users,
      text: `${a.candidates_missing_resume} ${a.candidates_missing_resume === 1 ? "candidate is" : "candidates are"} missing a résumé`,
    });
  }
  return items;
}
