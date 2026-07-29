// Single source of truth for how AI evaluation vocabulary is rendered to recruiters.
// Enum values NEVER reach the screen raw; they map to humane, product-appropriate copy.
// Meaning is never conveyed by color alone — every mapping pairs a tone with an icon + text.

import { Check, CircleCheck, CircleSlash, Flag, Scale, type LucideIcon } from "lucide-react";

import type { EscalationReason, Recommendation } from "@/types/evaluation";

/** Semantic tone — deliberately NOT reused between recommendation and confidence, so a
 * confident negative call never borrows "good" colors and low confidence never looks like
 * an error. */
export type Tone = "positive" | "moderate" | "negative" | "review";

export interface ToneClasses {
  chip: string; // small pill / badge
  icon: string; // icon color
  accent: string; // left border / ring accent
  soft: string; // faint fill for larger surfaces
}

export const TONE_CLASSES: Record<Tone, ToneClasses> = {
  positive: {
    chip: "bg-success/10 text-success",
    icon: "text-success",
    accent: "border-success/40",
    soft: "bg-success/5",
  },
  moderate: {
    chip: "bg-warning/15 text-warning",
    icon: "text-warning",
    accent: "border-warning/40",
    soft: "bg-warning/5",
  },
  negative: {
    chip: "bg-destructive/10 text-destructive",
    icon: "text-destructive",
    accent: "border-destructive/40",
    soft: "bg-destructive/5",
  },
  review: {
    chip: "bg-primary/10 text-primary",
    icon: "text-primary",
    accent: "border-primary/40",
    soft: "bg-primary/5",
  },
};

export interface RecommendationPresentation {
  label: string; // the headline, in recruiter language
  detail: string; // one plain-language sentence
  tone: Tone;
  Icon: LucideIcon;
}

const RECOMMENDATIONS: Record<Recommendation, RecommendationPresentation> = {
  STRONG_PROCEED: {
    label: "Strong evidence to proceed",
    detail: "The submitted work-sample evidence clearly and consistently supports moving forward.",
    tone: "positive",
    Icon: CircleCheck,
  },
  PROCEED: {
    label: "Evidence supports proceeding",
    detail: "The evidence meets the role's bar on the assessed competencies.",
    tone: "positive",
    Icon: Check,
  },
  MIXED: {
    label: "Mixed evidence",
    detail: "The evidence points in more than one direction — it supports neither a clear yes nor a clear no.",
    tone: "moderate",
    Icon: Scale,
  },
  DO_NOT_PROCEED: {
    label: "Evidence does not support proceeding",
    detail: "Taken together, the evidence indicates the candidate is below the bar on the assessed competencies.",
    tone: "negative",
    Icon: CircleSlash,
  },
  ESCALATE: {
    label: "Human review needed",
    detail: "There isn't enough reliable evidence for the system to responsibly propose a direction.",
    tone: "review",
    Icon: Flag,
  },
};

export function recommendationPresentation(rec: Recommendation): RecommendationPresentation {
  return RECOMMENDATIONS[rec];
}

/** Terse label for compact rows (history, roster). Still humane, never the raw enum. */
const SHORT_LABELS: Record<Recommendation, string> = {
  STRONG_PROCEED: "Strong proceed",
  PROCEED: "Proceed",
  MIXED: "Mixed",
  DO_NOT_PROCEED: "Do not proceed",
  ESCALATE: "Human review",
};

export function recommendationShortLabel(rec: Recommendation): string {
  return SHORT_LABELS[rec];
}

// --- confidence (evidence reliability, NOT a probability) --- //

export type ConfidenceLevel = "high" | "moderate" | "low";

export function confidenceLevel(value: number): ConfidenceLevel {
  if (value >= 0.7) return "high";
  if (value >= 0.4) return "moderate";
  return "low";
}

export interface ConfidencePresentation {
  label: string;
  // A calm scale: high reads as solid, low reads as "a human should look" — never as error.
  barClass: string;
  textClass: string;
  fill: number; // 0..1 for the meter width (the raw value; shown as a bar, never as "%")
}

export function confidencePresentation(value: number): ConfidencePresentation {
  const level = confidenceLevel(value);
  const label =
    level === "high"
      ? "High evidence confidence"
      : level === "moderate"
        ? "Moderate evidence confidence"
        : "Low evidence confidence";
  const barClass =
    level === "high" ? "bg-primary" : level === "moderate" ? "bg-warning" : "bg-muted-foreground/50";
  const textClass =
    level === "high" ? "text-foreground" : level === "moderate" ? "text-warning" : "text-muted-foreground";
  return { label, barClass, textClass, fill: value };
}

export const CONFIDENCE_EXPLANATION =
  "Evidence confidence reflects how complete and internally consistent the available evidence " +
  "is. It is not a probability that the candidate will succeed, and it is independent of the " +
  "direction of the recommendation.";

export function escalationReasonCopy(reason: EscalationReason | null): string | null {
  if (reason === "INSUFFICIENT_EVIDENCE")
    return "There isn't enough job-relevant evidence to assess this candidate responsibly.";
  if (reason === "LOW_CONFIDENCE")
    return "The available evidence isn't complete or consistent enough to support a confident recommendation.";
  return null;
}
