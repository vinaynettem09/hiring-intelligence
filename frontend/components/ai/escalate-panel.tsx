"use client";

import { Flag, HelpCircle } from "lucide-react";

import { Card } from "@/components/ui/card";
import type { EvaluationDetail } from "@/types/evaluation";

import { escalationReasonCopy } from "./presentation";

// ESCALATE has its own designed state — it is NOT a failure. It says "a human should look,"
// explains why, and makes the gaps explicit so the recruiter understands what the system
// does NOT know. Uncertainty is a product feature here.
export function EscalatePanel({ detail }: { detail: EvaluationDetail }) {
  const reason = escalationReasonCopy(detail.escalation_reason);
  const cov = detail.evidence_coverage;

  const gaps: string[] = [];
  if (cov.competencies_assessed < cov.competencies_total) {
    gaps.push(
      `${cov.competencies_total - cov.competencies_assessed} of ${cov.competencies_total} competencies could not be grounded in evidence.`,
    );
  }
  if (cov.tasks_with_evidence < cov.tasks_total) {
    gaps.push(
      `${cov.tasks_total - cov.tasks_with_evidence} of ${cov.tasks_total} work-sample tasks have no submitted evidence.`,
    );
  }

  return (
    <Card className="border-primary/30 bg-primary/5 p-6">
      <div className="flex items-start gap-4">
        <span className="bg-primary/10 text-primary flex size-10 shrink-0 items-center justify-center rounded-xl">
          <Flag className="size-5" aria-hidden />
        </span>
        <div className="space-y-3">
          <div className="space-y-1">
            <h2 className="text-lg font-semibold tracking-tight">More human review is needed</h2>
            <p className="text-muted-foreground text-sm leading-relaxed">
              {reason ??
                "The system does not have enough reliable evidence to responsibly propose a direction."}
            </p>
          </div>

          {gaps.length > 0 && (
            <div className="space-y-2">
              <p className="text-foreground flex items-center gap-1.5 text-xs font-medium">
                <HelpCircle className="text-muted-foreground size-3.5" aria-hidden />
                What the system could not determine
              </p>
              <ul className="text-muted-foreground space-y-1 text-sm">
                {gaps.map((g, i) => (
                  <li key={i} className="flex gap-2">
                    <span aria-hidden className="text-muted-foreground/50">
                      &bull;
                    </span>
                    {g}
                  </li>
                ))}
              </ul>
            </div>
          )}

          <p className="text-muted-foreground text-xs">
            This is not a judgement that the candidate is weak — it means the evidence is
            insufficient to assess responsibly. A person should review directly.
          </p>
        </div>
      </div>
    </Card>
  );
}
