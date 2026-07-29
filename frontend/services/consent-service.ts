import { apiClient, type ApiResponse } from "@/lib/api-client";
import type { ConsentState } from "@/types/consent";

// Candidate magic-link flow — the token (body) resolves the evaluation server-side.
export const ConsentService = {
  getState: (token: string): Promise<ApiResponse<ConsentState>> =>
    apiClient.post<ConsentState>("/candidate/consent", { token }),

  grant: (token: string): Promise<ApiResponse<ConsentState>> =>
    apiClient.post<ConsentState>("/candidate/consent/grant", { token }),
};
