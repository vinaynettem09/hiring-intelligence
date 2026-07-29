"""Human decision workflow (Story 6.2).

Proves the boundary: AI proposes, a human decides, the system records both separately.
Decisions are append-only, reference (never mutate) the immutable Evaluation, may be made
with or without an AI run, are authorized + tenant-scoped, and are audited.
"""

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from support import submitted_evaluation

from app.modules.audit.models import AuditEvent
from app.modules.decisions.enums import DecisionType
from app.modules.decisions.schemas import RecordDecisionRequest
from app.modules.decisions.service import DecisionService
from app.modules.evaluations.repository import EvaluationRepository
from app.modules.identity.models import User
from app.modules.intelligence.service import IntelligenceService
from app.shared.context import AuthContext
from app.shared.errors import AuthorizationError, NotFoundError


def _auth(tenant: str, user_id: str, *, role: str = "recruiter") -> AuthContext:
    return AuthContext(user_id=user_id, organization_id=tenant, role=role, correlation_id="c")


async def _founder_id(session: AsyncSession, tenant: str) -> str:
    user = (
        (await session.execute(select(User).where(User.organization_id == tenant)))
        .scalars()
        .first()
    )
    assert user is not None
    return user.id


async def _persist_evaluation(session: AsyncSession, tenant: str, eval_id: str) -> str:
    outcome = await IntelligenceService(session, tenant).evaluate(eval_id)
    assert outcome.proposal is not None
    ev = await EvaluationRepository(session, tenant).create_evaluation(
        candidate_evaluation_id=eval_id,
        run_number=1,
        idempotency_key=None,
        proposal=outcome.proposal,
        input_fingerprint=outcome.input_fingerprint,
        usage=outcome.usage,
    )
    return ev.id


async def test_record_decision_referencing_an_evaluation(session: AsyncSession) -> None:
    setup = await submitted_evaluation(session)
    evaluation_id = await _persist_evaluation(session, setup.tenant, setup.evaluation_id)
    user_id = await _founder_id(session, setup.tenant)
    service = DecisionService(session, _auth(setup.tenant, user_id))

    view = await service.record(
        setup.evaluation_id,
        RecordDecisionRequest(
            decision=DecisionType.ADVANCE,
            rationale="Strong SQL evidence.",
            evaluation_id=evaluation_id,
        ),
    )
    assert view.decision == DecisionType.ADVANCE
    assert view.decided_by_email == "founder@acme.com"
    assert view.informed_by_run_number == 1  # references the run that informed it
    assert view.rationale == "Strong SQL evidence."


async def test_decision_can_be_made_without_an_evaluation(session: AsyncSession) -> None:
    # AI is advisory, never a gate — a human may decide with no evaluation run.
    setup = await submitted_evaluation(session)
    user_id = await _founder_id(session, setup.tenant)
    view = await DecisionService(session, _auth(setup.tenant, user_id)).record(
        setup.evaluation_id, RecordDecisionRequest(decision=DecisionType.HOLD)
    )
    assert view.decision == DecisionType.HOLD
    assert view.informed_by_run_number is None


async def test_decisions_are_append_only_history(session: AsyncSession) -> None:
    setup = await submitted_evaluation(session)
    user_id = await _founder_id(session, setup.tenant)
    service = DecisionService(session, _auth(setup.tenant, user_id))

    await service.record(setup.evaluation_id, RecordDecisionRequest(decision=DecisionType.HOLD))
    await service.record(setup.evaluation_id, RecordDecisionRequest(decision=DecisionType.ADVANCE))

    history = await service.get_history(setup.evaluation_id)
    assert len(history.decisions) == 2  # nothing overwritten
    assert history.latest is not None
    assert history.latest.decision == DecisionType.ADVANCE  # newest is current
    assert [d.decision for d in history.decisions] == [DecisionType.ADVANCE, DecisionType.HOLD]


async def test_recording_a_decision_does_not_mutate_the_evaluation(session: AsyncSession) -> None:
    setup = await submitted_evaluation(session)
    evaluation_id = await _persist_evaluation(session, setup.tenant, setup.evaluation_id)
    user_id = await _founder_id(session, setup.tenant)

    before = await EvaluationRepository(session, setup.tenant).get_evaluation(evaluation_id)
    assert before is not None
    original_recommendation = before.recommendation

    await DecisionService(session, _auth(setup.tenant, user_id)).record(
        setup.evaluation_id,
        RecordDecisionRequest(decision=DecisionType.DECLINE, evaluation_id=evaluation_id),
    )
    after = await EvaluationRepository(session, setup.tenant).get_evaluation(evaluation_id)
    assert after is not None
    assert after.recommendation == original_recommendation  # evaluation is untouched


async def test_unknown_evaluation_reference_is_rejected(session: AsyncSession) -> None:
    setup = await submitted_evaluation(session)
    user_id = await _founder_id(session, setup.tenant)
    with pytest.raises(NotFoundError) as exc:
        await DecisionService(session, _auth(setup.tenant, user_id)).record(
            setup.evaluation_id,
            RecordDecisionRequest(decision=DecisionType.ADVANCE, evaluation_id="does-not-exist"),
        )
    assert exc.value.code == "EVALUATION_NOT_FOUND"


async def test_disallowed_role_cannot_decide(session: AsyncSession) -> None:
    setup = await submitted_evaluation(session)
    user_id = await _founder_id(session, setup.tenant)
    with pytest.raises(AuthorizationError) as exc:
        await DecisionService(session, _auth(setup.tenant, user_id, role="observer")).record(
            setup.evaluation_id, RecordDecisionRequest(decision=DecisionType.ADVANCE)
        )
    assert exc.value.code == "DECISION_FORBIDDEN"


async def test_decision_is_tenant_scoped(session: AsyncSession) -> None:
    a = await submitted_evaluation(session, org="Acme", user_email="a@acme.com")
    b = await submitted_evaluation(session, org="Globex", user_email="b@globex.com")
    b_user = await _founder_id(session, b.tenant)
    # Org B cannot decide on Org A's candidate evaluation — it reads as absent (404).
    with pytest.raises(NotFoundError) as exc:
        await DecisionService(session, _auth(b.tenant, b_user)).record(
            a.evaluation_id, RecordDecisionRequest(decision=DecisionType.ADVANCE)
        )
    assert exc.value.code == "CANDIDATE_EVALUATION_NOT_FOUND"


async def test_decision_is_audited(session: AsyncSession) -> None:
    setup = await submitted_evaluation(session)
    user_id = await _founder_id(session, setup.tenant)
    await DecisionService(session, _auth(setup.tenant, user_id)).record(
        setup.evaluation_id,
        RecordDecisionRequest(decision=DecisionType.ADVANCE, rationale="secret note"),
    )
    events = (
        (await session.execute(select(AuditEvent).where(AuditEvent.action == "decision.recorded")))
        .scalars()
        .all()
    )
    assert len(events) == 1
    details = events[0].details
    assert details is not None
    # PII-safe: the free-text rationale is never written to the audit log.
    assert "secret note" not in str(details)
    assert details["decision"] == "ADVANCE"
