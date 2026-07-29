"""DashboardService tests — metrics correctness, empty tenant, needs-attention, and
cross-tenant isolation."""

from sqlalchemy.ext.asyncio import AsyncSession
from support import define_minimal_work_sample

from app.modules.campaigns.schemas import Competency, CreateCampaignRequest, RoleProfile
from app.modules.campaigns.service import CampaignService
from app.modules.candidates.schemas import AddCandidateRequest
from app.modules.candidates.service import CandidateService
from app.modules.dashboard.service import DashboardService


def _campaign_request() -> CreateCampaignRequest:
    return CreateCampaignRequest(
        role_title="Data Engineer",
        role_profile=RoleProfile(competencies=[Competency(name="SQL")], bar="senior"),
    )


async def _draft(session: AsyncSession, tenant: str) -> str:
    created = await CampaignService(session, tenant).create(_campaign_request())
    return created.id


async def _active(session: AsyncSession, tenant: str) -> str:
    service = CampaignService(session, tenant)
    created = await service.create(_campaign_request())
    await define_minimal_work_sample(session, tenant, created.id)  # required to activate
    await service.activate(created.id)
    return created.id


async def test_empty_tenant_dashboard_is_all_zeros(session: AsyncSession) -> None:
    dashboard = await DashboardService(session, "org-a").get()

    assert dashboard.metrics.total_campaigns == 0
    assert dashboard.metrics.total_candidates == 0
    assert dashboard.attention.draft_campaigns == 0
    assert dashboard.attention.active_campaigns_without_candidates == 0
    assert dashboard.recent_campaigns == []
    assert dashboard.recent_candidates == []


async def test_dashboard_metrics_and_attention(session: AsyncSession) -> None:
    await _draft(session, "org-a")  # 1 draft
    active_with = await _active(session, "org-a")  # active, will get a candidate
    await _active(session, "org-a")  # active, stays empty
    await CandidateService(session, "org-a").add_to_campaign(
        active_with,
        AddCandidateRequest(name="Ada", email="ada@x.com"),  # no résumé
    )

    dashboard = await DashboardService(session, "org-a").get()

    assert dashboard.metrics.total_campaigns == 3
    assert dashboard.metrics.active_campaigns == 2
    assert dashboard.metrics.draft_campaigns == 1
    assert dashboard.metrics.total_candidates == 1
    assert dashboard.metrics.candidates_missing_resume == 1
    # Needs attention: 1 draft, 1 active campaign with no candidates, 1 missing résumé.
    assert dashboard.attention.draft_campaigns == 1
    assert dashboard.attention.active_campaigns_without_candidates == 1
    assert dashboard.attention.candidates_missing_resume == 1
    assert len(dashboard.recent_campaigns) == 3
    assert len(dashboard.recent_candidates) == 1
    assert dashboard.recent_candidates[0].campaign_role_title == "Data Engineer"


async def test_dashboard_is_tenant_scoped(session: AsyncSession) -> None:
    # org-a has a campaign + candidate; org-b has nothing.
    campaign_id = await _active(session, "org-a")
    await CandidateService(session, "org-a").add_to_campaign(
        campaign_id, AddCandidateRequest(name="Ada", email="ada@x.com")
    )

    dashboard_b = await DashboardService(session, "org-b").get()

    assert dashboard_b.metrics.total_campaigns == 0
    assert dashboard_b.metrics.total_candidates == 0
    assert dashboard_b.recent_campaigns == []
    assert dashboard_b.recent_candidates == []
