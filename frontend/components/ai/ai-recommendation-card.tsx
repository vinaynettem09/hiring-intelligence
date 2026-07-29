"use client";

import { Sparkles } from "lucide-react";

import { Card } from "@/components/ui/card";
import { cn } from "@/lib/utils";
import type { EvaluationDetail } from "@/types/evaluation";

import { ConfidenceMeter } from "./confidence-meter";
import { TONE_CLASSES, recommendationPresentation } from "./presentation";

// The headline AI output. Prominent but deliberately NOT a verdict stamp: it reads as an
// advisory proposal (marked as AI), pairs the recommendation with its evidence-confidence,
// and states the human-decides boundary in quiet copy. No score, no percentage.
export function AIRecommendationCard({ detail }: { detail: EvaluationDetail }) {
  const { label, detail: sentence, tone, Icon } = recommendationPresentation(detail.recommendation);
  const t = TONE_CLASSES[tone];

  return (
    <Card className={cn("overflow-hidden border-l-4", t.accent)}>
      <div className={cn("p-6", t.soft)}>
        <div className="text-muted-foreground mb-4 flex items-center gap-1.5 text-xs font-medium">
          <Sparkles className="text-primary size-3.5" aria-hidden />
          AI-assisted assessment
        </div>

        <div className="flex items-start gap-4">
          <span
            className={cn(
              "flex size-11 shrink-0 items-center justify-center rounded-xl",
              t.chip,
            )}
          >
            <Icon className={cn("size-6", t.icon)} aria-hidden />
          </span>
          <div className="min-w-0 space-y-1">
            <h2 className="text-xl font-semibold tracking-tight">{label}</h2>
            <p className="text-muted-foreground text-sm leading-relaxed">{sentence}</p>
          </div>
        </div>
      </div>

      <div className="space-y-4 p-6 pt-5">
        <ConfidenceMeter
          value={detail.confidence}
          emphasizeInsufficiency={detail.recommendation === "ESCALATE"}
        />
        <p className="text-muted-foreground border-t pt-4 text-xs leading-relaxed">
          Based on the candidate&rsquo;s submitted work-sample evidence. This is a proposal to
          support your judgement — <span className="text-foreground">final decisions remain with
          your hiring team.</span>
        </p>
      </div>
    </Card>
  );
}
