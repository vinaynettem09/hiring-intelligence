"use client";

import { ArrowLeft, History, RefreshCw, Sparkles } from "lucide-react";
import Link from "next/link";
import { useParams, useRouter } from "next/navigation";
import { useCallback, useEffect, useState } from "react";
import { toast } from "sonner";

import { AIRecommendationCard } from "@/components/ai/ai-recommendation-card";
import { CompetencyReasoningCard } from "@/components/ai/competency-reasoning-card";
import { DecisionPanel } from "@/components/ai/decision-panel";
import { EscalatePanel } from "@/components/ai/escalate-panel";
import { EvaluationGeneratingState } from "@/components/ai/evaluation-generating-state";
import { EvaluationHistory } from "@/components/ai/evaluation-history";
import { EvaluationTechnicalDetails } from "@/components/ai/evaluation-technical-details";
import { EvidenceProvider } from "@/components/ai/evidence-context";
import { MockEvaluationNotice } from "@/components/ai/mock-evaluation-notice";
import { useBreadcrumbLabels } from "@/components/layout/breadcrumbs";
import { ReasoningSummary } from "@/components/ai/reasoning-summary";
import { EmptyState } from "@/components/feedback/empty-state";
import { ErrorState } from "@/components/feedback/error-state";
import { FadeIn } from "@/components/motion/motion";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Skeleton } from "@/components/ui/skeleton";
import { ApiError } from "@/lib/api-client";
import { authStore } from "@/lib/auth-store";
import { CandidateService } from "@/services/candidate-service";
import { DecisionService } from "@/services/decision-service";
import { EvaluationService } from "@/services/evaluation-service";
import type { DecisionHistoryResponse } from "@/types/decision";
import type { EvaluationHistoryResponse, SubmittedEvidenceItem } from "@/types/evaluation";

export default function EvaluationWorkspacePage() {
  const router = useRouter();
  const { id, evaluationId } = useParams<{ id: string; evaluationId: string }>();

  const [candidateName, setCandidateName] = useState<string | null>(null);
  const [submitted, setSubmitted] = useState<boolean | null>(null);
  const [history, setHistory] = useState<EvaluationHistoryResponse | null>(null);
  const [evidence, setEvidence] = useState<SubmittedEvidenceItem[]>([]);
  const [decisions, setDecisions] = useState<DecisionHistoryResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<{ message: string; correlationId: string | null } | null>(
    null,
  );
  const [generating, setGenerating] = useState(false);
  const [genError, setGenError] = useState<{ message: string; correlationId: string | null } | null>(
    null,
  );
  const [rerunning, setRerunning] = useState(false);
  const [confirmRerun, setConfirmRerun] = useState(false);

  const load = useCallback(() => {
    setLoading(true);
    setError(null);
    Promise.all([
      CandidateService.listRoster(id, { limit: 200 }),
      EvaluationService.getHistory(evaluationId),
      EvaluationService.getEvidence(evaluationId),
      DecisionService.getHistory(evaluationId),
    ])
      .then(([rosterRes, historyRes, evidenceRes, decisionsRes]) => {
        const entry = rosterRes.data.items.find((e) => e.evaluation_id === evaluationId);
        setCandidateName(entry?.candidate.name ?? null);
        setSubmitted(entry ? entry.status === "submitted" : null);
        setHistory(historyRes.data);
        setEvidence(evidenceRes.data.items);
        setDecisions(decisionsRes.data);
      })
      .catch((e: unknown) => {
        if (e instanceof ApiError && e.status === 401) {
          router.replace("/login");
          return;
        }
        setError({
          message: e instanceof Error ? e.message : "Failed to load the evaluation",
          correlationId: e instanceof ApiError ? e.body.correlation_id : null,
        });
      })
      .finally(() => setLoading(false));
  }, [id, evaluationId, router]);

  useEffect(() => {
    if (!authStore.getAccess()) {
      router.replace("/login");
      return;
    }
    load();
  }, [load, router]);

  const generate = useCallback(async () => {
    setGenerating(true);
    setGenError(null);
    try {
      await EvaluationService.generate(evaluationId);
      const refreshed = await EvaluationService.getHistory(evaluationId);
      setHistory(refreshed.data);
      // Evidence may now exist for citation resolution; refresh best-effort.
      EvaluationService.getEvidence(evaluationId)
        .then((r) => setEvidence(r.data.items))
        .catch(() => undefined);
    } catch (e: unknown) {
      if (e instanceof ApiError && e.status === 401) {
        router.replace("/login");
        return;
      }
      setGenError({
        message:
          e instanceof Error ? e.message : "The evaluation could not be generated. Please retry.",
        correlationId: e instanceof ApiError ? e.body.correlation_id : null,
      });
    } finally {
      setGenerating(false);
    }
  }, [evaluationId, router]);

  const rerun = useCallback(async () => {
    setConfirmRerun(false);
    setRerunning(true);
    try {
      await EvaluationService.rerun(evaluationId);
      const refreshed = await EvaluationService.getHistory(evaluationId);
      setHistory(refreshed.data);
      toast.success("New evaluation run created. Previous runs are unchanged.");
    } catch (e: unknown) {
      if (e instanceof ApiError && e.status === 401) {
        router.replace("/login");
        return;
      }
      toast.error(e instanceof Error ? e.message : "Could not create a new run");
    } finally {
      setRerunning(false);
    }
  }, [evaluationId, router]);

  const refreshDecisions = useCallback(() => {
    DecisionService.getHistory(evaluationId)
      .then((res) => setDecisions(res.data))
      .catch(() => undefined);
  }, [evaluationId]);

  // After a decision, confirm it AND make returning to operational work obvious — a
  // recruiter who came from the Review Queue shouldn't be stranded deep in a candidate route.
  const onDecisionRecorded = useCallback(() => {
    refreshDecisions();
    toast.success("Decision recorded.", {
      action: { label: "Review queue", onClick: () => router.push("/review-queue") },
    });
  }, [refreshDecisions, router]);

  useBreadcrumbLabels(candidateName ? { [evaluationId]: candidateName } : {});

  const back = (
    <Link
      href={`/campaigns/${id}/candidates`}
      className="text-muted-foreground hover:text-foreground inline-flex items-center gap-1 text-sm transition-colors lg:hidden"
    >
      <ArrowLeft className="size-4" aria-hidden />
      Back to candidates
    </Link>
  );

  if (loading) {
    return (
      <div className="space-y-6">
        {back}
        <Skeleton className="h-8 w-72" />
        <Skeleton className="h-44 w-full rounded-xl" />
        <div className="grid gap-4 md:grid-cols-2">
          <Skeleton className="h-40 rounded-xl" />
          <Skeleton className="h-40 rounded-xl" />
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="space-y-6">
        {back}
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

  const heading = candidateName ? `${candidateName} · evaluation` : "Candidate evaluation";
  const latest = history?.latest ?? null;

  // Candidate hasn't submitted — the AI must not run on an incomplete work sample.
  if (submitted === false) {
    return (
      <FadeIn className="space-y-6">
        {back}
        <PageTitle
          heading={heading}
          timelineHref={`/campaigns/${id}/candidates/${evaluationId}/timeline`}
        />
        <EmptyState
          icon={Sparkles}
          title="Awaiting submission"
          description="This candidate hasn't submitted their work sample yet. An evaluation can be generated once they do."
        />
      </FadeIn>
    );
  }

  return (
    <FadeIn className="space-y-6">
      {back}
      <PageTitle
        heading={heading}
        runNumber={latest?.run_number ?? null}
        timelineHref={`/campaigns/${id}/candidates/${evaluationId}/timeline`}
      />

      {/* generating takes over the content region with a designed processing state */}
      {generating && !latest ? (
        <EvaluationGeneratingState />
      ) : genError && !latest ? (
        <ErrorState
          title="The evaluation couldn't be generated"
          message={`${genError.message} No evaluation was saved — you can try again.`}
          correlationId={genError.correlationId}
          action={
            <Button size="sm" onClick={generate} loading={generating}>
              <RefreshCw className="size-4" aria-hidden />
              Try again
            </Button>
          }
        />
      ) : !latest ? (
        <GenerateEntry onGenerate={generate} generating={generating} />
      ) : (
        <EvidenceProvider items={evidence}>
          <div className="space-y-6">
            <MockEvaluationNotice provider={latest.provenance.provider} />
            <AIRecommendationCard detail={latest} />

            {latest.recommendation === "ESCALATE" && <EscalatePanel detail={latest} />}

            <section className="space-y-3">
              <h3 className="text-sm font-semibold">Why</h3>
              <ReasoningSummary strengths={latest.strengths} concerns={latest.concerns} />
            </section>

            {latest.competency_assessments.length > 0 && (
              <section className="space-y-3">
                <h3 className="text-sm font-semibold">Competency assessment</h3>
                <div className="grid gap-3 md:grid-cols-2">
                  {latest.competency_assessments.map((a) => (
                    <CompetencyReasoningCard key={a.competency} assessment={a} />
                  ))}
                </div>
              </section>
            )}

            {/* The culminating human act — AI proposal above is input; this is the decision. */}
            <DecisionPanel
              candidateEvaluationId={evaluationId}
              informingEvaluationId={latest.id}
              informingRunNumber={latest.run_number}
              history={decisions}
              onRecorded={onDecisionRecorded}
            />

            {history && (
              <EvaluationHistory runs={history.runs} latestRunNumber={latest.run_number} />
            )}

            <EvaluationTechnicalDetails detail={latest} />

            {/* Rerun is secondary + deliberate — behind a confirmation, never a magic button. */}
            <div className="flex justify-end border-t pt-4">
              <Dialog open={confirmRerun} onOpenChange={setConfirmRerun}>
                <DialogTrigger asChild>
                  <Button variant="ghost" size="sm" loading={rerunning}>
                    <RefreshCw className="size-4" aria-hidden />
                    Rerun evaluation
                  </Button>
                </DialogTrigger>
                <DialogContent>
                  <DialogHeader>
                    <DialogTitle>Rerun evaluation?</DialogTitle>
                    <DialogDescription>
                      This creates a new evaluation run using the current evaluation
                      configuration. Previous runs remain unchanged and stay in history.
                    </DialogDescription>
                  </DialogHeader>
                  <div className="flex justify-end gap-2">
                    <Button variant="outline" size="sm" onClick={() => setConfirmRerun(false)}>
                      Cancel
                    </Button>
                    <Button size="sm" onClick={rerun} loading={rerunning}>
                      Create new run
                    </Button>
                  </div>
                </DialogContent>
              </Dialog>
            </div>
          </div>
        </EvidenceProvider>
      )}
    </FadeIn>
  );
}

function PageTitle({
  heading,
  runNumber,
  timelineHref,
}: {
  heading: string;
  runNumber?: number | null;
  timelineHref?: string;
}) {
  return (
    <div className="flex flex-col gap-1">
      <div className="flex flex-wrap items-center gap-x-3 gap-y-1">
        <h1 className="text-2xl font-semibold tracking-tight">{heading}</h1>
        {runNumber != null && (
          <span className="text-muted-foreground text-sm tabular-nums">Run {runNumber} · latest</span>
        )}
        {timelineHref && (
          <Link
            href={timelineHref}
            className="text-muted-foreground hover:text-foreground inline-flex items-center gap-1 text-sm transition-colors"
          >
            <History className="size-3.5" aria-hidden />
            History &amp; audit trail
          </Link>
        )}
      </div>
      <p className="text-muted-foreground text-sm">
        Evidence-based assessment from the submitted work sample. AI proposes; your team decides.
      </p>
    </div>
  );
}

function GenerateEntry({
  onGenerate,
  generating,
}: {
  onGenerate: () => void;
  generating: boolean;
}) {
  return (
    <EmptyState
      icon={Sparkles}
      title="No evaluation yet"
      description="Generate an evidence-based assessment from this candidate's submitted work sample. You'll see the recommendation, how reliable the evidence is, and the reasoning behind it — all cited to the source."
      action={
        <Button onClick={onGenerate} loading={generating}>
          <Sparkles className="size-4" aria-hidden />
          Generate evaluation
        </Button>
      }
    />
  );
}
