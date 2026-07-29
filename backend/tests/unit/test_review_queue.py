"""Review-queue read model (Story 6.1) — derivation, attention, ordering, filters,
pagination, search, and tenant isolation.

Because this exercises a READ MODEL, the domain rows are constructed directly in the exact
states the queue must classify (the write flows have their own tests). Evaluations are
persisted through the real repository so recommendation/confidence are authoritative.
"""

from datetime import UTC, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.campaigns.models import Campaign
from app.modules.candidates.models import Candidate, CandidateEvaluation
from app.modules.decisions.models import HiringDecision
from app.modules.evaluations.repository import EvaluationRepository
from app.modules.identity.schemas import SignupRequest
from app.modules.identity.service import IdentityService
from app.modules.intelligence.enums import EscalationReason, RecommendationProposal
from app.modules.intelligence.schemas import (
    EvaluationProposal,
    EvidenceCoverage,
    Provenance,
)
from app.modules.invitations.models import Invitation
from app.modules.review.enums import QueueFilter, QueueStage
from app.modules.review.service import ReviewQueueService
from app.shared.ids import new_id


async def _org(session: AsyncSession, name: str, email: str) -> str:
    signup = await IdentityService(session).signup(
        SignupRequest(organization_name=name, email=email, password="password123")
    )
    return signup.organization.id


async def _campaign(session: AsyncSession, tenant: str, role: str = "Data Engineer") -> str:
    cid = new_id()
    session.add(
        Campaign(
            id=cid,
            organization_id=tenant,
            role_title=role,
            role_profile={"competencies": [{"name": "SQL"}], "bar": "senior"},
            status="active",
        )
    )
    await session.flush()
    return cid


async def _cand_eval(
    session: AsyncSession,
    tenant: str,
    campaign_id: str,
    *,
    name: str,
    email: str,
    submitted: bool = False,
) -> str:
    candidate_id, eval_id = new_id(), new_id()
    session.add(Candidate(id=candidate_id, organization_id=tenant, name=name, email=email))
    session.add(
        CandidateEvaluation(
            id=eval_id,
            organization_id=tenant,
            campaign_id=campaign_id,
            candidate_id=candidate_id,
            status="submitted" if submitted else "invited",
            submitted_at=datetime.now(UTC) if submitted else None,
        )
    )
    await session.flush()
    return eval_id


async def _invite(session: AsyncSession, tenant: str, eval_id: str) -> None:
    session.add(
        Invitation(
            id=new_id(),
            organization_id=tenant,
            candidate_evaluation_id=eval_id,
            token_hash=new_id(),
            expires_at=datetime.now(UTC) + timedelta(days=1),
        )
    )
    await session.flush()


def _proposal(recommendation: RecommendationProposal, confidence: float) -> EvaluationProposal:
    return EvaluationProposal(
        recommendation=recommendation,
        confidence=confidence,
        confidence_rationale="t",
        escalation_reason=(
            EscalationReason.INSUFFICIENT_EVIDENCE
            if recommendation == RecommendationProposal.ESCALATE
            else None
        ),
        competency_assessments=(),
        strengths=(),
        concerns=(),
        evidence_coverage=EvidenceCoverage(
            competencies_total=1, competencies_assessed=1, tasks_total=1, tasks_with_evidence=1
        ),
        provenance=Provenance(
            provider="mock",
            model="deterministic-mock",
            model_version="v1",
            prompt_version="eval-prompt-v3",
            input_schema_version="eval-input-v1",
            output_schema_version="eval-proposal-v1",
            confidence_algorithm_version="confidence-v2",
            generated_at=datetime(2026, 1, 1, tzinfo=UTC),
        ),
    )


async def _evaluate(
    session: AsyncSession, tenant: str, eval_id: str, recommendation: str, confidence: float
) -> None:
    await EvaluationRepository(session, tenant).create_evaluation(
        candidate_evaluation_id=eval_id,
        run_number=1,
        idempotency_key=None,
        proposal=_proposal(RecommendationProposal(recommendation), confidence),
        input_fingerprint="sha256:x",
    )


async def _one_of_each(session: AsyncSession) -> tuple[str, str, dict[str, str]]:
    """Build one org/campaign with one candidate evaluation in each queue stage."""
    tenant = await _org(session, "Acme", "founder@acme.com")
    campaign = await _campaign(session, tenant)
    ids: dict[str, str] = {}

    ids["awaiting_invitation"] = await _cand_eval(
        session, tenant, campaign, name="No Invite", email="noinvite@x.com"
    )

    awaiting = await _cand_eval(session, tenant, campaign, name="Waiting Cand", email="w@x.com")
    await _invite(session, tenant, awaiting)
    ids["awaiting_candidate"] = awaiting

    ids["ready"] = await _cand_eval(
        session, tenant, campaign, name="Ready Cand", email="r@x.com", submitted=True
    )

    evaluated = await _cand_eval(
        session, tenant, campaign, name="Done Cand", email="d@x.com", submitted=True
    )
    await _evaluate(session, tenant, evaluated, "PROCEED", 0.9)
    ids["evaluated"] = evaluated

    escalate = await _cand_eval(
        session, tenant, campaign, name="Escalate Cand", email="e@x.com", submitted=True
    )
    await _evaluate(session, tenant, escalate, "ESCALATE", 0.2)
    ids["escalate"] = escalate

    mixed = await _cand_eval(
        session, tenant, campaign, name="Mixed Cand", email="m@x.com", submitted=True
    )
    await _evaluate(session, tenant, mixed, "MIXED", 0.5)
    ids["mixed"] = mixed

    return tenant, campaign, ids


# --- derivation + attention --------------------------------------------------------- #


async def test_stage_derivation_and_attention(session: AsyncSession) -> None:
    tenant, _, ids = await _one_of_each(session)
    queue = await ReviewQueueService(session, tenant).get_queue(limit=50)
    by_id = {item.candidate_evaluation_id: item for item in queue.items}

    assert by_id[ids["awaiting_invitation"]].stage == QueueStage.AWAITING_INVITATION
    assert by_id[ids["awaiting_candidate"]].stage == QueueStage.AWAITING_CANDIDATE
    assert by_id[ids["ready"]].stage == QueueStage.READY_FOR_EVALUATION
    assert by_id[ids["evaluated"]].stage == QueueStage.EVALUATED
    assert by_id[ids["escalate"]].stage == QueueStage.NEEDS_REVIEW
    assert by_id[ids["mixed"]].stage == QueueStage.NEEDS_REVIEW

    # Recruiter-attention vs waiting/completed.
    assert by_id[ids["escalate"]].needs_attention is True
    assert by_id[ids["ready"]].needs_attention is True
    assert by_id[ids["awaiting_invitation"]].needs_attention is True
    assert by_id[ids["awaiting_candidate"]].needs_attention is False  # waiting on candidate
    assert by_id[ids["evaluated"]].needs_attention is False  # completed

    # Recommendation + confidence surfaced only when evaluated (raw values, not labels).
    assert by_id[ids["escalate"]].recommendation == "ESCALATE"
    assert by_id[ids["escalate"]].confidence == 0.2
    assert by_id[ids["ready"]].recommendation is None


async def test_deterministic_priority_ordering(session: AsyncSession) -> None:
    tenant, _, _ = await _one_of_each(session)
    queue = await ReviewQueueService(session, tenant).get_queue(limit=50)
    stages = [item.stage for item in queue.items]
    # ESCALATE, READY, MIXED, AWAITING_INVITATION, EVALUATED, AWAITING_CANDIDATE
    assert stages == [
        QueueStage.NEEDS_REVIEW,  # escalate (rank 0)
        QueueStage.READY_FOR_EVALUATION,  # rank 1
        QueueStage.NEEDS_REVIEW,  # mixed (rank 2)
        QueueStage.AWAITING_INVITATION,  # rank 3
        QueueStage.EVALUATED,  # rank 4
        QueueStage.AWAITING_CANDIDATE,  # rank 5
    ]


async def test_summary_counts_reflect_whole_queue(session: AsyncSession) -> None:
    tenant, _, _ = await _one_of_each(session)
    s = (await ReviewQueueService(session, tenant).get_queue(limit=1)).summary
    assert s.needs_review == 2  # escalate + mixed
    assert s.ready_to_evaluate == 1
    assert s.awaiting_invitation == 1
    assert s.waiting_on_candidate == 1
    assert s.completed == 1
    assert s.total == 6


# --- filters / search / pagination -------------------------------------------------- #


async def test_needs_attention_filter(session: AsyncSession) -> None:
    tenant, _, _ = await _one_of_each(session)
    queue = await ReviewQueueService(session, tenant).get_queue(
        queue_filter=QueueFilter.NEEDS_ATTENTION, limit=50
    )
    assert queue.total == 4  # escalate, ready, mixed, awaiting_invitation
    assert all(item.needs_attention for item in queue.items)


async def test_completed_and_waiting_filters(session: AsyncSession) -> None:
    tenant, _, _ = await _one_of_each(session)
    svc = ReviewQueueService(session, tenant)
    completed = await svc.get_queue(queue_filter=QueueFilter.COMPLETED, limit=50)
    assert [i.stage for i in completed.items] == [QueueStage.EVALUATED]
    waiting = await svc.get_queue(queue_filter=QueueFilter.WAITING, limit=50)
    assert [i.stage for i in waiting.items] == [QueueStage.AWAITING_CANDIDATE]


async def test_pagination_is_backend_and_deterministic(session: AsyncSession) -> None:
    tenant, _, _ = await _one_of_each(session)
    svc = ReviewQueueService(session, tenant)
    page1 = await svc.get_queue(limit=2, offset=0)
    page2 = await svc.get_queue(limit=2, offset=2)
    assert page1.total == 6 and len(page1.items) == 2
    assert [i.stage for i in page1.items] == [
        QueueStage.NEEDS_REVIEW,
        QueueStage.READY_FOR_EVALUATION,
    ]
    assert [i.stage for i in page2.items] == [
        QueueStage.NEEDS_REVIEW,  # mixed
        QueueStage.AWAITING_INVITATION,
    ]
    # Disjoint pages.
    assert not {i.candidate_evaluation_id for i in page1.items} & {
        i.candidate_evaluation_id for i in page2.items
    }


async def test_name_search_is_server_side(session: AsyncSession) -> None:
    tenant, _, ids = await _one_of_each(session)
    queue = await ReviewQueueService(session, tenant).get_queue(search="escalate", limit=50)
    assert [i.candidate_evaluation_id for i in queue.items] == [ids["escalate"]]
    assert queue.total == 1


async def test_search_also_matches_role(session: AsyncSession) -> None:
    tenant, _, _ = await _one_of_each(session)  # all six share role "Data Engineer"
    by_role = await ReviewQueueService(session, tenant).get_queue(search="data engineer", limit=50)
    assert by_role.total == 6  # a recruiter can find the whole role, not just a person
    none = await ReviewQueueService(session, tenant).get_queue(search="platform", limit=50)
    assert none.total == 0


# --- tenant isolation --------------------------------------------------------------- #


async def test_queue_surfaces_latest_decision_badge(session: AsyncSession) -> None:
    tenant, _, ids = await _one_of_each(session)
    # A recorded human decision appears as a badge on the row; others stay null. It does
    # NOT change the row's stage (badge only).
    session.add(
        HiringDecision(
            id=new_id(),
            organization_id=tenant,
            candidate_evaluation_id=ids["evaluated"],
            evaluation_id=None,
            sequence_number=1,
            decision="ADVANCE",
            rationale=None,
            decided_by_user_id="u",
            decided_at=datetime.now(UTC),
        )
    )
    await session.flush()

    queue = await ReviewQueueService(session, tenant).get_queue(limit=50)
    by_id = {i.candidate_evaluation_id: i for i in queue.items}
    assert by_id[ids["evaluated"]].decision == "ADVANCE"
    assert by_id[ids["evaluated"]].stage == QueueStage.EVALUATED  # stage unchanged
    assert by_id[ids["ready"]].decision is None


async def test_queue_is_tenant_isolated(session: AsyncSession) -> None:
    a_tenant, _, a_ids = await _one_of_each(session)
    # A second org with its own single ready candidate.
    b_tenant = await _org(session, "Globex", "b@globex.com")
    b_campaign = await _campaign(session, b_tenant, role="Platform Engineer")
    b_eval = await _cand_eval(
        session, b_tenant, b_campaign, name="B Person", email="bp@x.com", submitted=True
    )

    a_queue = await ReviewQueueService(session, a_tenant).get_queue(limit=50)
    a_visible = {i.candidate_evaluation_id for i in a_queue.items}
    assert b_eval not in a_visible  # never see the other tenant's candidate
    assert a_visible == set(a_ids.values())

    b_queue = await ReviewQueueService(session, b_tenant).get_queue(limit=50)
    assert {i.candidate_evaluation_id for i in b_queue.items} == {b_eval}
    # Counts are per-tenant — A's six do not bleed into B's summary.
    assert b_queue.summary.total == 1
    assert a_queue.summary.total == 6
