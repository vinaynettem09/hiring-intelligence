import { apiClient, type ApiResponse } from "@/lib/api-client";
import type { DefineWorkSampleRequest, WorkSample } from "@/types/work-sample";

export const WorkSampleService = {
  get: (campaignId: string): Promise<ApiResponse<WorkSample>> =>
    apiClient.get<WorkSample>(`/campaigns/${campaignId}/work-sample`),

  // "Define the whole work sample" — one business operation, not per-question CRUD.
  define: (
    campaignId: string,
    body: DefineWorkSampleRequest,
  ): Promise<ApiResponse<WorkSample>> =>
    apiClient.put<WorkSample>(`/campaigns/${campaignId}/work-sample`, body),
};
