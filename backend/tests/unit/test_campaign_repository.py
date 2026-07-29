"""CampaignRepository tests — tenant isolation is the point (Story 2.1).

The critical guarantee: a repository scoped to one organization can never read
another organization's campaign. This is INV-000/INV-001 enforced in code, not by
developer discipline. (SQLite FK enforcement is off in tests, so we use plain tenant
ids to exercise the tenant filter directly.)
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.campaigns.enums import CampaignStatus
from app.modules.campaigns.repository import CampaignRepository

_ROLE_PROFILE = {
    "competencies": [{"name": "SQL", "description": "writes correct joins"}],
    "bar": "senior: independently ships correct queries",
}


async def test_create_yields_a_draft_owned_by_the_tenant(session: AsyncSession) -> None:
    repo = CampaignRepository(session, tenant_id="org-a")

    campaign = await repo.create_draft(role_title="Data Engineer", role_profile=_ROLE_PROFILE)

    assert campaign.id
    assert campaign.organization_id == "org-a"
    assert campaign.role_title == "Data Engineer"
    assert campaign.status == CampaignStatus.DRAFT.value  # born draft
    assert campaign.created_at is not None


async def test_get_returns_own_campaign(session: AsyncSession) -> None:
    repo = CampaignRepository(session, tenant_id="org-a")
    created = await repo.create_draft(role_title="Data Engineer", role_profile=_ROLE_PROFILE)

    fetched = await repo.get(created.id)

    assert fetched is not None
    assert fetched.id == created.id


async def test_get_missing_returns_none(session: AsyncSession) -> None:
    repo = CampaignRepository(session, tenant_id="org-a")
    assert await repo.get("does-not-exist") is None


async def test_other_tenant_cannot_read_campaign(session: AsyncSession) -> None:
    """The whole reason TenantScopedRepository exists: org B cannot read org A's data."""
    org_a = CampaignRepository(session, tenant_id="org-a")
    org_b = CampaignRepository(session, tenant_id="org-b")

    campaign = await org_a.create_draft(role_title="Data Engineer", role_profile=_ROLE_PROFILE)

    # Same id, different tenant → invisible (None), not an error, not the row.
    assert await org_b.get(campaign.id) is None
    # And the owner still sees it — isolation, not breakage.
    assert await org_a.get(campaign.id) is not None


async def test_list_and_count_are_tenant_scoped(session: AsyncSession) -> None:
    org_a = CampaignRepository(session, tenant_id="org-a")
    org_b = CampaignRepository(session, tenant_id="org-b")
    await org_a.create_draft(role_title="A1", role_profile=_ROLE_PROFILE)
    await org_a.create_draft(role_title="A2", role_profile=_ROLE_PROFILE)
    await org_b.create_draft(role_title="B1", role_profile=_ROLE_PROFILE)

    a_titles = {c.role_title for c in await org_a.list_for_tenant(limit=10, offset=0)}
    assert a_titles == {"A1", "A2"}  # never B1
    assert await org_a.count_for_tenant() == 2
    assert await org_b.count_for_tenant() == 1


async def test_list_is_newest_first(session: AsyncSession) -> None:
    repo = CampaignRepository(session, tenant_id="org-a")
    for title in ("first", "second", "third"):
        await repo.create_draft(role_title=title, role_profile=_ROLE_PROFILE)

    created_ats = [c.created_at for c in await repo.list_for_tenant(limit=10, offset=0)]
    # Non-increasing: robust even if the OS clock ties two rows to the same instant.
    assert created_ats == sorted(created_ats, reverse=True)


async def test_list_paginates(session: AsyncSession) -> None:
    repo = CampaignRepository(session, tenant_id="org-a")
    for i in range(3):
        await repo.create_draft(role_title=f"c{i}", role_profile=_ROLE_PROFILE)

    page1 = await repo.list_for_tenant(limit=2, offset=0)
    page2 = await repo.list_for_tenant(limit=2, offset=2)

    assert len(page1) == 2
    assert len(page2) == 1
    # Pages are disjoint and together cover everything (no gaps, no repeats).
    assert len({c.id for c in page1} | {c.id for c in page2}) == 3
