// Handwritten DTO independent of the backend's internal types.
// If we adopt OpenAPI generation later, this can become generated.

export interface HealthResponse {
  status: "healthy" | "degraded";
  checks: Record<string, string>;
  version: string;
}
