"use client";

import { ShieldCheck, TriangleAlert } from "lucide-react";
import type { LucideIcon } from "lucide-react";

import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import type { ObservationView } from "@/types/evaluation";

import { GroundedObservation } from "./grounded-observation";

// The executive "why": supporting evidence vs. evidence that needs attention. Both groups
// are grounded (every line links to source). Empty states are designed intentionally —
// we never manufacture balance by inventing a strength or a concern that wasn't found.
export function ReasoningSummary({
  strengths,
  concerns,
}: {
  strengths: ObservationView[];
  concerns: ObservationView[];
}) {
  return (
    <div className="grid gap-4 md:grid-cols-2">
      <Group
        title="Supporting evidence"
        Icon={ShieldCheck}
        iconClass="text-success"
        observations={strengths}
        kind="strength"
        emptyLabel="No clear strengths were surfaced in the submitted evidence."
      />
      <Group
        title="Needs attention"
        Icon={TriangleAlert}
        iconClass="text-warning"
        observations={concerns}
        kind="concern"
        emptyLabel="No specific concerns were surfaced in the submitted evidence."
      />
    </div>
  );
}

function Group({
  title,
  Icon,
  iconClass,
  observations,
  kind,
  emptyLabel,
}: {
  title: string;
  Icon: LucideIcon;
  iconClass: string;
  observations: ObservationView[];
  kind: "strength" | "concern";
  emptyLabel: string;
}) {
  return (
    <Card className="p-5">
      <div className="mb-4 flex items-center gap-2">
        <Icon className={cn("size-4", iconClass)} aria-hidden />
        <h3 className="text-sm font-semibold">{title}</h3>
        <span className="text-muted-foreground text-xs tabular-nums">{observations.length}</span>
      </div>
      {observations.length > 0 ? (
        <ul className="space-y-4">
          {observations.map((o, i) => (
            <GroundedObservation key={i} observation={o} kind={kind} />
          ))}
        </ul>
      ) : (
        <p className="text-muted-foreground text-sm">{emptyLabel}</p>
      )}
    </Card>
  );
}
