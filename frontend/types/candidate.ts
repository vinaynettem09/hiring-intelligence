// Handwritten DTOs mirroring app/modules/candidates/schemas.py.

export type EvaluationStatus = "invited" | "submitted";

export interface CandidateSummary {
  id: string;
  name: string;
  email: string;
}

/** One roster row (recruiter-facing — includes candidate PII). */
export interface RosterEntry {
  evaluation_id: string;
  candidate: CandidateSummary;
  status: EvaluationStatus;
  has_resume: boolean;
  created_at: string;
  // Evaluation status for the contextual action (Generate vs. View) + a glanceable badge.
  has_evaluation: boolean;
  latest_recommendation: string | null;
  latest_run_number: number | null;
}

export interface RosterResponse {
  items: RosterEntry[];
  total: number;
  missing_resume: number;
  limit: number;
  offset: number;
}

export interface AddCandidateRequest {
  name: string;
  email: string;
  resume_object_key?: string | null;
}

export interface CandidateEvaluationResponse {
  id: string;
  campaign_id: string;
  candidate: CandidateSummary;
  status: EvaluationStatus;
  created_at: string;
}

export interface CandidateImportIssue {
  row: number;
  email: string | null;
  outcome: "skipped" | "failed";
  reason: string;
}

export interface CandidateImportSummary {
  total: number;
  imported: number;
  skipped: number;
  failed: number;
  issues: CandidateImportIssue[];
}
