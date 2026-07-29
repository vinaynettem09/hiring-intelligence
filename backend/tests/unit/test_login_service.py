"""Login + refresh service tests (Story 1.2)."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.modules.identity.schemas import (
    LoginRequest,
    LogoutRequest,
    RefreshRequest,
    SignupRequest,
)
from app.modules.identity.service import IdentityService
from app.shared.errors import AuthenticationError
from app.shared.tokens import decode_access_token

_SIGNUP = SignupRequest(organization_name="Acme", email="founder@acme.com", password="password123")


async def _signup(session: AsyncSession) -> None:
    await IdentityService(session).signup(_SIGNUP)


async def test_login_succeeds_and_issues_tokens(session: AsyncSession) -> None:
    await _signup(session)
    result = await IdentityService(session).login(
        LoginRequest(email="founder@acme.com", password="password123")
    )
    assert result.token_type == "bearer"
    assert result.expires_in > 0
    assert result.refresh_token

    settings = get_settings()
    claims = decode_access_token(
        result.access_token, secret=settings.jwt_secret, algorithm=settings.jwt_algorithm
    )
    assert claims["role"] == "admin"
    assert claims["organization_id"]


async def test_login_wrong_password_is_rejected(session: AsyncSession) -> None:
    await _signup(session)
    with pytest.raises(AuthenticationError) as exc:
        await IdentityService(session).login(
            LoginRequest(email="founder@acme.com", password="wrong-password")
        )
    assert exc.value.code == "INVALID_CREDENTIALS"


async def test_login_unknown_email_is_rejected(session: AsyncSession) -> None:
    with pytest.raises(AuthenticationError) as exc:
        await IdentityService(session).login(
            LoginRequest(email="nobody@acme.com", password="password123")
        )
    assert exc.value.code == "INVALID_CREDENTIALS"


async def test_refresh_returns_new_access_token(session: AsyncSession) -> None:
    await _signup(session)
    login = await IdentityService(session).login(
        LoginRequest(email="founder@acme.com", password="password123")
    )
    refreshed = await IdentityService(session).refresh(
        RefreshRequest(refresh_token=login.refresh_token)
    )
    assert refreshed.token_type == "bearer"
    assert refreshed.access_token


async def test_refresh_rejects_unknown_token(session: AsyncSession) -> None:
    with pytest.raises(AuthenticationError) as exc:
        await IdentityService(session).refresh(RefreshRequest(refresh_token="not-a-real-token"))
    assert exc.value.code == "INVALID_REFRESH_TOKEN"


async def test_logout_revokes_refresh_token(session: AsyncSession) -> None:
    await _signup(session)
    login = await IdentityService(session).login(
        LoginRequest(email="founder@acme.com", password="password123")
    )
    await IdentityService(session).logout(LogoutRequest(refresh_token=login.refresh_token))

    # The revoked token can no longer be refreshed — the revocation payoff.
    with pytest.raises(AuthenticationError) as exc:
        await IdentityService(session).refresh(RefreshRequest(refresh_token=login.refresh_token))
    assert exc.value.code == "INVALID_REFRESH_TOKEN"


async def test_logout_unknown_token_is_idempotent(session: AsyncSession) -> None:
    # No error, no leak about whether the token existed.
    await IdentityService(session).logout(LogoutRequest(refresh_token="never-existed"))
