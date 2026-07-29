import { apiClient, type ApiResponse } from "@/lib/api-client";
import type {
  DecisionHistoryResponse,
  DecisionView,
  RecordDecisionRequest,
} from "@/types/decision";

// The accountable human decision. Recording appends a new immutable decision (a change of
// mind is a new record); history is preserved. The AI recommendation is at most an input.
export const DecisionService = {
  record: (
    candidateEvaluationId: string,
    body: RecordDecisionRequest,
  ): Promise<ApiResponse<DecisionView>> =>
    apiClient.post<DecisionView>(`/evaluations/${candidateEvaluationId}/decisions`, body),

  getHistory: (
    candidateEvaluationId: string,
  ): Promise<ApiResponse<DecisionHistoryResponse>> =>
    apiClient.get<DecisionHistoryResponse>(`/evaluations/${candidateEvaluationId}/decisions`),
};
