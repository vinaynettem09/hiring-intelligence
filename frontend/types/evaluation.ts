// Handwritten DTOs mirroring the recruiter-facing evaluation API
// (app/modules/evaluations/schemas.py + app/modules/evidence/schemas.py).
// These are the validated, grounded PROPOSAL — never raw provider output, never a decision.

export type Recommendation =
  | "STRONG_PROCEED"
  | "PROCEED"
  | "MIXED"
  | "DO_NOT_PROCEED"
  | "ESCALATE";

export type EscalationReason = "INSUFFICIENT_EVIDENCE" | "LOW_CONFIDENCE";

/** A verified link from a claim to real submitted evidence (ids, never model quotes). */
export interface CitationView {
  evidence_id: string;
  task_id: string;
}

export interface CompetencyAssessmentView {
  competency: string;
  assessment: string;
  provider_signal: number | null;
  citations: CitationView[];
}

/** A grounded strength or concern — always carries its evidence citations. */
export interface ObservationView {
  text: string;
  citations: CitationView[];
}

export interface EvidenceCoverageView {
  competencies_total: number;
  competencies_assessed: number;
  tasks_total: number;
  tasks_with_evidence: number;
}

export interface ProvenanceView {
  provider: string;
  model: string;
  model_version: string;
  prompt_version: string;
  input_schema_version: string;
  output_schema_version: string;
  confidence_algorithm_version: string;
  generated_at: string;
}

export interface EvaluationDetail {
  id: string;
  candidate_evaluation_id: string;
  run_number: number;
  recommendation: Recommendation;
  /** Platform-computed evidence-RELIABILITY signal in [0,1]. NOT a success probability. */
  confidence: number;
  confidence_rationale: string;
  escalation_reason: EscalationReason | null;
  competency_assessments: CompetencyAssessmentView[];
  strengths: ObservationView[];
  concerns: ObservationView[];
  evidence_coverage: EvidenceCoverageView;
  provenance: ProvenanceView;
  input_fingerprint: string;
  input_tokens: number | null;
  output_tokens: number | null;
  created_at: string;
}

export interface EvaluationRunSummary {
  id: string;
  run_number: number;
  recommendation: Recommendation;
  confidence: number;
  model: string;
  prompt_version: string;
  created_at: string;
}

export interface EvaluationHistoryResponse {
  candidate_evaluation_id: string;
  run_count: number;
  latest: EvaluationDetail | null;
  runs: EvaluationRunSummary[];
}

// --- submitted evidence (the citation -> source trust anchor) --- //

export interface SubmittedEvidenceItem {
  evidence_id: string;
  task_id: string;
  task_number: number;
  task_prompt: string;
  evidence_intent: string;
  response_text: string;
  captured_at: string;
}

export interface SubmittedEvidenceResponse {
  candidate_evaluation_id: string;
  items: SubmittedEvidenceItem[];
}
