"""HiringDecision persistence — **append-only**, tenant-scoped.

Exposes create + reads only (no update/delete): a decision, once made, is a historical
fact; a change of mind is a new row. Reads join the deciding user (for the accountable
email) and the referenced Evaluation (for its run number) in one query — no N+1.
"""

from collections.abc import Sequence
from typing import Any

from sqlalchemy import Row, func, select

from app.modules.decisions.models import HiringDecision
from app.modules.evaluations.models import Evaluation
from app.modules.identity.models import User
from app.shared.ids import new_id
from app.shared.repository import TenantScopedRepository


class DecisionRepository(TenantScopedRepository):
    async def create(
        self,
        *,
        candidate_evaluation_id: str,
        evaluation_id: str | None,
        decision: str,
        rationale: str | None,
        decided_by_user_id: str,
        decided_at: Any,
    ) -> HiringDecision:
        record = HiringDecision(
            id=new_id(),
            organization_id=self.tenant_id,
            candidate_evaluation_id=candidate_evaluation_id,
            evaluation_id=evaluation_id,
            sequence_number=await self._next_sequence(candidate_evaluation_id),
            decision=decision,
            rationale=rationale,
            decided_by_user_id=decided_by_user_id,
            decided_at=decided_at,
        )
        self.session.add(record)
        await self.session.flush()
        return record

    async def _next_sequence(self, candidate_evaluation_id: str) -> int:
        stmt = self._scoped(
            select(func.max(HiringDecision.sequence_number)).where(
                HiringDecision.candidate_evaluation_id == candidate_evaluation_id
            ),
            HiringDecision.organization_id,
        )
        current = (await self.session.execute(stmt)).scalar_one_or_none()
        return (current or 0) + 1

    async def list_for_candidate_evaluation(
        self, candidate_evaluation_id: str
    ) -> Sequence[Row[Any]]:
        """Every decision (newest first) with the decider's email + the referenced run
        number. Tenant-scoped."""
        stmt = (
            self._scoped(
                select(HiringDecision, User.email, Evaluation.run_number),
                HiringDecision.organization_id,
            )
            .join(User, HiringDecision.decided_by_user_id == User.id)
            .outerjoin(Evaluation, HiringDecision.evaluation_id == Evaluation.id)
            .where(HiringDecision.candidate_evaluation_id == candidate_evaluation_id)
            .order_by(HiringDecision.sequence_number.desc())
        )
        result = await self.session.execute(stmt)
        return result.all()
