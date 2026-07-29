"""Roster evaluation-status enrichment (Story 5.4B entry point).

The roster must know whether each candidate already has an evaluation — so the UI can show
'Generate evaluation' vs. 'View evaluation' without an N+1 of reads — and it must stay
tenant-scoped (one org's runs can never surface on another org's roster).
"""

from sqlalchemy.ext.asyncio import AsyncSession
from support import submitted_evaluation

from app.modules.candidates.service import CandidateService
from app.modules.evaluations.repository import EvaluationRepository
from app.modules.intelligence.service import IntelligenceService


async def _persist_run(session: AsyncSession, tenant: str, evaluation_id: str, run: int) -> None:
    outcome = await IntelligenceService(session, tenant).evaluate(evaluation_id)
    assert outcome.proposal is not None
    await EvaluationRepository(session, tenant).create_evaluation(
        candidate_evaluation_id=evaluation_id,
        run_number=run,
        idempotency_key=None,
        proposal=outcome.proposal,
        input_fingerprint=outcome.input_fingerprint,
        usage=outcome.usage,
    )


async def test_roster_shows_no_evaluation_before_generation(session: AsyncSession) -> None:
    setup = await submitted_evaluation(session)
    roster = await CandidateService(session, setup.tenant).list_roster(
        setup.campaign_id, limit=50, offset=0
    )
    entry = next(e for e in roster.items if e.evaluation_id == setup.evaluation_id)
    assert entry.has_evaluation is False
    assert entry.latest_recommendation is None
    assert entry.latest_run_number is None


async def test_roster_reflects_latest_run_after_generation(session: AsyncSession) -> None:
    setup = await submitted_evaluation(session)
    await _persist_run(session, setup.tenant, setup.evaluation_id, run=1)
    await _persist_run(session, setup.tenant, setup.evaluation_id, run=2)  # a rerun

    roster = await CandidateService(session, setup.tenant).list_roster(
        setup.campaign_id, limit=50, offset=0
    )
    entry = next(e for e in roster.items if e.evaluation_id == setup.evaluation_id)
    assert entry.has_evaluation is True
    assert entry.latest_recommendation == "PROCEED"  # deterministic mock
    assert entry.latest_run_number == 2  # the LATEST run, not the first


async def test_latest_lookup_is_tenant_scoped(session: AsyncSession) -> None:
    a = await submitted_evaluation(session, org="Acme", user_email="a@acme.com")
    await _persist_run(session, a.tenant, a.evaluation_id, run=1)
    b = await submitted_evaluation(session, org="Globex", user_email="b@globex.com")

    # Org B's repository must not see Org A's run, even asked for A's id directly.
    leaked = await EvaluationRepository(session, b.tenant).latest_for_candidate_evaluations(
        [a.evaluation_id]
    )
    assert leaked == {}
