// The single place all backend calls go through. Components never call fetch()
// directly — they use a service (services/*), which uses this client. Add
// auth headers, retries, logging, etc. here once, not in every page.

import { authStore } from "@/lib/auth-store";

const BASE_URL = "/api"; // proxied to the backend by next.config rewrites (no CORS)
// Generous so a free-tier backend cold start (or a slower AI evaluation) doesn't trip the
// client abort ("signal is aborted without reason") before the server responds.
const DEFAULT_TIMEOUT_MS = 30_000;

/** Backend error shape (matches app/shared/error_handlers.py). */
export interface ApiErrorBody {
  type: string;
  code: string;
  message: string;
  correlation_id: string | null;
  metadata?: Record<string, unknown> | null;
}

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    public readonly body: ApiErrorBody,
  ) {
    super(body.message);
    this.name = "ApiError";
  }
}

/** Every call returns the body plus the correlation id (for support/logging). */
export interface ApiResponse<T> {
  data: T;
  correlationId: string | null;
}

async function request<T>(method: string, path: string, body?: unknown): Promise<ApiResponse<T>> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), DEFAULT_TIMEOUT_MS);
  try {
    const headers: Record<string, string> = {
      "Content-Type": "application/json",
      "X-Correlation-Id": crypto.randomUUID(),
    };
    const token = authStore.getAccess();
    if (token) headers["Authorization"] = `Bearer ${token}`;

    const response = await fetch(`${BASE_URL}${path}`, {
      method,
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
      signal: controller.signal,
    });

    const correlationId = response.headers.get("X-Correlation-Id");
    const data: unknown = await response.json().catch(() => null);

    if (!response.ok) {
      const fallback: ApiErrorBody = {
        type: "unknown",
        code: "UNKNOWN",
        message: response.statusText || "Request failed",
        correlation_id: correlationId,
      };
      throw new ApiError(response.status, (data as ApiErrorBody) ?? fallback);
    }
    return { data: data as T, correlationId };
  } finally {
    clearTimeout(timer);
  }
}

/** Multipart upload. The browser sets the multipart Content-Type + boundary, so we
 * must NOT set it ourselves. Auth + correlation id are attached as usual. */
async function upload<T>(path: string, formData: FormData): Promise<ApiResponse<T>> {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), DEFAULT_TIMEOUT_MS * 3); // uploads are slower
  try {
    const headers: Record<string, string> = { "X-Correlation-Id": crypto.randomUUID() };
    const token = authStore.getAccess();
    if (token) headers["Authorization"] = `Bearer ${token}`;

    const response = await fetch(`${BASE_URL}${path}`, {
      method: "POST",
      headers,
      body: formData,
      signal: controller.signal,
    });

    const correlationId = response.headers.get("X-Correlation-Id");
    const data: unknown = await response.json().catch(() => null);
    if (!response.ok) {
      const fallback: ApiErrorBody = {
        type: "unknown",
        code: "UNKNOWN",
        message: response.statusText || "Upload failed",
        correlation_id: correlationId,
      };
      throw new ApiError(response.status, (data as ApiErrorBody) ?? fallback);
    }
    return { data: data as T, correlationId };
  } finally {
    clearTimeout(timer);
  }
}

export const apiClient = {
  get: <T>(path: string): Promise<ApiResponse<T>> => request<T>("GET", path),
  post: <T>(path: string, body?: unknown): Promise<ApiResponse<T>> =>
    request<T>("POST", path, body),
  put: <T>(path: string, body?: unknown): Promise<ApiResponse<T>> => request<T>("PUT", path, body),
  upload: <T>(path: string, formData: FormData): Promise<ApiResponse<T>> =>
    upload<T>(path, formData),
};
