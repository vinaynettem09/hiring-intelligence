"""Evaluation persistence guarantees: append-only repository, citation integrity, and
tenant isolation of Evaluations/citations."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from support import SubmittedEvaluation, submitted_evaluation

from app.modules.evaluations.models import EvaluationCitation
from app.modules.evaluations.repository import EvaluationRepository
from app.modules.evaluations.service import EvaluationExecutionService
from app.modules.evidence.models import Evidence
from app.shared.context import AuthContext

Factory = async_sessionmaker[AsyncSession]


def _auth(tenant: str) -> AuthContext:
    return AuthContext(user_id="u", organization_id=tenant, role="recruiter", correlation_id="c")


async def _seed(factory: Factory, **kwargs: object) -> SubmittedEvaluation:
    async with factory() as session:
        setup = await submitted_evaluation(session, **kwargs)  # type: ignore[arg-type]
        await session.commit()
    return setup


async def _evidence_ids(session: AsyncSession, candidate_evaluation_id: str) -> set[str]:
    rows = await session.execute(
        select(Evidence.id).where(Evidence.candidate_evaluation_id == candidate_evaluation_id)
    )
    return set(rows.scalars())


def test_repository_is_append_only() -> None:
    for forbidden in ("update", "delete", "save", "remove"):
        assert not hasattr(EvaluationRepository, forbidden), f"repo must not expose {forbidden}"


async def test_citations_reference_only_this_evaluations_evidence(session_factory: Factory) -> None:
    a = await _seed(session_factory, org="Acme", user_email="a@acme.com")
    b = await _seed(session_factory, org="Globex", user_email="b@globex.com")
    await EvaluationExecutionService(session_factory, _auth(a.tenant)).evaluate(a.evaluation_id)

    async with session_factory() as session:
        a_evidence = await _evidence_ids(session, a.evaluation_id)
        b_evidence = await _evidence_ids(session, b.evaluation_id)
        citations = (await session.execute(select(EvaluationCitation))).scalars().all()

    assert citations  # the mock produced grounded citations
    for citation in citations:
        assert citation.evidence_id in a_evidence  # only A's evidence
        assert citation.evidence_id not in b_evidence  # never bridges to B
        assert citation.organization_id == a.tenant


async def test_other_tenant_cannot_read_or_list_evaluations(session_factory: Factory) -> None:
    a = await _seed(session_factory, org="Acme", user_email="a@acme.com")
    b = await _seed(session_factory, org="Globex", user_email="b@globex.com")
    detail = await EvaluationExecutionService(session_factory, _auth(a.tenant)).evaluate(
        a.evaluation_id
    )

    async with session_factory() as session:
        b_repo = EvaluationRepository(session, b.tenant)
        assert await b_repo.get_evaluation(detail.id) is None  # not readable cross-tenant
        assert await b_repo.list_for_candidate_evaluation(a.evaluation_id) == []
        assert await b_repo.get_latest_for_candidate_evaluation(a.evaluation_id) is None
        assert await EvaluationRepository(session, a.tenant).get_evaluation(detail.id) is not None
