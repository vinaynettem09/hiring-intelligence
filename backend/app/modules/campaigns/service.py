"""Campaigns application service.

Constructed with the caller's tenant id (from the verified token, via AuthContext),
so every operation is inherently scoped to that organization. Never commits (the
request's session commits once) and never returns ORM models.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.campaigns.enums import CampaignStatus
from app.modules.campaigns.models import Campaign
from app.modules.campaigns.repository import CampaignRepository
from app.modules.campaigns.schemas import (
    CampaignListResponse,
    CampaignResponse,
    CampaignSummary,
    CreateCampaignRequest,
    RoleProfile,
)
from app.modules.worksample.service import WorkSampleService
from app.shared.errors import NotFoundError


class CampaignService:
    def __init__(self, session: AsyncSession, tenant_id: str) -> None:
        self._campaigns = CampaignRepository(session, tenant_id)
        self._work_samples = WorkSampleService(session, tenant_id)

    async def create(self, request: CreateCampaignRequest) -> CampaignResponse:
        campaign = await self._campaigns.create_draft(
            role_title=request.role_title,
            role_profile=request.role_profile.model_dump(),
        )
        return self._to_response(campaign)

    async def activate(self, campaign_id: str) -> CampaignResponse:
        """Activate one of this tenant's campaigns. The model owns the state-machine
        guards (draft-only, no reopening, role-profile complete); the service adds the
        cross-aggregate readiness rule — a valid Structured Work Sample that covers every
        competency (INV-011) — before committing the one-way transition (INV-003/005)."""
        campaign = await self._require(campaign_id)
        campaign.assert_can_activate()  # draft + role profile (correct error precedence)
        competency_names = [
            c["name"]
            for c in (campaign.role_profile or {}).get("competencies", [])
            if c.get("name")
        ]
        await self._work_samples.assert_ready_for_activation(campaign_id, competency_names)
        campaign.activate()  # sets status = active
        return self._to_response(campaign)

    async def get(self, campaign_id: str) -> CampaignResponse:
        """Full detail for one of this tenant's campaigns (404 otherwise)."""
        return self._to_response(await self._require(campaign_id))

    async def list_campaigns(self, *, limit: int, offset: int) -> CampaignListResponse:
        """This tenant's campaigns as lightweight summaries, newest first."""
        campaigns = await self._campaigns.list_for_tenant(limit=limit, offset=offset)
        total = await self._campaigns.count_for_tenant()
        return CampaignListResponse(
            items=[self._to_summary(c) for c in campaigns],
            total=total,
            limit=limit,
            offset=offset,
        )

    async def _require(self, campaign_id: str) -> Campaign:
        # get() is tenant-scoped: another org's campaign is None → "does not exist"
        # (a 404, never a 403 — we don't confirm other tenants' resources exist).
        campaign = await self._campaigns.get(campaign_id)
        if campaign is None:
            raise NotFoundError("Campaign not found.", code="CAMPAIGN_NOT_FOUND")
        return campaign

    @staticmethod
    def _to_response(campaign: Campaign) -> CampaignResponse:
        return CampaignResponse(
            id=campaign.id,
            role_title=campaign.role_title,
            role_profile=RoleProfile.model_validate(campaign.role_profile),
            status=CampaignStatus(campaign.status),
            created_at=campaign.created_at,
        )

    @staticmethod
    def _to_summary(campaign: Campaign) -> CampaignSummary:
        return CampaignSummary(
            id=campaign.id,
            role_title=campaign.role_title,
            status=CampaignStatus(campaign.status),
            created_at=campaign.created_at,
        )
