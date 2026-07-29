import { apiClient, type ApiResponse } from "@/lib/api-client";
import type {
  AddCandidateRequest,
  CandidateEvaluationResponse,
  CandidateImportSummary,
  RosterResponse,
} from "@/types/candidate";

export const CandidateService = {
  listRoster: (
    campaignId: string,
    params?: { limit?: number; offset?: number },
  ): Promise<ApiResponse<RosterResponse>> => {
    const query = new URLSearchParams();
    if (params?.limit != null) query.set("limit", String(params.limit));
    if (params?.offset != null) query.set("offset", String(params.offset));
    const qs = query.toString();
    return apiClient.get<RosterResponse>(`/campaigns/${campaignId}/candidates${qs ? `?${qs}` : ""}`);
  },

  add: (
    campaignId: string,
    body: AddCandidateRequest,
  ): Promise<ApiResponse<CandidateEvaluationResponse>> =>
    apiClient.post<CandidateEvaluationResponse>(`/campaigns/${campaignId}/candidates`, body),

  importCsv: (campaignId: string, file: File): Promise<ApiResponse<CandidateImportSummary>> => {
    const formData = new FormData();
    formData.append("file", file);
    return apiClient.upload<CandidateImportSummary>(
      `/campaigns/${campaignId}/candidates/import`,
      formData,
    );
  },
};
