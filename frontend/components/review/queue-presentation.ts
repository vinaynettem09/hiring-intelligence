// How queue STAGES render (recruiter-action language + tone + the one contextual action).
// Recommendation/confidence copy still comes from components/ai/presentation.ts — the queue
// never invents a second vocabulary for those.

import { CircleCheck, Clock, Flag, Mail, Scale, Sparkles, type LucideIcon } from "lucide-react";

import type { ReviewQueueItem } from "@/types/review";

export interface QueuePresentation {
  stageLabel: string;
  chip: string; // chip background + text
  icon: string; // icon color
  Icon: LucideIcon;
  actionLabel: string;
  hrefKind: "workspace" | "roster";
  quiet: boolean; // waiting/completed are visually subordinate to work that needs action
}

const QUIET: Pick<QueuePresentation, "chip" | "icon"> = {
  chip: "bg-secondary text-muted-foreground",
  icon: "text-muted-foreground",
};

export function queuePresentation(item: ReviewQueueItem): QueuePresentation {
  switch (item.stage) {
    case "NEEDS_REVIEW":
      return item.recommendation === "MIXED"
        ? {
            stageLabel: "Review mixed evidence",
            chip: "bg-warning/15 text-warning",
            icon: "text-warning",
            Icon: Scale,
            actionLabel: "Review evidence",
            hrefKind: "workspace",
            quiet: false,
          }
        : {
            stageLabel: "Human review needed",
            chip: "bg-primary/10 text-primary",
            icon: "text-primary",
            Icon: Flag,
            actionLabel: "Review evidence",
            hrefKind: "workspace",
            quiet: false,
          };
    case "READY_FOR_EVALUATION":
      return {
        // "Awaiting evaluation", not "Ready for evaluation" — the latter can read as
        // "candidate hasn't started". This means: work submitted, AI not yet run.
        stageLabel: "Awaiting evaluation",
        chip: "bg-primary/10 text-primary",
        icon: "text-primary",
        Icon: Sparkles,
        actionLabel: "Generate evaluation",
        hrefKind: "workspace",
        quiet: false,
      };
    case "AWAITING_INVITATION":
      return {
        stageLabel: "Not yet invited",
        chip: "bg-secondary text-secondary-foreground",
        icon: "text-muted-foreground",
        Icon: Mail,
        actionLabel: "View candidate",
        hrefKind: "roster",
        quiet: false,
      };
    case "AWAITING_CANDIDATE":
      return {
        stageLabel: "Waiting on candidate",
        ...QUIET,
        Icon: Clock,
        actionLabel: "View candidate",
        hrefKind: "roster",
        quiet: true,
      };
    case "EVALUATED":
    default:
      return {
        stageLabel: "Evaluated",
        ...QUIET,
        Icon: CircleCheck,
        actionLabel: "View evaluation",
        hrefKind: "workspace",
        quiet: true,
      };
  }
}

export function queueHref(item: ReviewQueueItem): string {
  return queuePresentation(item).hrefKind === "workspace"
    ? `/campaigns/${item.campaign_id}/candidates/${item.candidate_evaluation_id}`
    : `/campaigns/${item.campaign_id}/candidates`;
}

/** The last MEANINGFUL activity, phrased for the stage so recruiters prioritize naturally:
 * "Submitted 18 min ago" / "Evaluated yesterday" / "Invited 2 d ago" — not a bare "2h ago". */
export function activityLabel(item: ReviewQueueItem): string {
  const t = relativeTime(item.last_activity_at);
  switch (item.stage) {
    case "NEEDS_REVIEW":
    case "EVALUATED":
      return `Evaluated ${t}`;
    case "READY_FOR_EVALUATION":
      return `Submitted ${t}`;
    case "AWAITING_CANDIDATE":
      return `Invited ${t}`;
    case "AWAITING_INVITATION":
      return `Added ${t}`;
    default:
      return t;
  }
}

/** Small relative-time label for "last meaningful activity" (client-side, display only). */
export function relativeTime(iso: string): string {
  const secs = Math.round((Date.now() - new Date(iso).getTime()) / 1000);
  if (secs < 60) return "just now";
  const mins = Math.round(secs / 60);
  if (mins < 60) return `${mins} min ago`;
  const hrs = Math.round(mins / 60);
  if (hrs < 24) return `${hrs} h ago`;
  const days = Math.round(hrs / 24);
  if (days < 30) return `${days} d ago`;
  return new Date(iso).toLocaleDateString();
}
