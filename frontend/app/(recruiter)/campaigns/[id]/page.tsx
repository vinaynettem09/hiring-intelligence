"use client";

import { ArrowLeft, ClipboardList, Lock, Users } from "lucide-react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import { toast } from "sonner";

import { useBreadcrumbLabels } from "@/components/layout/breadcrumbs";
import { ErrorState } from "@/components/feedback/error-state";
import { FadeIn } from "@/components/motion/motion";
import { StatusBadge } from "@/components/status-badge";
import { Button, buttonVariants } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import { ApiError } from "@/lib/api-client";
import { authStore } from "@/lib/auth-store";
import { cn } from "@/lib/utils";
import { CampaignService } from "@/services/campaign-service";
import { WorkSampleService } from "@/services/work-sample-service";
import type { Campaign } from "@/types/campaign";

export default function CampaignDetailPage() {
  const router = useRouter();
  const { id } = useParams<{ id: string }>();

  const [campaign, setCampaign] = useState<Campaign | null>(null);
  const [error, setError] = useState<{ message: string; correlationId: string | null } | null>(null);
  const [loading, setLoading] = useState(true);
  const [activating, setActivating] = useState(false);
  // Whether the work sample is complete (every competency covered). Drives the draft →
  // work-sample → activate sequencing. Best-effort UX only — the backend remains the
  // authority on whether activation is actually allowed.
  const [workSampleReady, setWorkSampleReady] = useState<boolean | null>(null);

  const load = useCallback(() => {
    setLoading(true);
    setError(null);
    WorkSampleService.get(id)
      .then((r) => setWorkSampleReady(r.data.exists && r.data.coverage.uncovered.length === 0))
      .catch(() => setWorkSampleReady(false));
    CampaignService.get(id)
      .then((res) => setCampaign(res.data))
      .catch((e: unknown) => {
        if (e instanceof ApiError && e.status === 401) {
          router.replace("/login");
          return;
        }
        setError({
          message: e instanceof Error ? e.message : "Failed to load campaign",
          correlationId: e instanceof ApiError ? e.body.correlation_id : null,
        });
      })
      .finally(() => setLoading(false));
  }, [id, router]);

  useEffect(() => {
    if (!authStore.getAccess()) {
      router.replace("/login");
      return;
    }
    load();
  }, [load, router]);

  useBreadcrumbLabels(campaign ? { [id]: campaign.role_title } : {});

  async function onActivate() {
    setActivating(true);
    try {
      const res = await CampaignService.activate(id);
      setCampaign(res.data); // reflect the state the backend returned
      toast.success("Campaign activated", { description: "Its configuration is now frozen." });
    } catch (err: unknown) {
      if (err instanceof ApiError && err.status === 401) {
        router.replace("/login");
        return;
      }
      // The backend decides whether activation is allowed — show its verdict.
      toast.error(err instanceof Error ? err.message : "Activation failed");
    } finally {
      setActivating(false);
    }
  }

  const back = (
    <Link
      href="/campaigns"
      className="text-muted-foreground hover:text-foreground inline-flex items-center gap-1 text-sm transition-colors lg:hidden"
    >
      <ArrowLeft className="size-4" aria-hidden />
      Campaigns
    </Link>
  );

  if (loading) {
    return (
      <div className="space-y-6">
        {back}
        <Skeleton className="h-8 w-64" />
        <Skeleton className="h-48 w-full rounded-xl" />
      </div>
    );
  }

  if (error || !campaign) {
    return (
      <div className="space-y-6">
        {back}
        <ErrorState
          message={error?.message ?? "Campaign not found"}
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

      <div className="flex items-start justify-between gap-4">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">{campaign.role_title}</h1>
          <p className="text-muted-foreground text-sm">
            Created {new Date(campaign.created_at).toLocaleDateString()}
          </p>
        </div>
        <StatusBadge status={campaign.status} />
      </div>

      <Card>
        <CardHeader>
          <CardTitle className="text-base">Evaluation profile</CardTitle>
          <CardDescription>Competencies and the bar candidates are measured against.</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <ul className="space-y-2">
            {campaign.role_profile.competencies.map((c, i) => (
              <li key={i} className="flex gap-2 text-sm">
                <span className="text-primary" aria-hidden>
                  •
                </span>
                <span>
                  <span className="font-medium">{c.name}</span>
                  {c.description && <span className="text-muted-foreground"> — {c.description}</span>}
                </span>
              </li>
            ))}
          </ul>
          <div className="border-t pt-4">
            <p className="text-sm font-medium">Hiring bar</p>
            <p className="text-muted-foreground mt-1 text-sm whitespace-pre-wrap">
              {campaign.role_profile.bar}
            </p>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardContent className="flex flex-col gap-4 pt-6 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-3">
            <ClipboardList className="text-muted-foreground size-5 shrink-0" aria-hidden />
            <div>
              <p className="text-sm font-medium">Work sample</p>
              <p className="text-muted-foreground text-sm">
                {campaign.status !== "draft"
                  ? "The evidence instrument for this campaign (frozen)."
                  : workSampleReady
                    ? "Ready — every competency has at least one task."
                    : "Design the structured tasks candidates will complete."}
              </p>
            </div>
          </div>
          <Link
            href={`/campaigns/${campaign.id}/work-sample`}
            className={cn(
              buttonVariants({
                variant: campaign.status === "draft" && !workSampleReady ? "primary" : "outline",
              }),
              "shrink-0",
            )}
          >
            {campaign.status !== "draft"
              ? "View work sample"
              : workSampleReady
                ? "Edit work sample"
                : "Design work sample"}
          </Link>
        </CardContent>
      </Card>

      {campaign.status === "draft" && (
        <Card className="border-primary/30 bg-primary/5">
          <CardContent className="flex flex-col gap-4 pt-6 sm:flex-row sm:items-center sm:justify-between">
            <div className="flex gap-3">
              <Lock className="text-primary mt-0.5 size-5 shrink-0" aria-hidden />
              <div>
                <p className="text-sm font-medium">
                  {workSampleReady ? "Ready to activate" : "Next: complete the work sample"}
                </p>
                <p className="text-muted-foreground text-sm">
                  {workSampleReady
                    ? "Activating freezes the role criteria and work sample as the fixed basis for every candidate's evaluation — it can't be changed or undone. Create a new campaign to change the criteria."
                    : "Every competency needs at least one work-sample task before you can activate. Once it's complete, activating freezes the configuration for consistent evaluation."}
                </p>
              </div>
            </div>
            <Button
              onClick={onActivate}
              loading={activating}
              disabled={!workSampleReady}
              className="shrink-0"
            >
              Activate campaign
            </Button>
          </CardContent>
        </Card>
      )}

      <Card>
        <CardContent className="flex flex-col gap-4 pt-6 sm:flex-row sm:items-center sm:justify-between">
          <div className="flex items-center gap-3">
            <Users className="text-muted-foreground size-5 shrink-0" aria-hidden />
            <div>
              <p className="text-sm font-medium">Candidates</p>
              <p className="text-muted-foreground text-sm">
                {campaign.status === "active"
                  ? "Invite and review candidates for this campaign."
                  : "Candidates can be added once the campaign is active."}
              </p>
            </div>
          </div>
          <Link
            href={`/campaigns/${campaign.id}/candidates`}
            className={cn(
              buttonVariants({ variant: campaign.status === "active" ? "primary" : "outline" }),
              "shrink-0",
            )}
          >
            {campaign.status === "active" ? "Manage candidates" : "View roster"}
          </Link>
        </CardContent>
      </Card>
    </FadeIn>
  );
}
