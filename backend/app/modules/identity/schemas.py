"""Pydantic request/response DTOs for the identity module.

These — not ORM models — are what cross the API boundary. Shape validation
(email format, password length) happens here; business validation lives in the service.
"""

from pydantic import BaseModel, EmailStr, Field

from app.modules.identity.enums import UserRole


class SignupRequest(BaseModel):
    organization_name: str = Field(min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class OrganizationSummary(BaseModel):
    id: str
    name: str


class UserSummary(BaseModel):
    id: str
    email: EmailStr
    role: UserRole
    organization_id: str


class SignupResponse(BaseModel):
    organization: OrganizationSummary
    user: UserSummary


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"  # noqa: S105  OAuth token type, not a secret
    expires_in: int


class RefreshRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"  # noqa: S105  OAuth token type, not a secret
    expires_in: int


class MeResponse(BaseModel):
    """Canonical identity — the frontend asks the backend 'who am I' (no token parsing)."""

    id: str
    email: EmailStr
    role: UserRole
    organization: OrganizationSummary
