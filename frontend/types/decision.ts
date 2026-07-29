// Handwritten DTOs mirroring app/modules/decisions/schemas.py.
// A decision is the accountable HUMAN act — distinct from the AI's recommendation.

export type DecisionType = "ADVANCE" | "HOLD" | "DECLINE";

export interface RecordDecisionRequest {
  decision: DecisionType;
  rationale?: string | null;
  evaluation_id?: string | null; // the AI run that informed it (optional — AI is advisory)
}

export interface DecisionView {
  id: string;
  decision: DecisionType;
  rationale: string | null;
  decided_by_email: string;
  decided_at: string;
  informed_by_run_number: number | null;
  created_at: string;
}

export interface DecisionHistoryResponse {
  candidate_evaluation_id: string;
  latest: DecisionView | null;
  decisions: DecisionView[]; // append-only, newest first
}
