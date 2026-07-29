"""Review-queue read model — one purpose-built, tenant-scoped query (no N+1).

Stage, an ordering rank, and a "last activity" timestamp are derived in SQL (CASE) from
authoritative data — CandidateEvaluation status + submission, the latest Evaluation run,
and Invitation existence — so filtering, deterministic ordering, and pagination all happen
in the database rather than in Python over an over-fetched set. Nothing here is a stored
workflow column; the queue is always a projection of the real world.

Ordering rank (attention first; deterministic tie-break by recent activity then id):
    0 NEEDS_REVIEW/ESCALATE · 1 READY_FOR_EVALUATION · 2 NEEDS_REVIEW/MIXED
    3 AWAITING_INVITATION · 4 EVALUATED (decisive) · 5 AWAITING_CANDIDATE
"""

from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any

from sqlalchemy import Row, and_, case, func, or_, select

from app.modules.campaigns.models import Campaign
from app.modules.candidates.enums import EvaluationStatus
from app.modules.candidates.models import Candidate, CandidateEvaluation
from app.modules.decisions.models import HiringDecision
from app.modules.evaluations.models import Evaluation
from app.modules.invitations.models import Invitation
from app.modules.review.enums import QueueFilter, QueueStage
from app.shared.repository import TenantScopedRepository

_SUBMITTED = EvaluationStatus.SUBMITTED.value


@dataclass(frozen=True)
class _Exprs:
    stage: Any
    rank: Any
    activity: Any
    is_submitted: Any
    has_eval: Any
    has_inv: Any


class ReviewQueueRepository(TenantScopedRepository):
    # --- shared subqueries + derived expressions -------------------------------------- #

    def _latest_eval_subquery(self) -> Any:
        latest_rn = (
            select(
                Evaluation.candidate_evaluation_id.label("cid"),
                func.max(Evaluation.run_number).label("rn"),
            )
            .where(Evaluation.organization_id == self.tenant_id)
            .group_by(Evaluation.candidate_evaluation_id)
            .subquery("latest_rn")
        )
        return (
            select(
                Evaluation.candidate_evaluation_id.label("cid"),
                Evaluation.recommendation.label("recommendation"),
                Evaluation.confidence.label("confidence"),
                Evaluation.run_number.label("run_number"),
                Evaluation.created_at.label("eval_at"),
            )
            .join(
                latest_rn,
                and_(
                    Evaluation.candidate_evaluation_id == latest_rn.c.cid,
                    Evaluation.run_number == latest_rn.c.rn,
                ),
            )
            .where(Evaluation.organization_id == self.tenant_id)
            .subquery("le")
        )

    def _invitation_subquery(self) -> Any:
        return (
            select(
                Invitation.candidate_evaluation_id.label("cid"),
                func.max(Invitation.created_at).label("invited_at"),
                func.max(Invitation.accessed_at).label("accessed_at"),
            )
            .where(Invitation.organization_id == self.tenant_id)
            .group_by(Invitation.candidate_evaluation_id)
            .subquery("inv")
        )

    def _latest_decision_expr(self) -> Any:
        """The latest HUMAN decision for a row (badge only — never changes stage/order).
        A correlated scalar so it adds one column without risking row multiplication."""
        return (
            select(HiringDecision.decision)
            .where(
                HiringDecision.candidate_evaluation_id == CandidateEvaluation.id,
                HiringDecision.organization_id == self.tenant_id,
            )
            .order_by(HiringDecision.sequence_number.desc())
            .limit(1)
            .scalar_subquery()
        )

    def _exprs(self, le: Any, inv: Any) -> _Exprs:
        is_submitted = CandidateEvaluation.status == _SUBMITTED
        has_eval = le.c.recommendation.isnot(None)
        has_inv = inv.c.cid.isnot(None)

        stage = case(
            (and_(is_submitted, le.c.recommendation == "ESCALATE"), QueueStage.NEEDS_REVIEW.value),
            (and_(is_submitted, le.c.recommendation == "MIXED"), QueueStage.NEEDS_REVIEW.value),
            (and_(is_submitted, has_eval), QueueStage.EVALUATED.value),
            (is_submitted, QueueStage.READY_FOR_EVALUATION.value),
            (has_inv, QueueStage.AWAITING_CANDIDATE.value),
            else_=QueueStage.AWAITING_INVITATION.value,
        )
        rank = case(
            (and_(is_submitted, le.c.recommendation == "ESCALATE"), 0),
            (and_(is_submitted, ~has_eval), 1),
            (and_(is_submitted, le.c.recommendation == "MIXED"), 2),
            (and_(~is_submitted, ~has_inv), 3),
            (and_(is_submitted, has_eval), 4),
            else_=5,
        )
        activity = case(
            (le.c.eval_at.isnot(None), le.c.eval_at),
            (CandidateEvaluation.submitted_at.isnot(None), CandidateEvaluation.submitted_at),
            (inv.c.accessed_at.isnot(None), inv.c.accessed_at),
            (inv.c.invited_at.isnot(None), inv.c.invited_at),
            else_=CandidateEvaluation.created_at,
        )
        return _Exprs(stage, rank, activity, is_submitted, has_eval, has_inv)

    @staticmethod
    def _filter_condition(queue_filter: QueueFilter, e: _Exprs) -> Any | None:
        if queue_filter == QueueFilter.NEEDS_ATTENTION:
            return e.rank <= 3
        if queue_filter == QueueFilter.READY:
            return and_(e.is_submitted, ~e.has_eval)
        if queue_filter == QueueFilter.WAITING:
            return and_(~e.is_submitted, e.has_inv)
        if queue_filter == QueueFilter.COMPLETED:
            return and_(e.is_submitted, e.has_eval, e.stage == QueueStage.EVALUATED.value)
        return None

    def _conditions(
        self, e: _Exprs, *, queue_filter: QueueFilter, campaign_id: str | None, search: str | None
    ) -> list[Any]:
        conditions: list[Any] = [CandidateEvaluation.organization_id == self.tenant_id]
        if campaign_id:
            conditions.append(CandidateEvaluation.campaign_id == campaign_id)
        if search and search.strip():
            # Recruiters recall the person OR the role ("that Backend Engineer") — match both.
            pattern = f"%{search.strip()}%"
            conditions.append(
                or_(Candidate.name.ilike(pattern), Campaign.role_title.ilike(pattern))
            )
        fc = self._filter_condition(queue_filter, e)
        if fc is not None:
            conditions.append(fc)
        return conditions

    # --- public reads ----------------------------------------------------------------- #

    async def fetch_page(
        self,
        *,
        queue_filter: QueueFilter,
        campaign_id: str | None,
        search: str | None,
        limit: int,
        offset: int,
    ) -> tuple[Sequence[Row[Any]], int]:
        le, inv = self._latest_eval_subquery(), self._invitation_subquery()
        e = self._exprs(le, inv)
        conditions = self._conditions(
            e, queue_filter=queue_filter, campaign_id=campaign_id, search=search
        )

        def joined(stmt: Any) -> Any:
            return (
                stmt.join(Candidate, CandidateEvaluation.candidate_id == Candidate.id)
                .join(Campaign, CandidateEvaluation.campaign_id == Campaign.id)
                .outerjoin(le, le.c.cid == CandidateEvaluation.id)
                .outerjoin(inv, inv.c.cid == CandidateEvaluation.id)
            )

        total = int(
            (
                await self.session.execute(
                    joined(select(func.count()).select_from(CandidateEvaluation)).where(*conditions)
                )
            ).scalar_one()
        )

        page = (
            joined(
                select(
                    CandidateEvaluation.id.label("candidate_evaluation_id"),
                    CandidateEvaluation.campaign_id,
                    Candidate.name.label("candidate_name"),
                    Candidate.email.label("candidate_email"),
                    Campaign.role_title,
                    le.c.recommendation,
                    le.c.confidence,
                    le.c.run_number,
                    e.stage.label("stage"),
                    e.activity.label("last_activity_at"),
                    self._latest_decision_expr().label("decision"),
                )
            )
            .where(*conditions)
            .order_by(e.rank.asc(), e.activity.desc(), CandidateEvaluation.id.desc())
            .limit(limit)
            .offset(offset)
        )
        rows = (await self.session.execute(page)).all()
        return rows, total

    async def stage_counts(self) -> dict[str, int]:
        """Whole-queue counts per derived stage (no filter/search) for the summary tiles."""
        le, inv = self._latest_eval_subquery(), self._invitation_subquery()
        e = self._exprs(le, inv)
        stmt = (
            select(e.stage.label("stage"), func.count().label("cnt"))
            .select_from(CandidateEvaluation)
            .outerjoin(le, le.c.cid == CandidateEvaluation.id)
            .outerjoin(inv, inv.c.cid == CandidateEvaluation.id)
            .where(CandidateEvaluation.organization_id == self.tenant_id)
            .group_by(e.stage)
        )
        result = await self.session.execute(stmt)
        return {row.stage: int(row.cnt) for row in result.all()}
