"""Dashboard service — assembles the tenant's read model in one place."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.campaigns.enums import CampaignStatus
from app.modules.dashboard.repository import DashboardRepository
from app.modules.dashboard.schemas import (
    DashboardAttention,
    DashboardCampaign,
    DashboardCandidate,
    DashboardMetrics,
    DashboardResponse,
)

_RECENT_LIMIT = 5


class DashboardService:
    def __init__(self, session: AsyncSession, tenant_id: str) -> None:
        self._repo = DashboardRepository(session, tenant_id)

    async def get(self) -> DashboardResponse:
        metrics = DashboardMetrics(
            total_campaigns=await self._repo.count_campaigns(),
            active_campaigns=await self._repo.count_campaigns(status=CampaignStatus.ACTIVE.value),
            draft_campaigns=await self._repo.count_campaigns(status=CampaignStatus.DRAFT.value),
            total_candidates=await self._repo.count_candidates(),
            candidates_missing_resume=await self._repo.count_candidates_missing_resume(),
        )
        attention = DashboardAttention(
            draft_campaigns=metrics.draft_campaigns,
            active_campaigns_without_candidates=(
                await self._repo.count_active_campaigns_without_candidates()
            ),
            candidates_missing_resume=metrics.candidates_missing_resume,
        )
        recent_campaigns = [
            DashboardCampaign(
                id=campaign.id,
                role_title=campaign.role_title,
                status=CampaignStatus(campaign.status),
                created_at=campaign.created_at,
            )
            for campaign in await self._repo.recent_campaigns(_RECENT_LIMIT)
        ]
        recent_candidates = [
            DashboardCandidate(
                evaluation_id=evaluation.id,
                name=candidate.name,
                email=candidate.email,
                campaign_id=campaign.id,
                campaign_role_title=campaign.role_title,
                created_at=evaluation.created_at,
            )
            for evaluation, candidate, campaign in await self._repo.recent_candidates(_RECENT_LIMIT)
        ]
        return DashboardResponse(
            metrics=metrics,
            attention=attention,
            recent_campaigns=recent_campaigns,
            recent_candidates=recent_candidates,
        )
