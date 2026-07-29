import { apiClient, type ApiResponse } from "@/lib/api-client";
import type { Campaign, CampaignListResponse, CreateCampaignRequest } from "@/types/campaign";

export const CampaignService = {
  create: (body: CreateCampaignRequest): Promise<ApiResponse<Campaign>> =>
    apiClient.post<Campaign>("/campaigns", body),

  activate: (id: string): Promise<ApiResponse<Campaign>> =>
    apiClient.post<Campaign>(`/campaigns/${id}/activate`),

  list: (params?: { limit?: number; offset?: number }): Promise<ApiResponse<CampaignListResponse>> => {
    const query = new URLSearchParams();
    if (params?.limit != null) query.set("limit", String(params.limit));
    if (params?.offset != null) query.set("offset", String(params.offset));
    const qs = query.toString();
    return apiClient.get<CampaignListResponse>(`/campaigns${qs ? `?${qs}` : ""}`);
  },

  get: (id: string): Promise<ApiResponse<Campaign>> => apiClient.get<Campaign>(`/campaigns/${id}`),
};
