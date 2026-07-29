import { apiClient, type ApiResponse } from "@/lib/api-client";
import type {
  LoginRequest,
  LoginResponse,
  LogoutRequest,
  MeResponse,
  SignupRequest,
  SignupResponse,
} from "@/types/identity";

export const IdentityService = {
  getMe: (): Promise<ApiResponse<MeResponse>> => apiClient.get<MeResponse>("/me"),

  signup: (body: SignupRequest): Promise<ApiResponse<SignupResponse>> =>
    apiClient.post<SignupResponse>("/auth/signup", body),

  login: (body: LoginRequest): Promise<ApiResponse<LoginResponse>> =>
    apiClient.post<LoginResponse>("/auth/login", body),

  logout: (body: LogoutRequest): Promise<ApiResponse<null>> =>
    apiClient.post<null>("/auth/logout", body),
};
