"use client";

import { FileText } from "lucide-react";

import { cn } from "@/lib/utils";
import type { CitationView } from "@/types/evaluation";

import { useEvidence } from "./evidence-context";

// A compact, tappable chip that links a claim to its source evidence. The label is the
// human task position ("Task 2") — never the internal evidence UUID. Tapping opens the
// evidence sheet. Large enough to be a comfortable touch target on mobile.
export function EvidenceCitation({ citation }: { citation: CitationView }) {
  const { getByEvidenceId, open } = useEvidence();
  const item = getByEvidenceId(citation.evidence_id);
  const label = item ? `Task ${item.task_number}` : "Evidence";

  return (
    <button
      type="button"
      onClick={() => open(citation.evidence_id)}
      aria-label={`View source evidence: ${label}`}
      className={cn(
        "border-primary/20 bg-primary/5 text-primary hover:bg-primary/10",
        "focus-visible:ring-ring inline-flex items-center gap-1 rounded-md border px-2 py-1",
        "text-xs font-medium transition-colors focus-visible:outline-none focus-visible:ring-2",
      )}
    >
      <FileText className="size-3" aria-hidden />
      {label}
    </button>
  );
}
