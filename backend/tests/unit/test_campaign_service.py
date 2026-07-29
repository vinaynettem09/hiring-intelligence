"""CampaignService tests (Story 2.1 create, Story 2.2 activate)."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from support import define_minimal_work_sample

from app.modules.campaigns.enums import CampaignStatus
from app.modules.campaigns.schemas import (
    Competency,
    CreateCampaignRequest,
    RoleProfile,
)
from app.modules.campaigns.service import CampaignService
from app.shared.errors import NotFoundError


def _request() -> CreateCampaignRequest:
    return CreateCampaignRequest(
        role_title="Data Engineer",
        role_profile=RoleProfile(
            competencies=[Competency(name="SQL", description="writes correct joins")],
            bar="senior: independently ships correct queries",
        ),
    )


async def test_create_returns_a_draft_campaign_dto(session: AsyncSession) -> None:
    service = CampaignService(session, tenant_id="org-a")

    response = await service.create(_request())

    assert response.id
    assert response.status is CampaignStatus.DRAFT
    assert response.role_title == "Data Engineer"
    assert response.role_profile.competencies[0].name == "SQL"
    assert response.role_profile.bar.startswith("senior")
    assert response.created_at is not None


async def test_activate_transitions_draft_to_active(session: AsyncSession) -> None:
    service = CampaignService(session, tenant_id="org-a")
    created = await service.create(_request())
    await define_minimal_work_sample(session, "org-a", created.id)  # required to activate

    activated = await service.activate(created.id)

    assert activated.id == created.id
    assert activated.status is CampaignStatus.ACTIVE


async def test_activate_missing_campaign_raises_not_found(session: AsyncSession) -> None:
    service = CampaignService(session, tenant_id="org-a")
    with pytest.raises(NotFoundError) as exc:
        await service.activate("does-not-exist")
    assert exc.value.code == "CAMPAIGN_NOT_FOUND"


async def test_cannot_activate_another_tenants_campaign(session: AsyncSession) -> None:
    """Isolation on a write path: org-b cannot even see org-a's campaign, so an
    activation attempt is a 404 (not a 403) — we never confirm it exists."""
    created = await CampaignService(session, tenant_id="org-a").create(_request())

    with pytest.raises(NotFoundError) as exc:
        await CampaignService(session, tenant_id="org-b").activate(created.id)
    assert exc.value.code == "CAMPAIGN_NOT_FOUND"


async def test_list_returns_summaries_and_total(session: AsyncSession) -> None:
    service = CampaignService(session, tenant_id="org-a")
    await service.create(_request())
    await service.create(_request())

    result = await service.list_campaigns(limit=10, offset=0)

    assert result.total == 2
    assert result.limit == 10
    assert result.offset == 0
    assert len(result.items) == 2
    # Summaries are lightweight — they carry no role_profile.
    assert not hasattr(result.items[0], "role_profile")


async def test_list_excludes_other_tenants(session: AsyncSession) -> None:
    await CampaignService(session, tenant_id="org-a").create(_request())

    result = await CampaignService(session, tenant_id="org-b").list_campaigns(limit=10, offset=0)

    assert result.total == 0
    assert result.items == []


async def test_get_returns_full_detail(session: AsyncSession) -> None:
    service = CampaignService(session, tenant_id="org-a")
    created = await service.create(_request())

    detail = await service.get(created.id)

    assert detail.id == created.id
    assert detail.role_profile.competencies[0].name == "SQL"  # full config present


async def test_get_missing_raises_not_found(session: AsyncSession) -> None:
    service = CampaignService(session, tenant_id="org-a")
    with pytest.raises(NotFoundError) as exc:
        await service.get("does-not-exist")
    assert exc.value.code == "CAMPAIGN_NOT_FOUND"


async def test_cannot_get_another_tenants_campaign(session: AsyncSession) -> None:
    created = await CampaignService(session, tenant_id="org-a").create(_request())

    with pytest.raises(NotFoundError) as exc:
        await CampaignService(session, tenant_id="org-b").get(created.id)
    assert exc.value.code == "CAMPAIGN_NOT_FOUND"
