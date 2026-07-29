import { apiClient, type ApiResponse } from "@/lib/api-client";
import type { DashboardResponse } from "@/types/dashboard";

export const DashboardService = {
  get: (): Promise<ApiResponse<DashboardResponse>> => apiClient.get<DashboardResponse>("/dashboard"),
};
