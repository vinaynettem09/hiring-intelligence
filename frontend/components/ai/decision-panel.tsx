"use client";

import { Gavel, History } from "lucide-react";
import { useState } from "react";
import { toast } from "sonner";

import { decisionPresentation, DECISION_ORDER } from "@/components/decisions/decision-presentation";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { cn } from "@/lib/utils";
import { ApiError } from "@/lib/api-client";
import { DecisionService } from "@/services/decision-service";
import type { DecisionHistoryResponse, DecisionType } from "@/types/decision";

// The bridge from AI proposal to accountable HUMAN decision (the DecisionSummary contract).
// Deliberately NOT marked as AI — this is the person's act. The AI recommendation is input;
// the recorded decision is the human's, append-only, with the informing run referenced.
export function DecisionPanel({
  candidateEvaluationId,
  informingEvaluationId,
  informingRunNumber,
  history,
  onRecorded,
}: {
  candidateEvaluationId: string;
  informingEvaluationId: string | null;
  informingRunNumber: number | null;
  history: DecisionHistoryResponse | null;
  onRecorded: () => void;
}) {
  const [pending, setPending] = useState<DecisionType | null>(null);
  const [rationale, setRationale] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [showHistory, setShowHistory] = useState(false);

  const latest = history?.latest ?? null;

  async function record() {
    if (!pending) return;
    setSubmitting(true);
    try {
      await DecisionService.record(candidateEvaluationId, {
        decision: pending,
        rationale: rationale.trim() || null,
        evaluation_id: informingEvaluationId,
      });
      // Success feedback (incl. the return-to-work affordance) is owned by the page, which
      // has the router — so a decision made from the queue can offer a one-tap way back.
      setPending(null);
      setRationale("");
      onRecorded();
    } catch (e: unknown) {
      toast.error(e instanceof ApiError ? e.body.message : "Could not record the decision");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <Card className="p-6">
      <div className="mb-1 flex items-center gap-2">
        <Gavel className="text-foreground size-4" aria-hidden />
        <h3 className="text-base font-semibold tracking-tight">Your decision</h3>
      </div>
      <p className="text-muted-foreground mb-5 text-sm">
        The AI recommendation is input — this decision is yours, recorded as an accountable
        action. Previous decisions are kept.
      </p>

      {latest && (
        <div className="bg-muted/40 mb-5 rounded-lg border p-4">
          <div className="flex flex-wrap items-center gap-2">
            <span className="text-muted-foreground text-xs">Current decision:</span>
            <Badge variant={decisionPresentation(latest.decision).badge} className="normal-case">
              {decisionPresentation(latest.decision).label}
            </Badge>
          </div>
          <p className="text-muted-foreground mt-1.5 text-xs">
            by {latest.decided_by_email} · {new Date(latest.decided_at).toLocaleString()}
            {latest.informed_by_run_number != null && ` · informed by run ${latest.informed_by_run_number}`}
          </p>
          {latest.rationale && <p className="mt-2 text-sm">{latest.rationale}</p>}
        </div>
      )}

      <fieldset disabled={submitting}>
        <legend className="text-sm font-medium">
          {latest ? "Change decision" : "Record a decision"}
        </legend>
        {informingRunNumber != null && (
          <p className="text-muted-foreground mt-1 text-xs">
            This decision will reference evaluation run {informingRunNumber}.
          </p>
        )}
        <div className="mt-2 flex flex-wrap gap-2">
          {DECISION_ORDER.map((d) => {
            const dp = decisionPresentation(d);
            const active = pending === d;
            return (
              <button
                key={d}
                type="button"
                aria-pressed={active}
                onClick={() => setPending(active ? null : d)}
                className={cn(
                  "focus-visible:ring-ring inline-flex items-center gap-1.5 rounded-lg border px-3 py-2 text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2",
                  active
                    ? "border-primary bg-primary/10 text-primary"
                    : "hover:bg-muted text-foreground",
                )}
              >
                <dp.Icon className="size-4" aria-hidden />
                {dp.verb}
              </button>
            );
          })}
        </div>

        {pending && (
          <div className="mt-4 space-y-2">
            <Label htmlFor="decision-rationale">Rationale (optional)</Label>
            <Textarea
              id="decision-rationale"
              value={rationale}
              onChange={(e) => setRationale(e.target.value)}
              placeholder="Why are you making this decision? (optional, for the record)"
              rows={3}
            />
            <div className="flex gap-2">
              <Button size="sm" onClick={record} loading={submitting}>
                Record {decisionPresentation(pending).verb.toLowerCase()}
              </Button>
              <Button variant="ghost" size="sm" onClick={() => setPending(null)}>
                Cancel
              </Button>
            </div>
          </div>
        )}
      </fieldset>

      {history && history.decisions.length > 1 && (
        <div className="mt-5 border-t pt-4">
          <button
            type="button"
            onClick={() => setShowHistory((v) => !v)}
            aria-expanded={showHistory}
            className="text-muted-foreground hover:text-foreground inline-flex items-center gap-1.5 text-xs font-medium"
          >
            <History className="size-3.5" aria-hidden />
            {showHistory ? "Hide" : "Show"} decision history ({history.decisions.length})
          </button>
          {showHistory && (
            <ul className="mt-3 space-y-2">
              {history.decisions.map((d) => (
                <li key={d.id} className="flex flex-wrap items-center gap-x-2 gap-y-1 text-sm">
                  <Badge variant={decisionPresentation(d.decision).badge} className="normal-case">
                    {decisionPresentation(d.decision).label}
                  </Badge>
                  <span className="text-muted-foreground text-xs">
                    {d.decided_by_email} · {new Date(d.decided_at).toLocaleString()}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </Card>
  );
}
