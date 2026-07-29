"use client";

import { ArrowLeft, Lock, Plus, Upload, Users } from "lucide-react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useCallback, useEffect, useRef, useState } from "react";
import { toast } from "sonner";

import { useBreadcrumbLabels } from "@/components/layout/breadcrumbs";
import { AddCandidateDialog } from "@/components/candidate/add-candidate-dialog";
import { ImportResultsPanel } from "@/components/candidate/import-results-panel";
import { RosterTable } from "@/components/candidate/roster-table";
import { EmptyState } from "@/components/feedback/empty-state";
import { ErrorState } from "@/components/feedback/error-state";
import { Stat } from "@/components/layout/stat";
import { FadeIn } from "@/components/motion/motion";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { ApiError } from "@/lib/api-client";
import { authStore } from "@/lib/auth-store";
import { CampaignService } from "@/services/campaign-service";
import { CandidateService } from "@/services/candidate-service";
import { InvitationService } from "@/services/invitation-service";
import type { Campaign } from "@/types/campaign";
import type { CandidateImportSummary, RosterResponse } from "@/types/candidate";

export default function RosterPage() {
  const router = useRouter();
  const { id } = useParams<{ id: string }>();

  const [campaign, setCampaign] = useState<Campaign | null>(null);
  const [roster, setRoster] = useState<RosterResponse | null>(null);
  const [error, setError] = useState<{ message: string; correlationId: string | null } | null>(null);
  const [loading, setLoading] = useState(true);
  const [importSummary, setImportSummary] = useState<CandidateImportSummary | null>(null);
  const [importing, setImporting] = useState(false);
  const [invitingId, setInvitingId] = useState<string | null>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  const load = useCallback(() => {
    setLoading(true);
    setError(null);
    Promise.all([CampaignService.get(id), CandidateService.listRoster(id, { limit: 50 })])
      .then(([campaignRes, rosterRes]) => {
        setCampaign(campaignRes.data);
        setRoster(rosterRes.data);
      })
      .catch((e: unknown) => {
        if (e instanceof ApiError && e.status === 401) {
          router.replace("/login");
          return;
        }
        setError({
          message: e instanceof Error ? e.message : "Failed to load candidates",
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

  const refreshRoster = useCallback(() => {
    CandidateService.listRoster(id, { limit: 50 })
      .then((res) => setRoster(res.data))
      .catch(() => undefined);
  }, [id]);

  async function onFileSelected(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setImporting(true);
    setImportSummary(null);
    try {
      const res = await CandidateService.importCsv(id, file);
      setImportSummary(res.data);
      refreshRoster();
    } catch (err: unknown) {
      if (err instanceof ApiError && err.status === 401) {
        router.replace("/login");
        return;
      }
      toast.error(err instanceof Error ? err.message : "Import failed");
    } finally {
      setImporting(false);
      if (fileRef.current) fileRef.current.value = "";
    }
  }

  function onGenerate(evaluationId: string) {
    // Navigate into the intelligence workspace, where a designed generate flow +
    // processing state live (generation is deliberate, never auto-run on navigation).
    router.push(`/campaigns/${id}/candidates/${evaluationId}`);
  }

  async function onInvite(evaluationId: string) {
    setInvitingId(evaluationId);
    try {
      await InvitationService.issue(evaluationId);
      toast.success("Invitation sent");
    } catch (err: unknown) {
      if (err instanceof ApiError && err.status === 401) {
        router.replace("/login");
        return;
      }
      toast.error(err instanceof Error ? err.message : "Could not send invitation");
    } finally {
      setInvitingId(null);
    }
  }

  const back = (
    <Link
      href={`/campaigns/${id}`}
      className="text-muted-foreground hover:text-foreground inline-flex items-center gap-1 text-sm transition-colors lg:hidden"
    >
      <ArrowLeft className="size-4" aria-hidden />
      Back to campaign
    </Link>
  );

  if (loading) {
    return (
      <div className="space-y-6">
        {back}
        <Skeleton className="h-8 w-64" />
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
          <Skeleton className="h-20 rounded-xl" />
          <Skeleton className="h-20 rounded-xl" />
        </div>
        <Skeleton className="h-64 w-full rounded-xl" />
      </div>
    );
  }

  if (error || !campaign || !roster) {
    return (
      <div className="space-y-6">
        {back}
        <ErrorState
          message={error?.message ?? "Could not load candidates"}
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

  const isActive = campaign.status === "active";
  const isDraft = campaign.status === "draft";

  const importButton = (
    <Button variant="outline" onClick={() => fileRef.current?.click()} loading={importing}>
      <Upload className="size-4" aria-hidden />
      Import CSV
    </Button>
  );
  const addButton = (
    <AddCandidateDialog
      campaignId={id}
      onAdded={refreshRoster}
      trigger={
        <Button>
          <Plus className="size-4" aria-hidden />
          Add candidate
        </Button>
      }
    />
  );

  const hasCandidates = roster.items.length > 0;

  return (
    <FadeIn className="space-y-6">
      {back}

      <input
        ref={fileRef}
        type="file"
        accept=".csv,text/csv"
        hidden
        onChange={onFileSelected}
      />

      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div className="space-y-1">
          <h1 className="text-2xl font-semibold tracking-tight">{campaign.role_title}</h1>
          <p className="text-muted-foreground text-sm">Candidates in this campaign.</p>
        </div>
        {isActive && hasCandidates && (
          <div className="flex items-center gap-2">
            {importButton}
            {addButton}
          </div>
        )}
      </div>

      {/* What's here · what needs attention */}
      <div className="grid grid-cols-2 gap-3 sm:grid-cols-4">
        <Stat label="Candidates" value={roster.total} />
        <Stat label="Missing résumé" value={roster.missing_resume} tone="attention" />
      </div>

      {importSummary && (
        <ImportResultsPanel summary={importSummary} onDismiss={() => setImportSummary(null)} />
      )}

      {!hasCandidates && isActive && (
        <EmptyState
          icon={Users}
          title="No candidates yet"
          description="This campaign is active and ready to receive candidates. Import a CSV or add one manually."
          action={
            <div className="flex flex-wrap items-center justify-center gap-2">
              {importButton}
              {addButton}
            </div>
          }
        />
      )}

      {!hasCandidates && isDraft && (
        <EmptyState
          icon={Lock}
          title="Not accepting candidates yet"
          description="Activate this campaign to start inviting candidates."
          action={
            <Link href={`/campaigns/${id}`}>
              <Button variant="outline">Go to campaign</Button>
            </Link>
          }
        />
      )}

      {!hasCandidates && !isActive && !isDraft && (
        <EmptyState icon={Users} title="No candidates" description="This campaign has no candidates." />
      )}

      {hasCandidates && (
        <div className="space-y-3">
          <RosterTable
            data={roster.items}
            campaignId={id}
            onInvite={isActive ? onInvite : undefined}
            invitingId={invitingId}
            onGenerate={onGenerate}
          />
          <p className="text-muted-foreground text-xs">
            Showing {roster.items.length} of {roster.total}.
          </p>
        </div>
      )}
    </FadeIn>
  );
}
