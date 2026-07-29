// Test-only synthetic fixtures (never imported by app pages, so never bundled).
import type {
  CompetencyAssessmentView,
  EvaluationDetail,
  ObservationView,
  Recommendation,
} from "@/types/evaluation";

export function makeEvaluationDetail(over: Partial<EvaluationDetail> = {}): EvaluationDetail {
  return {
    id: "ev-1",
    candidate_evaluation_id: "ce-1",
    run_number: 1,
    recommendation: "PROCEED" as Recommendation,
    confidence: 0.9,
    confidence_rationale: "sufficiency x decisiveness",
    escalation_reason: null,
    competency_assessments: [],
    strengths: [],
    concerns: [],
    evidence_coverage: {
      competencies_total: 2,
      competencies_assessed: 2,
      tasks_total: 2,
      tasks_with_evidence: 2,
    },
    provenance: {
      provider: "gemini",
      model: "gemini-3.6-flash",
      model_version: "gemini-3.6-flash",
      prompt_version: "eval-prompt-v3",
      input_schema_version: "eval-input-v1",
      output_schema_version: "eval-proposal-v1",
      confidence_algorithm_version: "confidence-v2",
      generated_at: "2026-07-29T10:00:00Z",
    },
    input_fingerprint: "sha256:abc",
    input_tokens: 1400,
    output_tokens: 200,
    created_at: "2026-07-29T10:00:00Z",
    ...over,
  };
}

export function observation(text: string, taskNumber = 1): ObservationView {
  return { text, citations: [{ evidence_id: `ev-${taskNumber}`, task_id: `task-${taskNumber}` }] };
}

export function assessment(competency: string): CompetencyAssessmentView {
  return {
    competency,
    assessment: `Grounded assessment for ${competency}.`,
    provider_signal: null,
    citations: [{ evidence_id: "ev-1", task_id: "task-1" }],
  };
}
