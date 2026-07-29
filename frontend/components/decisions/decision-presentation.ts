// How human decisions render. Deliberately non-punitive: "Declined" is a considered human
// judgement, never framed as failure or "the AI rejected the candidate".

import { ArrowRight, CircleSlash, PauseCircle, type LucideIcon } from "lucide-react";

import type { BadgeProps } from "@/components/ui/badge";
import type { DecisionType } from "@/types/decision";

export interface DecisionPresentation {
  verb: string; // the action button ("Advance")
  label: string; // the recorded state ("Advanced")
  badge: BadgeProps["variant"];
  Icon: LucideIcon;
}

const MAP: Record<DecisionType, DecisionPresentation> = {
  ADVANCE: { verb: "Advance", label: "Advanced", badge: "success", Icon: ArrowRight },
  HOLD: { verb: "Hold", label: "On hold", badge: "warning", Icon: PauseCircle },
  DECLINE: { verb: "Decline", label: "Declined", badge: "neutral", Icon: CircleSlash },
};

export function decisionPresentation(d: DecisionType): DecisionPresentation {
  return MAP[d];
}

export const DECISION_ORDER: DecisionType[] = ["ADVANCE", "HOLD", "DECLINE"];
