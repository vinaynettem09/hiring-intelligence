// Handwritten DTOs mirroring app/modules/review/schemas.py.
// The queue carries authoritative state; the frontend owns all recruiter display copy
// (recommendation/confidence via components/ai/presentation.ts; stage via queue-presentation).

import type { DecisionType } from "@/types/decision";
import type { Recommendation } from "@/types/evaluation";

export type QueueStage =
  | "AWAITING_INVITATION"
  | "AWAITING_CANDIDATE"
  | "READY_FOR_EVALUATION"
  | "NEEDS_REVIEW"
  | "EVALUATED";

export type QueueFilter = "all" | "needs_attention" | "ready" | "waiting" | "completed";

export interface ReviewQueueItem {
  candidate_evaluation_id: string;
  candidate_name: string;
  candidate_email: string;
  campaign_id: string;
  role_title: string;
  stage: QueueStage;
  needs_attention: boolean;
  recommendation: Recommendation | null;
  confidence: number | null;
  run_number: number | null;
  decision: DecisionType | null; // latest human decision, if recorded (badge only)
  last_activity_at: string;
}

export interface ReviewQueueSummary {
  needs_review: number;
  ready_to_evaluate: number;
  awaiting_invitation: number;
  waiting_on_candidate: number;
  completed: number;
  total: number;
}

export interface ReviewQueueResponse {
  items: ReviewQueueItem[];
  summary: ReviewQueueSummary;
  total: number;
  limit: number;
  offset: number;
}
