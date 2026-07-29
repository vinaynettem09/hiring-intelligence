import { apiClient, type ApiResponse } from "@/lib/api-client";
import type {
  CandidateWorkSample,
  SavedResponse,
  SubmissionResult,
} from "@/types/candidate-work-sample";

// Candidate magic-link flow. The token (body) resolves the evaluation server-side; the
// server re-checks access + consent on every call.
export const CandidateWorkSampleService = {
  load: (token: string): Promise<ApiResponse<CandidateWorkSample>> =>
    apiClient.post<CandidateWorkSample>("/candidate/work-sample", { token }),

  saveResponse: (
    token: string,
    taskId: string,
    responseText: string,
  ): Promise<ApiResponse<SavedResponse>> =>
    apiClient.post<SavedResponse>("/candidate/work-sample/response", {
      token,
      task_id: taskId,
      response_text: responseText,
    }),

  submit: (token: string): Promise<ApiResponse<SubmissionResult>> =>
    apiClient.post<SubmissionResult>("/candidate/work-sample/submit", { token }),
};
