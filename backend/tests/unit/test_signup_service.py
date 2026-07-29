"""Signup service tests (Story 1.1) — the DoD, at the service level."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.identity.enums import UserRole
from app.modules.identity.repository import UserRepository
from app.modules.identity.schemas import SignupRequest
from app.modules.identity.service import IdentityService
from app.shared.errors import ConflictError
from app.shared.security import verify_password


def _request(email: str = "founder@acme.com", org: str = "Acme") -> SignupRequest:
    return SignupRequest(organization_name=org, email=email, password="password123")


async def test_signup_creates_org_and_admin_user(session: AsyncSession) -> None:
    result = await IdentityService(session).signup(_request())
    assert result.organization.name == "Acme"
    assert result.user.email == "founder@acme.com"
    assert result.user.role is UserRole.ADMIN
    assert result.user.organization_id == result.organization.id


async def test_signup_hashes_password(session: AsyncSession) -> None:
    await IdentityService(session).signup(_request())
    user = await UserRepository(session).get_by_email("founder@acme.com")
    assert user is not None
    assert user.password_hash != "password123"
    assert verify_password(user.password_hash, "password123")


async def test_signup_rejects_duplicate_email(session: AsyncSession) -> None:
    await IdentityService(session).signup(_request())
    with pytest.raises(ConflictError) as exc:
        await IdentityService(session).signup(_request(org="Different Co"))
    assert exc.value.code == "USER_ALREADY_EXISTS"
