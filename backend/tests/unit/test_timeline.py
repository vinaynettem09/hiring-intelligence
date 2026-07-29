"""Hiring-process timeline (Story 6.3) — the exportable audit trail.

Proves the trail is assembled from authoritative records across the whole lifecycle,
ordered chronologically, tenant-scoped, and PII-minimal (a decision rationale is never
inlined). No new business logic — pure read assembly.
"""

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from support import submitted_evaluation

from app.modules.decisions.enums import DecisionType
from app.modules.decisions.schemas import RecordDecisionRequest
from app.modules.decisions.service import DecisionService
from app.modules.evaluations.repository import EvaluationRepository
from app.modules.identity.models import User
from app.modules.intelligence.service import IntelligenceService
from app.modules.timeline.enums import TimelineEventKind
from app.modules.timeline.service import TimelineService
from app.shared.context import AuthContext
from app.shared.errors import NotFoundError


async def _founder_id(session: AsyncSession, tenant: str) -> str:
    user = (
        (await session.execute(select(User).where(User.organization_id == tenant)))
        .scalars()
        .first()
    )
    assert user is not None
    return user.id


async def _full_lifecycle(session: AsyncSession, **kwargs: object) -> tuple[str, str]:
    """A submitted evaluation + a persisted AI run + a recorded human decision (rationale)."""
    setup = await submitted_evaluation(session, **kwargs)  # type: ignore[arg-type]
    outcome = await IntelligenceService(session, setup.tenant).evaluate(setup.evaluation_id)
    assert outcome.proposal is not None
    ev = await EvaluationRepository(session, setup.tenant).create_evaluation(
        candidate_evaluation_id=setup.evaluation_id,
        run_number=1,
        idempotency_key=None,
        proposal=outcome.proposal,
        input_fingerprint=outcome.input_fingerprint,
        usage=outcome.usage,
    )
    user_id = await _founder_id(session, setup.tenant)
    await DecisionService(
        session,
        AuthContext(
            user_id=user_id, organization_id=setup.tenant, role="recruiter", correlation_id="c"
        ),
    ).record(
        setup.evaluation_id,
        RecordDecisionRequest(
            decision=DecisionType.ADVANCE, rationale="PRIVATE NOTE", evaluation_id=ev.id
        ),
    )
    return setup.tenant, setup.evaluation_id


async def test_timeline_assembles_the_full_lifecycle(session: AsyncSession) -> None:
    tenant, eval_id = await _full_lifecycle(session)
    timeline = await TimelineService(session, tenant).get_timeline(eval_id)

    kinds = {e.kind for e in timeline.entries}
    assert TimelineEventKind.INVITATION_SENT in kinds
    assert TimelineEventKind.CONSENT_GRANTED in kinds
    assert TimelineEventKind.WORK_SAMPLE_SUBMITTED in kinds
    assert TimelineEventKind.EVALUATION_GENERATED in kinds
    assert TimelineEventKind.DECISION_RECORDED in kinds

    assert timeline.candidate_name == "Ada Lovelace"
    assert timeline.role_title == "Data Engineer"


async def test_timeline_is_chronological(session: AsyncSession) -> None:
    tenant, eval_id = await _full_lifecycle(session)
    timeline = await TimelineService(session, tenant).get_timeline(eval_id)
    ats = [e.at for e in timeline.entries]
    assert ats == sorted(ats)  # oldest first
    # The lifecycle order holds: consent/submission precede evaluation, which precedes the decision.
    at_of = {e.kind: e.at for e in timeline.entries}
    assert (
        at_of[TimelineEventKind.WORK_SAMPLE_SUBMITTED]
        <= at_of[TimelineEventKind.EVALUATION_GENERATED]
    )
    assert (
        at_of[TimelineEventKind.EVALUATION_GENERATED] <= at_of[TimelineEventKind.DECISION_RECORDED]
    )


async def test_timeline_does_not_leak_decision_rationale(session: AsyncSession) -> None:
    tenant, eval_id = await _full_lifecycle(session)
    timeline = await TimelineService(session, tenant).get_timeline(eval_id)
    # The free-text rationale is recorded on the decision but never inlined in the audit trail.
    assert all("PRIVATE NOTE" not in e.summary for e in timeline.entries)
    decision_entry = next(
        e for e in timeline.entries if e.kind == TimelineEventKind.DECISION_RECORDED
    )
    assert "with rationale" in decision_entry.summary  # presence noted, content withheld
    assert decision_entry.actor == "founder@acme.com"


async def test_timeline_is_tenant_scoped(session: AsyncSession) -> None:
    _, a_eval = await _full_lifecycle(session, org="Acme", user_email="a@acme.com")
    b = await submitted_evaluation(session, org="Globex", user_email="b@globex.com")
    with pytest.raises(NotFoundError) as exc:
        await TimelineService(session, b.tenant).get_timeline(a_eval)
    assert exc.value.code == "CANDIDATE_EVALUATION_NOT_FOUND"
