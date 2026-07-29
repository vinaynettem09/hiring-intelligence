"""Persistence for campaigns — the **first real `TenantScopedRepository`**.

Every read here goes through the tenant filter (`_scoped`) so a caller physically
cannot fetch another organization's campaign (INV-000/INV-001). The tenant id is
supplied by the service from the verified token — never from request data.
Repositories persist (`add`/`flush`); they never commit.
"""

from collections.abc import Sequence
from typing import Any

from sqlalchemy import func, select

from app.modules.campaigns.enums import CampaignStatus
from app.modules.campaigns.models import Campaign
from app.shared.ids import new_id
from app.shared.repository import TenantScopedRepository


class CampaignRepository(TenantScopedRepository):
    async def create_draft(self, *, role_title: str, role_profile: dict[str, Any]) -> Campaign:
        # Campaigns are always born `draft` (lifecycle). Owned by this tenant.
        # (Domain-language name: a campaign is *created as a draft*, never just "created".)
        campaign = Campaign(
            id=new_id(),
            organization_id=self.tenant_id,
            role_title=role_title,
            role_profile=role_profile,
            status=CampaignStatus.DRAFT.value,
        )
        self.session.add(campaign)
        await self.session.flush()  # persist within the request's single transaction
        return campaign

    async def get(self, campaign_id: str) -> Campaign | None:
        """Fetch one campaign **owned by this tenant**. Returns None for a campaign
        that exists but belongs to another organization — isolation, not a 'maybe'."""
        stmt = self._scoped(
            select(Campaign).where(Campaign.id == campaign_id), Campaign.organization_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_for_tenant(self, *, limit: int, offset: int) -> Sequence[Campaign]:
        """This tenant's campaigns, newest first, one page at a time. The tenant
        filter goes through `_scoped`, so the list can never span organizations."""
        stmt = (
            self._scoped(select(Campaign), Campaign.organization_id)
            .order_by(Campaign.created_at.desc(), Campaign.id.desc())  # id = stable tiebreak
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def count_for_tenant(self) -> int:
        """How many campaigns this tenant has (for pagination). Also tenant-scoped."""
        stmt = self._scoped(select(func.count()).select_from(Campaign), Campaign.organization_id)
        result = await self.session.execute(stmt)
        return int(result.scalar_one())
