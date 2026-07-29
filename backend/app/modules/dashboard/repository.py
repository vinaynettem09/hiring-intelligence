"""Dashboard read model. A `TenantScopedRepository`, so every count and list is
filtered to the caller's organization (INV-000) — one org can never see or count
another's campaigns or candidates. Read-only: it reads across the campaign and
candidate tables but owns no writes.
"""

from collections.abc import Sequence

from sqlalchemy import Select, func, select

from app.modules.campaigns.enums import CampaignStatus
from app.modules.campaigns.models import Campaign
from app.modules.candidates.models import Candidate, CandidateEvaluation
from app.shared.repository import TenantScopedRepository


class DashboardRepository(TenantScopedRepository):
    async def _count(self, stmt: Select[tuple[int]]) -> int:
        result = await self.session.execute(stmt)
        return int(result.scalar_one())

    async def count_campaigns(self, *, status: str | None = None) -> int:
        stmt = self._scoped(select(func.count()).select_from(Campaign), Campaign.organization_id)
        if status is not None:
            stmt = stmt.where(Campaign.status == status)
        return await self._count(stmt)

    async def count_candidates(self) -> int:
        return await self._count(
            self._scoped(select(func.count()).select_from(Candidate), Candidate.organization_id)
        )

    async def count_candidates_missing_resume(self) -> int:
        stmt = self._scoped(
            select(func.count()).select_from(Candidate), Candidate.organization_id
        ).where(Candidate.resume_object_key.is_(None))
        return await self._count(stmt)

    async def count_active_campaigns_without_candidates(self) -> int:
        used = self._scoped(
            select(CandidateEvaluation.campaign_id), CandidateEvaluation.organization_id
        ).distinct()
        stmt = self._scoped(
            select(func.count()).select_from(Campaign), Campaign.organization_id
        ).where(Campaign.status == CampaignStatus.ACTIVE.value, Campaign.id.not_in(used))
        return await self._count(stmt)

    async def recent_campaigns(self, limit: int) -> Sequence[Campaign]:
        stmt = (
            self._scoped(select(Campaign), Campaign.organization_id)
            .order_by(Campaign.created_at.desc(), Campaign.id.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def recent_candidates(
        self, limit: int
    ) -> Sequence[tuple[CandidateEvaluation, Candidate, Campaign]]:
        stmt = (
            self._scoped(
                select(CandidateEvaluation, Candidate, Campaign),
                CandidateEvaluation.organization_id,
            )
            .join(Candidate, CandidateEvaluation.candidate_id == Candidate.id)
            .join(Campaign, CandidateEvaluation.campaign_id == Campaign.id)
            .order_by(CandidateEvaluation.created_at.desc(), CandidateEvaluation.id.desc())
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return [(row[0], row[1], row[2]) for row in result.all()]
