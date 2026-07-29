"""Identity application service.

- signup: create the organization (tenant) + first admin user.
- login:  verify credentials → issue a short-lived access JWT + an opaque,
          persisted, revocable refresh token.
- refresh: exchange a valid refresh token for a new access token.

Never commits (the request's session commits once). Never returns ORM models.
Password verification and token creation go through the centralized helpers.
"""

from datetime import UTC, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.modules.identity.enums import UserRole
from app.modules.identity.repository import (
    OrganizationRepository,
    RefreshTokenRepository,
    UserRepository,
)
from app.modules.identity.schemas import (
    AccessTokenResponse,
    LoginRequest,
    LoginResponse,
    LogoutRequest,
    MeResponse,
    OrganizationSummary,
    RefreshRequest,
    SignupRequest,
    SignupResponse,
    UserSummary,
)
from app.shared.errors import AuthenticationError, ConflictError, ValidationError
from app.shared.security import hash_password, verify_password
from app.shared.tokens import (
    create_access_token,
    generate_refresh_token,
    hash_refresh_token,
)


def _validate_organization_name(name: str) -> None:
    if not name.strip():
        raise ValidationError("Organization name is required.", code="ORGANIZATION_NAME_REQUIRED")


def validate_signup(request: SignupRequest) -> None:
    """Business validation for signup. Small validators, orchestrated here — this
    is where signup validation grows as Epic 1 expands."""
    _validate_organization_name(request.organization_name)


class IdentityService:
    def __init__(self, session: AsyncSession) -> None:
        self._organizations = OrganizationRepository(session)
        self._users = UserRepository(session)
        self._refresh_tokens = RefreshTokenRepository(session)

    async def signup(self, request: SignupRequest) -> SignupResponse:
        validate_signup(request)

        if await self._users.get_by_email(request.email) is not None:
            raise ConflictError(
                "An account with this email already exists.",
                code="USER_ALREADY_EXISTS",
            )

        organization = await self._organizations.create(name=request.organization_name.strip())
        user = await self._users.create(
            organization_id=organization.id,
            email=request.email,
            password_hash=hash_password(request.password),
            role=UserRole.ADMIN,  # the first user is the org admin
        )

        return SignupResponse(
            organization=OrganizationSummary(id=organization.id, name=organization.name),
            user=UserSummary(
                id=user.id,
                email=user.email,
                role=UserRole(user.role),
                organization_id=organization.id,
            ),
        )

    async def login(self, request: LoginRequest) -> LoginResponse:
        user = await self._users.get_by_email(request.email)
        # Verify even on missing user is unnecessary; a generic error avoids leaking
        # whether the email exists.
        if user is None or not verify_password(user.password_hash, request.password):
            raise AuthenticationError("Invalid email or password.", code="INVALID_CREDENTIALS")

        settings = get_settings()
        access_token, expires_in = create_access_token(
            user_id=user.id,
            organization_id=user.organization_id,
            role=user.role,
            secret=settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
            ttl_seconds=settings.access_token_ttl_seconds,
        )
        refresh_value = generate_refresh_token()
        await self._refresh_tokens.create(
            user_id=user.id,
            token_hash=hash_refresh_token(refresh_value),
            expires_at=datetime.now(UTC) + timedelta(seconds=settings.refresh_token_ttl_seconds),
        )

        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_value,
            expires_in=expires_in,
        )

    async def refresh(self, request: RefreshRequest) -> AccessTokenResponse:
        record = await self._refresh_tokens.get_by_hash(hash_refresh_token(request.refresh_token))
        expires_at = record.expires_at if record else None
        if expires_at is not None and expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=UTC)  # sqlite returns naive; treat as UTC

        if record is None or record.revoked or expires_at is None or expires_at < datetime.now(UTC):
            raise AuthenticationError(
                "Invalid or expired refresh token.", code="INVALID_REFRESH_TOKEN"
            )

        record.last_used_at = datetime.now(UTC)  # metadata; committed with the request

        user = await self._users.get(record.user_id)
        if user is None:  # pragma: no cover - defensive; FK guarantees presence
            raise AuthenticationError("Invalid refresh token.", code="INVALID_REFRESH_TOKEN")

        settings = get_settings()
        access_token, expires_in = create_access_token(
            user_id=user.id,
            organization_id=user.organization_id,
            role=user.role,
            secret=settings.jwt_secret,
            algorithm=settings.jwt_algorithm,
            ttl_seconds=settings.access_token_ttl_seconds,
        )
        return AccessTokenResponse(access_token=access_token, expires_in=expires_in)

    async def logout(self, request: LogoutRequest) -> None:
        """Revoke a refresh token. Idempotent — an unknown or already-revoked token
        is a no-op (and never reveals whether it existed)."""
        record = await self._refresh_tokens.get_by_hash(hash_refresh_token(request.refresh_token))
        if record is not None and not record.revoked:
            record.revoked = True  # committed with the request

    async def get_identity(self, user_id: str) -> MeResponse:
        """Canonical identity for the authenticated user (Story 1.3 /me)."""
        user = await self._users.get(user_id)
        if user is None:  # pragma: no cover - token verified, user must exist
            raise AuthenticationError("Account not found.", code="NOT_AUTHENTICATED")
        organization = await self._organizations.get(user.organization_id)
        if organization is None:  # pragma: no cover - FK guarantees presence
            raise AuthenticationError("Organization not found.", code="NOT_AUTHENTICATED")
        return MeResponse(
            id=user.id,
            email=user.email,
            role=UserRole(user.role),
            organization=OrganizationSummary(id=organization.id, name=organization.name),
        )
