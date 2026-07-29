"""Persistence for candidate intake. Both aggregates are tenant-scoped: every read
routes through `_scoped`, so a repository can never reach another org's candidates or
evaluations (INV-000). Repositories persist (`add`/`flush`); they never commit.
"""

from collections.abc import Sequence

from sqlalchemy import func, select

from app.modules.candidates.enums import EvaluationStatus
from app.modules.candidates.models import Candidate, CandidateEvaluation
from app.shared.ids import new_id
from app.shared.repository import TenantScopedRepository


class CandidateRepository(TenantScopedRepository):
    async def get_by_email(self, email: str) -> Candidate | None:
        """Find this org's identity record for a person (the find-or-create seam).
        Tenant-scoped: another org's candidate with the same email is invisible."""
        stmt = self._scoped(
            select(Candidate).where(Candidate.email == email), Candidate.organization_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get(self, candidate_id: str) -> Candidate | None:
        stmt = self._scoped(
            select(Candidate).where(Candidate.id == candidate_id), Candidate.organization_id
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, *, name: str, email: str, resume_object_key: str | None) -> Candidate:
        candidate = Candidate(
            id=new_id(),
            organization_id=self.tenant_id,
            name=name,
            email=email,
            resume_object_key=resume_object_key,
        )
        self.session.add(candidate)
        await self.session.flush()
        return candidate


class CandidateEvaluationRepository(TenantScopedRepository):
    async def get_for_candidate_in_campaign(
        self, *, campaign_id: str, candidate_id: str
    ) -> CandidateEvaluation | None:
        """Used to enforce one evaluation per (campaign, candidate). Tenant-scoped."""
        stmt = self._scoped(
            select(CandidateEvaluation).where(
                CandidateEvaluation.campaign_id == campaign_id,
                CandidateEvaluation.candidate_id == candidate_id,
            ),
            CandidateEvaluation.organization_id,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get(self, evaluation_id: str) -> CandidateEvaluation | None:
        stmt = self._scoped(
            select(CandidateEvaluation).where(CandidateEvaluation.id == evaluation_id),
            CandidateEvaluation.organization_id,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, *, campaign_id: str, candidate_id: str) -> CandidateEvaluation:
        # Born `invited` — the entry point of the work-sample lifecycle.
        evaluation = CandidateEvaluation(
            id=new_id(),
            organization_id=self.tenant_id,
            campaign_id=campaign_id,
            candidate_id=candidate_id,
            status=EvaluationStatus.INVITED.value,
        )
        self.session.add(evaluation)
        await self.session.flush()
        return evaluation

    async def list_roster(
        self, *, campaign_id: str, limit: int, offset: int
    ) -> Sequence[tuple[CandidateEvaluation, Candidate]]:
        """The campaign's roster: each evaluation with its candidate (recruiter-facing,
        so PII is joined here — this is NOT the AI's view). Tenant-scoped, newest first."""
        stmt = (
            self._scoped(
                select(CandidateEvaluation, Candidate), CandidateEvaluation.organization_id
            )
            .join(Candidate, CandidateEvaluation.candidate_id == Candidate.id)
            .where(CandidateEvaluation.campaign_id == campaign_id)
            .order_by(CandidateEvaluation.created_at.desc(), CandidateEvaluation.id.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.session.execute(stmt)
        return [(row[0], row[1]) for row in result.all()]

    async def count_for_campaign(self, campaign_id: str) -> int:
        stmt = self._scoped(
            select(func.count()).select_from(CandidateEvaluation),
            CandidateEvaluation.organization_id,
        ).where(CandidateEvaluation.campaign_id == campaign_id)
        result = await self.session.execute(stmt)
        return int(result.scalar_one())

    async def count_missing_resume(self, campaign_id: str) -> int:
        """How many roster candidates have no résumé pointer — a 'needs attention' signal."""
        stmt = (
            self._scoped(select(func.count()), CandidateEvaluation.organization_id)
            .select_from(CandidateEvaluation)
            .join(Candidate, CandidateEvaluation.candidate_id == Candidate.id)
            .where(
                CandidateEvaluation.campaign_id == campaign_id,
                Candidate.resume_object_key.is_(None),
            )
        )
        result = await self.session.execute(stmt)
        return int(result.scalar_one())
