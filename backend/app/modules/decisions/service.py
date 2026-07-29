"""Decision service — the accountable human act.

Records a HiringDecision against a candidate evaluation. The AI recommendation is at most
an *input* the recruiter references (`evaluation_id`); it is never the mechanism. Decisions
are append-only, tenant-scoped, and made by a real authenticated user. The Evaluation is
referenced, never modified.
"""

from datetime import UTC, datetime
from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.audit.service import AuditService
from app.modules.candidates.repository import CandidateEvaluationRepository
from app.modules.decisions.enums import DecisionType
from app.modules.decisions.repository import DecisionRepository
from app.modules.decisions.schemas import (
    DecisionHistoryResponse,
    DecisionView,
    RecordDecisionRequest,
)
from app.modules.evaluations.repository import EvaluationRepository
from app.modules.identity.enums import UserRole
from app.shared.context import AuthContext
from app.shared.errors import AuthorizationError, NotFoundError

# Who may record a hiring decision (same authority that runs/views evaluations).
_ALLOWED_ROLES = frozenset(
    {UserRole.ADMIN.value, UserRole.RECRUITER.value, UserRole.HIRING_MANAGER.value}
)


class DecisionService:
    def __init__(self, session: AsyncSession, auth: AuthContext) -> None:
        self._session = session
        self._auth = auth
        self._tenant_id = auth.organization_id
        self._repo = DecisionRepository(session, self._tenant_id)

    async def record(
        self, candidate_evaluation_id: str, request: RecordDecisionRequest
    ) -> DecisionView:
        self._authorize()
        await self._require_candidate_evaluation(candidate_evaluation_id)

        # If the recruiter is deciding against a specific AI run, it must belong to THIS
        # candidate evaluation (and tenant). A decision without a run is allowed (AI advisory).
        if request.evaluation_id is not None:
            evaluation = await EvaluationRepository(self._session, self._tenant_id).get_evaluation(
                request.evaluation_id
            )
            if evaluation is None or evaluation.candidate_evaluation_id != candidate_evaluation_id:
                raise NotFoundError(
                    "Evaluation run not found for this candidate evaluation.",
                    code="EVALUATION_NOT_FOUND",
                )

        await self._repo.create(
            candidate_evaluation_id=candidate_evaluation_id,
            evaluation_id=request.evaluation_id,
            decision=request.decision.value,
            rationale=request.rationale,
            decided_by_user_id=self._auth.user_id,
            decided_at=datetime.now(UTC),
        )
        await AuditService(self._session).record(
            organization_id=self._tenant_id,
            actor_type="recruiter",
            actor_user_id=self._auth.user_id,
            action="decision.recorded",
            target_type="candidate_evaluation",
            target_id=candidate_evaluation_id,
            # PII-safe: the decision + what informed it, never the free-text rationale.
            details={
                "decision": request.decision.value,
                "evaluation_id": request.evaluation_id,
                "rationale_present": request.rationale is not None,
            },
        )
        # Return the just-recorded decision, enriched (decider email + run number).
        rows = await self._repo.list_for_candidate_evaluation(candidate_evaluation_id)
        return _to_view(rows[0])

    async def get_history(self, candidate_evaluation_id: str) -> DecisionHistoryResponse:
        self._authorize()
        await self._require_candidate_evaluation(candidate_evaluation_id)
        views = [
            _to_view(row)
            for row in await self._repo.list_for_candidate_evaluation(candidate_evaluation_id)
        ]
        return DecisionHistoryResponse(
            candidate_evaluation_id=candidate_evaluation_id,
            latest=views[0] if views else None,
            decisions=views,
        )

    def _authorize(self) -> None:
        if self._auth.role not in _ALLOWED_ROLES:
            raise AuthorizationError(
                "You are not allowed to record hiring decisions.", code="DECISION_FORBIDDEN"
            )

    async def _require_candidate_evaluation(self, candidate_evaluation_id: str) -> None:
        # Tenant-scoped: another org's candidate evaluation reads as absent (404, never 403).
        owned = await CandidateEvaluationRepository(self._session, self._tenant_id).get(
            candidate_evaluation_id
        )
        if owned is None:
            raise NotFoundError(
                "Candidate evaluation not found.", code="CANDIDATE_EVALUATION_NOT_FOUND"
            )


def _to_view(row: Any) -> DecisionView:
    decision, email, run_number = row[0], row[1], row[2]
    return DecisionView(
        id=decision.id,
        decision=DecisionType(decision.decision),
        rationale=decision.rationale,
        decided_by_email=email,
        decided_at=_utc(decision.decided_at),
        informed_by_run_number=run_number,
        created_at=_utc(decision.created_at),
    )


def _utc(value: datetime) -> datetime:
    return value if value.tzinfo is not None else value.replace(tzinfo=UTC)
