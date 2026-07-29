"use client";

import { Check, AlertTriangle } from "lucide-react";

import { cn } from "@/lib/utils";
import type { ObservationView } from "@/types/evaluation";

import { EvidenceCitation } from "./evidence-citation";

// One grounded strength or concern. It ALWAYS renders its citations — a material claim
// about the candidate is never allowed to appear as uncited narrative (the backend
// guarantees grounding; the UI keeps the claim visibly tied to its source).
export function GroundedObservation({
  observation,
  kind,
}: {
  observation: ObservationView;
  kind: "strength" | "concern";
}) {
  const Icon = kind === "strength" ? Check : AlertTriangle;
  return (
    <li className="flex gap-3">
      <Icon
        className={cn(
          "mt-0.5 size-4 shrink-0",
          kind === "strength" ? "text-success" : "text-warning",
        )}
        aria-hidden
      />
      <div className="min-w-0 space-y-1.5">
        <p className="text-sm leading-relaxed">{observation.text}</p>
        {observation.citations.length > 0 && (
          <div className="flex flex-wrap gap-1.5">
            {observation.citations.map((c) => (
              <EvidenceCitation key={`${c.evidence_id}:${c.task_id}`} citation={c} />
            ))}
          </div>
        )}
      </div>
    </li>
  );
}
