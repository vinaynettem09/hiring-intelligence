import { apiClient, type ApiResponse } from "@/lib/api-client";
import type { QueueFilter, ReviewQueueResponse } from "@/types/review";

// The recruiter's operational inbox — one purpose-built read model, server-side filtering,
// search, and pagination (never client-side over an over-fetched set).
export const ReviewService = {
  getQueue: (params?: {
    filter?: QueueFilter;
    campaignId?: string;
    search?: string;
    limit?: number;
    offset?: number;
  }): Promise<ApiResponse<ReviewQueueResponse>> => {
    const q = new URLSearchParams();
    if (params?.filter && params.filter !== "all") q.set("filter", params.filter);
    if (params?.campaignId) q.set("campaign_id", params.campaignId);
    if (params?.search?.trim()) q.set("search", params.search.trim());
    if (params?.limit != null) q.set("limit", String(params.limit));
    if (params?.offset != null) q.set("offset", String(params.offset));
    const qs = q.toString();
    return apiClient.get<ReviewQueueResponse>(`/review-queue${qs ? `?${qs}` : ""}`);
  },
};
