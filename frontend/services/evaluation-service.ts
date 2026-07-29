import { apiClient, type ApiResponse } from "@/lib/api-client";
import type {
  EvaluationDetail,
  EvaluationHistoryResponse,
  SubmittedEvidenceResponse,
} from "@/types/evaluation";

// All calls hit the existing recruiter-facing evaluation execution + read API. `generate`
// is idempotent server-side (a repeat returns the existing run without re-calling the
// provider); `rerun` deliberately creates a NEW immutable run and never mutates history.
export const EvaluationService = {
  /** History for a candidate evaluation: latest run in full + run summaries. */
  getHistory: (
    candidateEvaluationId: string,
  ): Promise<ApiResponse<EvaluationHistoryResponse>> =>
    apiClient.get<EvaluationHistoryResponse>(`/evaluations/${candidateEvaluationId}`),

  /** Generate the first evaluation (idempotent — returns the existing run if one exists). */
  generate: (candidateEvaluationId: string): Promise<ApiResponse<EvaluationDetail>> =>
    apiClient.post<EvaluationDetail>(`/evaluations/${candidateEvaluationId}/evaluate`),

  /** Explicitly create a new immutable run using the current evaluation configuration. */
  rerun: (candidateEvaluationId: string): Promise<ApiResponse<EvaluationDetail>> =>
    apiClient.post<EvaluationDetail>(`/evaluations/${candidateEvaluationId}/rerun`),

  /** The submitted evidence behind an evaluation's citations (claim -> citation -> source). */
  getEvidence: (
    candidateEvaluationId: string,
  ): Promise<ApiResponse<SubmittedEvidenceResponse>> =>
    apiClient.get<SubmittedEvidenceResponse>(`/evaluations/${candidateEvaluationId}/evidence`),
};
