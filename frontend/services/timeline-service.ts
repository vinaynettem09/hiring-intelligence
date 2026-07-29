import { apiClient, type ApiResponse } from "@/lib/api-client";
import type { HiringTimelineResponse } from "@/types/timeline";

// The exportable audit trail for one candidate evaluation — assembled server-side from
// authoritative records (consent, invitation, submission, evaluation runs, decisions).
export const TimelineService = {
  getTimeline: (
    candidateEvaluationId: string,
  ): Promise<ApiResponse<HiringTimelineResponse>> =>
    apiClient.get<HiringTimelineResponse>(`/evaluations/${candidateEvaluationId}/timeline`),
};
