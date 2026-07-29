"""OrganizationRepository tests."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.identity.repository import OrganizationRepository


async def test_create_and_get_organization(session: AsyncSession) -> None:
    repo = OrganizationRepository(session)

    created = await repo.create(name="Acme Inc")
    assert created.id
    assert created.name == "Acme Inc"
    assert created.created_at is not None

    fetched = await repo.get(created.id)
    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.name == "Acme Inc"


async def test_get_missing_organization_returns_none(session: AsyncSession) -> None:
    repo = OrganizationRepository(session)
    assert await repo.get("does-not-exist") is None
