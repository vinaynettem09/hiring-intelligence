"use client";

import { ChevronDown } from "lucide-react";
import { useState } from "react";

import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import type { CompetencyAssessmentView } from "@/types/evaluation";

import { EvidenceCitation } from "./evidence-citation";

// One competency's grounded assessment. Qualitative only — NO numeric score, NO progress
// bar pretending a judgement is a measurement. The recruiter scans the assessment, then
// expands to inspect the exact evidence it rests on.
export function CompetencyReasoningCard({
  assessment,
}: {
  assessment: CompetencyAssessmentView;
}) {
  const [open, setOpen] = useState(false);
  const count = assessment.citations.length;

  return (
    <Card className="p-5">
      <h3 className="text-sm font-semibold">{assessment.competency}</h3>
      <p className="text-muted-foreground mt-2 text-sm leading-relaxed">{assessment.assessment}</p>

      {count > 0 && (
        <div className="mt-3">
          <button
            type="button"
            onClick={() => setOpen((v) => !v)}
            aria-expanded={open}
            className="text-muted-foreground hover:text-foreground focus-visible:ring-ring inline-flex items-center gap-1 rounded text-xs font-medium transition-colors focus-visible:outline-none focus-visible:ring-2"
          >
            <ChevronDown
              className={cn("size-3.5 transition-transform", open && "rotate-180")}
              aria-hidden
            />
            {count} supporting {count === 1 ? "citation" : "citations"}
          </button>
          {open && (
            <div className="mt-2 flex flex-wrap gap-1.5">
              {assessment.citations.map((c) => (
                <EvidenceCitation key={`${c.evidence_id}:${c.task_id}`} citation={c} />
              ))}
            </div>
          )}
        </div>
      )}
    </Card>
  );
}
