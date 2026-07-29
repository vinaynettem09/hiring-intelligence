import { apiClient, type ApiResponse } from "@/lib/api-client";
import type { CandidateInvitationView, InvitationSummary } from "@/types/invitation";

export const InvitationService = {
  // Recruiter: issue/replace an invitation for a candidate evaluation.
  issue: (evaluationId: string): Promise<ApiResponse<InvitationSummary>> =>
    apiClient.post<InvitationSummary>(`/evaluations/${evaluationId}/invitation`),

  // Candidate: resolve a magic-link token (sent in the body, never a URL/query).
  resolve: (token: string): Promise<ApiResponse<CandidateInvitationView>> =>
    apiClient.post<CandidateInvitationView>("/candidate/invitation", { token }),
};
