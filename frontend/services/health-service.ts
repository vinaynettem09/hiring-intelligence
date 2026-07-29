import { apiClient, type ApiResponse } from "@/lib/api-client";
import type { HealthResponse } from "@/types/health";

// Services talk to the API; components render. One method per backend operation.
export const HealthService = {
  get: (): Promise<ApiResponse<HealthResponse>> => apiClient.get<HealthResponse>("/health"),
};
