"""Persistence for the identity module. Domain-language, not CRUD.

Repositories return ORM models for use *within* the service layer only. The
service maps them to DTOs before anything crosses to the API.
"""

from datetime import datetime

from sqlalchemy import select

from app.modules.identity.enums import UserRole
from app.modules.identity.models import Organization, RefreshToken, User
from app.shared.ids import new_id
from app.shared.repository import Repository


class OrganizationRepository(Repository):
    """Organizations are the tenant root, so this is not tenant-scoped."""

    async def create(self, name: str) -> Organization:
        organization = Organization(id=new_id(), name=name)
        self.session.add(organization)
        await self.session.flush()  # persist within the request's single transaction
        return organization

    async def get(self, organization_id: str) -> Organization | None:
        return await self.session.get(Organization, organization_id)


class UserRepository(Repository):
    """Users belong to a tenant (organization_id).

    `get_by_email` is a **global** lookup — the authentication seam, since email is
    a system-wide login identity. All *authorized* user access after login is
    tenant-scoped.
    """

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    async def get(self, user_id: str) -> User | None:
        return await self.session.get(User, user_id)

    async def create(
        self,
        *,
        organization_id: str,
        email: str,
        password_hash: str,
        role: UserRole,
    ) -> User:
        user = User(
            id=new_id(),
            organization_id=organization_id,
            email=email,
            password_hash=password_hash,
            role=role.value,
        )
        self.session.add(user)
        await self.session.flush()
        return user


class RefreshTokenRepository(Repository):
    async def create(self, *, user_id: str, token_hash: str, expires_at: datetime) -> RefreshToken:
        token = RefreshToken(
            id=new_id(), user_id=user_id, token_hash=token_hash, expires_at=expires_at
        )
        self.session.add(token)
        await self.session.flush()
        return token

    async def get_by_hash(self, token_hash: str) -> RefreshToken | None:
        result = await self.session.execute(
            select(RefreshToken).where(RefreshToken.token_hash == token_hash)
        )
        return result.scalar_one_or_none()
