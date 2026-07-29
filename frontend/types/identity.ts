// Handwritten DTOs. Auth is not implemented yet (Epic 1.2); tenant_id/actor are null.

export type UserRole = "admin" | "recruiter" | "hiring_manager";

export interface MeResponse {
  id: string;
  email: string;
  role: UserRole;
  organization: { id: string; name: string };
}

export interface SignupRequest {
  organization_name: string;
  email: string;
  password: string;
}

export interface SignupResponse {
  organization: { id: string; name: string };
  user: { id: string; email: string; role: UserRole; organization_id: string };
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
  expires_in: number;
}

export interface LogoutRequest {
  refresh_token: string;
}
