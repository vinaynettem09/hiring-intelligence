"""PostgreSQL integration — the Evaluation DB guarantees SQLite can't fully prove:
the run-number and idempotency-key uniqueness backstops, and the citation→Evidence
foreign key. These protect immutability/idempotency independently of application code.

Assumes migrations are applied (CI runs `alembic upgrade head`). Builds a minimal
candidate-evaluation graph directly (no full candidate pipeline) so the test stays focused.
"""

import os
from collections.abc import AsyncIterator
from datetime import UTC, datetime

import pytest
import pytest_asyncio
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.modules.campaigns.models import Campaign
from app.modules.candidates.models import Candidate, CandidateEvaluation
from app.modules.evaluations.models import EvaluationCitation
from app.modules.evaluations.repository import EvaluationRepository
from app.modules.identity.models import Organization
from app.modules.intelligence.enums import RecommendationProposal
from app.modules.intelligence.schemas import (
    CompetencyAssessment,
    EvaluationProposal,
    EvidenceCoverage,
    Provenance,
)
from app.shared.ids import new_id

pytestmark = pytest.mark.integration

DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql+asyncpg://app:app@localhost:5432/hiring")


@pytest_asyncio.fixture
async def make_session() -> AsyncIterator[async_sessionmaker[AsyncSession]]:
    engine = create_async_engine(DATABASE_URL)
    yield async_sessionmaker(engine, expire_on_commit=False)
    await engine.dispose()


def _proposal(*, with_assessment: bool = False) -> EvaluationProposal:
    provenance = Provenance(
        provider="mock",
        model="deterministic-mock",
        model_version="v1",
        prompt_version="eval-prompt-v1",
        input_schema_version="eval-input-v1",
        output_schema_version="eval-proposal-v1",
        confidence_algorithm_version="confidence-v1",
        generated_at=datetime(2026, 1, 1, tzinfo=UTC),
    )
    assessments = (
        (CompetencyAssessment(competency="SQL", assessment="ok", evidence_citations=()),)
        if with_assessment
        else ()
    )
    return EvaluationProposal(
        recommendation=RecommendationProposal.PROCEED,
        confidence=1.0,
        confidence_rationale="t",
        competency_assessments=assessments,
        strengths=(),
        concerns=(),
        evidence_coverage=EvidenceCoverage(
            competencies_total=1, competencies_assessed=1, tasks_total=1, tasks_with_evidence=1
        ),
        provenance=provenance,
    )


async def _seed_candidate_evaluation(session: AsyncSession) -> tuple[str, str]:
    """Minimal org → campaign → candidate → candidate_evaluation. Returns (org_id, eval_id)."""
    org_id, campaign_id, candidate_id, eval_id = (new_id() for _ in range(4))
    # These models carry no ORM relationship/column-level ForeignKey (the FKs live in the
    # migrations), so the unit of work won't order inserts by dependency — it would emit them
    # by table name and violate the real Postgres FKs. Flush each tier before the rows that
    # reference it: organization -> {campaign, candidate} -> candidate_evaluation.
    session.add(Organization(id=org_id, name="PG Eval Co"))
    await session.flush()
    session.add(
        Campaign(
            id=campaign_id,
            organization_id=org_id,
            role_title="Data Engineer",
            role_profile={"competencies": [{"name": "SQL"}], "bar": "senior"},
            status="active",
        )
    )
    session.add(Candidate(id=candidate_id, organization_id=org_id, name="Ada", email="ada@x.com"))
    await session.flush()
    session.add(
        CandidateEvaluation(
            id=eval_id,
            organization_id=org_id,
            campaign_id=campaign_id,
            candidate_id=candidate_id,
            status="submitted",
        )
    )
    await session.commit()
    return org_id, eval_id


async def test_duplicate_run_number_is_rejected(
    make_session: async_sessionmaker[AsyncSession],
) -> None:
    async with make_session() as s:
        org_id, eval_id = await _seed_candidate_evaluation(s)
    async with make_session() as s:
        await EvaluationRepository(s, org_id).create_evaluation(
            candidate_evaluation_id=eval_id,
            run_number=1,
            idempotency_key=None,
            proposal=_proposal(),
            input_fingerprint="sha256:x",
        )
        await s.commit()
    async with make_session() as s:
        with pytest.raises(IntegrityError):
            await EvaluationRepository(s, org_id).create_evaluation(
                candidate_evaluation_id=eval_id,
                run_number=1,  # same run number → unique(candidate_evaluation_id, run_number)
                idempotency_key=None,
                proposal=_proposal(),
                input_fingerprint="sha256:y",
            )
            await s.commit()


async def test_duplicate_idempotency_key_is_rejected(
    make_session: async_sessionmaker[AsyncSession],
) -> None:
    async with make_session() as s:
        org_id, eval_id = await _seed_candidate_evaluation(s)
    async with make_session() as s:
        await EvaluationRepository(s, org_id).create_evaluation(
            candidate_evaluation_id=eval_id,
            run_number=1,
            idempotency_key="key-1",
            proposal=_proposal(),
            input_fingerprint="sha256:x",
        )
        await s.commit()
    async with make_session() as s:
        with pytest.raises(IntegrityError):
            await EvaluationRepository(s, org_id).create_evaluation(
                candidate_evaluation_id=eval_id,
                run_number=2,
                idempotency_key="key-1",  # same key -> unique(cand_eval_id, idempotency_key)
                proposal=_proposal(),
                input_fingerprint="sha256:y",
            )
            await s.commit()


async def test_citation_to_missing_evidence_is_rejected(
    make_session: async_sessionmaker[AsyncSession],
) -> None:
    async with make_session() as s:
        org_id, eval_id = await _seed_candidate_evaluation(s)
    async with make_session() as s:
        evaluation = await EvaluationRepository(s, org_id).create_evaluation(
            candidate_evaluation_id=eval_id,
            run_number=1,
            idempotency_key=None,
            proposal=_proposal(with_assessment=True),
            input_fingerprint="sha256:x",
        )
        await s.commit()
        assessment_id = evaluation.assessments[0].id
    # A citation to non-existent Evidence must fail the foreign key.
    async with make_session() as s:
        with pytest.raises(IntegrityError):
            s.add(
                EvaluationCitation(
                    id=new_id(),
                    organization_id=org_id,
                    evaluation_id=evaluation.id,
                    competency_assessment_id=assessment_id,
                    evidence_id="does-not-exist",
                    work_sample_task_id="does-not-exist",
                )
            )
            await s.commit()
