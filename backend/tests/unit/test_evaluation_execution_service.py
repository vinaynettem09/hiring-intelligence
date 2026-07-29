"""Evaluation execution — the production-safe boundary (TD-011) + the 5.2 guarantees.

The service owns its transaction boundaries: Txn A assembles the PII-safe input, the
transaction is released, the provider is called with NO session held, then Txn B re-checks
consent and persists. These tests prove that split, plus idempotency, rerun/immutability,
confidence, provenance, failure, and consent-race behavior — all with the deterministic mock.
"""

from collections.abc import Callable
from datetime import UTC, datetime

import pytest
from sqlalchemy import func, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from support import SubmittedEvaluation, submitted_evaluation

from app.modules.audit.models import AuditEvent
from app.modules.consent.models import Consent
from app.modules.consent.service import ConsentService
from app.modules.evaluations.models import Evaluation
from app.modules.evaluations.repository import EvaluationRepository
from app.modules.evaluations.service import EvaluationExecutionService
from app.modules.intelligence.enums import EscalationReason, RecommendationProposal
from app.modules.intelligence.schemas import (
    EvaluationInput,
    EvaluationProposal,
    EvidenceCoverage,
    Provenance,
)
from app.modules.intelligence.service import IntelligenceService
from app.platform.ai import (
    AIProvider,
    ProviderCitation,
    ProviderCompetencyAssessment,
    ProviderDescriptor,
    ProviderError,
    ProviderResult,
)
from app.shared.context import AuthContext
from app.shared.errors import (
    AuthorizationError,
    BusinessRuleViolation,
    NotFoundError,
    UpstreamServiceError,
)

Factory = async_sessionmaker[AsyncSession]


def _auth(tenant: str, *, role: str = "recruiter", user_id: str = "u1") -> AuthContext:
    return AuthContext(user_id=user_id, organization_id=tenant, role=role, correlation_id="corr")


# --- provider doubles -------------------------------------------------------- #


class _GroundedProvider:
    def __init__(
        self,
        *,
        provider: str = "fake",
        model_version: str = "v9",
        recommendation: str = "PROCEED",
        provider_confidence: float | None = None,
    ) -> None:
        self._provider = provider
        self._model_version = model_version
        self._recommendation = recommendation
        self._provider_confidence = provider_confidence

    @property
    def descriptor(self) -> ProviderDescriptor:
        return ProviderDescriptor(
            provider=self._provider, model="fake-model", model_version=self._model_version
        )

    async def evaluate(self, evaluation_input: EvaluationInput) -> ProviderResult:
        by_competency: dict[str, list[str]] = {}
        for task in evaluation_input.tasks:
            for competency in task.competencies:
                by_competency.setdefault(competency, []).extend(
                    item.evidence_id for item in task.evidence
                )
        return ProviderResult(
            competency_assessments=[
                ProviderCompetencyAssessment(
                    competency=c.name,
                    assessment="grounded",
                    citations=[
                        ProviderCitation(evidence_id=e) for e in by_competency.get(c.name, [])
                    ],
                )
                for c in evaluation_input.role.competencies
            ],
            recommendation=self._recommendation,
            provider_confidence=self._provider_confidence,
        )


class _RaisingProvider:
    @property
    def descriptor(self) -> ProviderDescriptor:
        return ProviderDescriptor(provider="fake", model="m", model_version="1")

    async def evaluate(self, evaluation_input: EvaluationInput) -> ProviderResult:
        raise ProviderError("down")


class _FixedConfidence:
    def __init__(self, value: float) -> None:
        self._value = value

    @property
    def version(self) -> str:
        return "test"

    def compute(self, evaluation_input: EvaluationInput, result: ProviderResult) -> float:
        return self._value


def _intel_factory(
    tenant: str, *, provider: AIProvider, confidence: float | None = None
) -> Callable[[AsyncSession], IntelligenceService]:
    calc = _FixedConfidence(confidence) if confidence is not None else None
    return lambda session: IntelligenceService(
        session,
        tenant,
        provider=provider,
        confidence_calculator=calc,
    )


# --- transaction-tracking factory (proves no session open during provider call) --- #


class _OpenCounter:
    def __init__(self) -> None:
        self.open = 0


class _TrackedSession:
    def __init__(self, session: AsyncSession, counter: _OpenCounter) -> None:
        self._session = session
        self._counter = counter

    async def __aenter__(self) -> AsyncSession:
        self._counter.open += 1
        return await self._session.__aenter__()

    async def __aexit__(self, *exc: object) -> None:
        try:
            await self._session.__aexit__(*exc)
        finally:
            self._counter.open -= 1


def _counting_factory(real: Factory, counter: _OpenCounter) -> Callable[[], _TrackedSession]:
    def make() -> _TrackedSession:
        return _TrackedSession(real(), counter)

    return make


# --- helpers ----------------------------------------------------------------- #


async def _seed(factory: Factory, **kwargs: object) -> SubmittedEvaluation:
    async with factory() as session:
        setup = await submitted_evaluation(session, **kwargs)  # type: ignore[arg-type]
        await session.commit()
    return setup


async def _count(factory: Factory, model: type) -> int:
    async with factory() as session:
        return int((await session.execute(select(func.count()).select_from(model))).scalar_one())


async def _generated_audits(factory: Factory) -> int:
    async with factory() as session:
        return int(
            (
                await session.execute(
                    select(func.count())
                    .select_from(AuditEvent)
                    .where(AuditEvent.action == "evaluation.generated")
                )
            ).scalar_one()
        )


async def _withdraw_consent(factory: Factory, candidate_evaluation_id: str) -> None:
    async with factory() as session:
        await session.execute(
            update(Consent)
            .where(Consent.candidate_evaluation_id == candidate_evaluation_id)
            .values(withdrawn_at=datetime.now(UTC))
        )
        await session.commit()


# --- TD-011: no transaction held during the provider call -------------------- #


async def test_no_transaction_held_during_provider_call(session_factory: Factory) -> None:
    setup = await _seed(session_factory)
    counter = _OpenCounter()
    counting = _counting_factory(session_factory, counter)
    observed: dict[str, int] = {}

    class _Spy(_GroundedProvider):
        async def evaluate(self, evaluation_input: EvaluationInput) -> ProviderResult:
            observed["open_during_call"] = counter.open  # sessions open right now
            return await super().evaluate(evaluation_input)

    await EvaluationExecutionService(
        counting,  # type: ignore[arg-type]  # intentional test double, not a real async_sessionmaker
        _auth(setup.tenant),
        intelligence_factory=_intel_factory(setup.tenant, provider=_Spy()),
    ).evaluate(setup.evaluation_id)

    # PROOF: zero sessions (hence zero DB transactions) were open during the provider call.
    assert observed["open_during_call"] == 0
    assert await _count(session_factory, Evaluation) == 1  # and it still persisted


# --- happy path -------------------------------------------------------------- #


async def test_evaluate_persists_immutable_grounded_evaluation(session_factory: Factory) -> None:
    setup = await _seed(session_factory)
    detail = await EvaluationExecutionService(session_factory, _auth(setup.tenant)).evaluate(
        setup.evaluation_id
    )
    assert detail.run_number == 1
    assert detail.recommendation == RecommendationProposal.PROCEED
    assert detail.provenance.provider == "mock"
    assert detail.input_fingerprint.startswith("sha256:")
    assert detail.competency_assessments
    for assessment in detail.competency_assessments:
        assert assessment.citations
        for citation in assessment.citations:
            assert citation.task_id in set(setup.task_ids)
    assert await _generated_audits(session_factory) == 1
    assert await _count(session_factory, Evaluation) == 1


# --- idempotency ------------------------------------------------------------- #


async def test_evaluate_is_idempotent_without_key(session_factory: Factory) -> None:
    setup = await _seed(session_factory)
    service = EvaluationExecutionService(session_factory, _auth(setup.tenant))
    first = await service.evaluate(setup.evaluation_id)
    second = await service.evaluate(setup.evaluation_id)
    assert second.id == first.id
    assert await _count(session_factory, Evaluation) == 1
    assert await _generated_audits(session_factory) == 1


async def test_evaluate_idempotency_key_returns_same_run(session_factory: Factory) -> None:
    setup = await _seed(session_factory)
    service = EvaluationExecutionService(session_factory, _auth(setup.tenant))
    first = await service.evaluate(setup.evaluation_id, idempotency_key="abc")
    second = await service.evaluate(setup.evaluation_id, idempotency_key="abc")
    assert second.id == first.id
    assert await _count(session_factory, Evaluation) == 1


# --- rerun + immutability ---------------------------------------------------- #


async def test_rerun_creates_new_run_and_leaves_run_one_intact(session_factory: Factory) -> None:
    setup = await _seed(session_factory)
    auth = _auth(setup.tenant)
    run1 = await EvaluationExecutionService(session_factory, auth).evaluate(setup.evaluation_id)

    alt = _intel_factory(
        setup.tenant,
        provider=_GroundedProvider(
            provider="alt", model_version="99", recommendation="DO_NOT_PROCEED"
        ),
        confidence=0.9,
    )
    run2 = await EvaluationExecutionService(session_factory, auth, intelligence_factory=alt).rerun(
        setup.evaluation_id
    )
    assert run2.run_number == 2
    assert run2.id != run1.id
    assert run2.recommendation == RecommendationProposal.DO_NOT_PROCEED

    async with session_factory() as session:
        reloaded = await EvaluationRepository(session, setup.tenant).get_evaluation(run1.id)
    assert reloaded is not None
    assert reloaded.recommendation == RecommendationProposal.PROCEED.value  # unchanged
    assert reloaded.model_version == "v1"


async def test_history_exposes_latest_and_run_count(session_factory: Factory) -> None:
    setup = await _seed(session_factory)
    service = EvaluationExecutionService(session_factory, _auth(setup.tenant))
    await service.evaluate(setup.evaluation_id)
    await service.rerun(setup.evaluation_id)
    history = await service.get_history(setup.evaluation_id)
    assert history.run_count == 2
    assert history.latest is not None
    assert history.latest.run_number == 2
    assert [r.run_number for r in history.runs] == [2, 1]


async def test_history_before_any_evaluation_is_empty(session_factory: Factory) -> None:
    setup = await _seed(session_factory)
    history = await EvaluationExecutionService(session_factory, _auth(setup.tenant)).get_history(
        setup.evaluation_id
    )
    assert history.run_count == 0
    assert history.latest is None


# --- confidence -------------------------------------------------------------- #


async def test_persisted_confidence_is_platform_not_provider(session_factory: Factory) -> None:
    setup = await _seed(session_factory)
    detail = await EvaluationExecutionService(session_factory, _auth(setup.tenant)).evaluate(
        setup.evaluation_id
    )
    # Platform value: full coverage, but the mock emits a balanced strength+concern, so v2
    # decisiveness floors it to 0.5. Crucially it is NOT the mock's raw provider_confidence
    # (0.42) — the platform computes confidence; the model does not own it.
    assert detail.confidence == 0.5
    assert detail.confidence != 0.42


async def test_low_confidence_persists_escalate(session_factory: Factory) -> None:
    setup = await _seed(session_factory)
    factory = _intel_factory(
        setup.tenant, provider=_GroundedProvider(recommendation="PROCEED"), confidence=0.1
    )
    detail = await EvaluationExecutionService(
        session_factory, _auth(setup.tenant), intelligence_factory=factory
    ).evaluate(setup.evaluation_id)
    assert detail.recommendation == RecommendationProposal.ESCALATE
    assert detail.escalation_reason == EscalationReason.LOW_CONFIDENCE


async def test_historical_run_retains_its_original_confidence_and_version(
    session_factory: Factory,
) -> None:
    """Point 12(h): a run persisted under confidence-v1 keeps its original number and
    algorithm version forever — reads never recompute or silently upgrade it. This is what
    lets us bump the confidence algorithm without rewriting history."""
    setup = await _seed(session_factory)
    async with session_factory() as session:
        created = await EvaluationRepository(session, setup.tenant).create_evaluation(
            candidate_evaluation_id=setup.evaluation_id,
            run_number=1,
            idempotency_key=None,
            proposal=_v1_proposal(),  # an "old" run: confidence-v1, confidence 0.83
            input_fingerprint="sha256:x",
        )
        await session.commit()
        evaluation_id = created.id

    async with session_factory() as session:
        reloaded = await EvaluationRepository(session, setup.tenant).get_evaluation(evaluation_id)
    assert reloaded is not None
    assert reloaded.confidence_algorithm_version == "confidence-v1"  # not upgraded to v2
    assert reloaded.confidence == 0.83  # original number, verbatim


def _v1_proposal() -> EvaluationProposal:
    """A proposal shaped as a historical confidence-v1 run (0.83), for the retention test."""
    provenance = Provenance(
        provider="mock",
        model="deterministic-mock",
        model_version="v1",
        prompt_version="eval-prompt-v2",
        input_schema_version="eval-input-v1",
        output_schema_version="eval-proposal-v1",
        confidence_algorithm_version="confidence-v1",
        generated_at=datetime(2026, 1, 1, tzinfo=UTC),
    )
    return EvaluationProposal(
        recommendation=RecommendationProposal.PROCEED,
        confidence=0.83,
        confidence_rationale="historical v1 run",
        competency_assessments=(),
        strengths=(),
        concerns=(),
        evidence_coverage=EvidenceCoverage(
            competencies_total=1, competencies_assessed=1, tasks_total=1, tasks_with_evidence=1
        ),
        provenance=provenance,
    )


async def test_high_confidence_do_not_proceed_persists_unchanged(session_factory: Factory) -> None:
    setup = await _seed(session_factory)
    factory = _intel_factory(
        setup.tenant, provider=_GroundedProvider(recommendation="DO_NOT_PROCEED"), confidence=0.95
    )
    detail = await EvaluationExecutionService(
        session_factory, _auth(setup.tenant), intelligence_factory=factory
    ).evaluate(setup.evaluation_id)
    assert detail.recommendation == RecommendationProposal.DO_NOT_PROCEED
    assert detail.escalation_reason is None


# --- provenance -------------------------------------------------------------- #


async def test_provenance_persisted_and_stable_across_reruns(session_factory: Factory) -> None:
    setup = await _seed(session_factory)
    auth = _auth(setup.tenant)
    run1 = await EvaluationExecutionService(session_factory, auth).evaluate(setup.evaluation_id)
    assert run1.provenance.prompt_version == "eval-prompt-v3"

    alt = _intel_factory(
        setup.tenant, provider=_GroundedProvider(provider="alt", model_version="42")
    )
    await EvaluationExecutionService(session_factory, auth, intelligence_factory=alt).rerun(
        setup.evaluation_id
    )
    async with session_factory() as session:
        reloaded = await EvaluationRepository(session, setup.tenant).get_evaluation(run1.id)
    assert reloaded is not None
    assert reloaded.provider == "mock"
    assert reloaded.model_version == "v1"


# --- failure taxonomy -------------------------------------------------------- #


async def test_provider_failure_persists_nothing(session_factory: Factory) -> None:
    setup = await _seed(session_factory)
    factory = _intel_factory(setup.tenant, provider=_RaisingProvider())
    with pytest.raises(UpstreamServiceError) as exc:
        await EvaluationExecutionService(
            session_factory, _auth(setup.tenant), intelligence_factory=factory
        ).evaluate(setup.evaluation_id)
    assert exc.value.code == "PROVIDER_UNAVAILABLE"
    assert await _count(session_factory, Evaluation) == 0
    assert await _generated_audits(session_factory) == 0


async def test_failed_rerun_leaves_prior_run_and_audit_intact(session_factory: Factory) -> None:
    setup = await _seed(session_factory)
    auth = _auth(setup.tenant)
    await EvaluationExecutionService(session_factory, auth).evaluate(setup.evaluation_id)
    factory = _intel_factory(setup.tenant, provider=_RaisingProvider())
    with pytest.raises(UpstreamServiceError):
        await EvaluationExecutionService(session_factory, auth, intelligence_factory=factory).rerun(
            setup.evaluation_id
        )
    assert await _count(session_factory, Evaluation) == 1
    assert await _generated_audits(session_factory) == 1


# --- preconditions / consent ------------------------------------------------- #


async def test_evaluate_requires_active_consent(session_factory: Factory) -> None:
    setup = await _seed(session_factory)
    await _withdraw_consent(session_factory, setup.evaluation_id)
    with pytest.raises(AuthorizationError) as exc:
        await EvaluationExecutionService(session_factory, _auth(setup.tenant)).evaluate(
            setup.evaluation_id
        )
    assert exc.value.code == "CONSENT_REQUIRED"
    assert await _count(session_factory, Evaluation) == 0


async def test_consent_withdrawn_mid_execution_persists_nothing(session_factory: Factory) -> None:
    # The race: consent active during assembly, withdrawn during the provider call. Gate #2
    # (fresh transaction before persist) catches it.
    setup = await _seed(session_factory)

    class _WithdrawingProvider(_GroundedProvider):
        async def evaluate(self, evaluation_input: EvaluationInput) -> ProviderResult:
            await _withdraw_consent(session_factory, setup.evaluation_id)
            return await super().evaluate(evaluation_input)

    factory = _intel_factory(setup.tenant, provider=_WithdrawingProvider())
    with pytest.raises(AuthorizationError) as exc:
        await EvaluationExecutionService(
            session_factory, _auth(setup.tenant), intelligence_factory=factory
        ).evaluate(setup.evaluation_id)
    assert exc.value.code == "CONSENT_REQUIRED"
    assert await _count(session_factory, Evaluation) == 0
    assert await _generated_audits(session_factory) == 0


async def test_unsubmitted_evaluation_cannot_be_evaluated(session_factory: Factory) -> None:
    setup = await _seed(session_factory, submit=False)
    async with session_factory() as session:
        await ConsentService(session).grant(setup.token)
        await session.commit()
    with pytest.raises(BusinessRuleViolation) as exc:
        await EvaluationExecutionService(session_factory, _auth(setup.tenant)).evaluate(
            setup.evaluation_id
        )
    assert exc.value.code == "EVALUATION_NOT_SUBMITTED"
    assert await _count(session_factory, Evaluation) == 0


# --- authorization / tenant isolation ---------------------------------------- #


async def test_disallowed_role_is_forbidden(session_factory: Factory) -> None:
    setup = await _seed(session_factory)
    with pytest.raises(AuthorizationError) as exc:
        await EvaluationExecutionService(
            session_factory, _auth(setup.tenant, role="observer")
        ).evaluate(setup.evaluation_id)
    assert exc.value.code == "EVALUATION_FORBIDDEN"


async def test_other_tenant_cannot_evaluate_or_read(session_factory: Factory) -> None:
    a = await _seed(session_factory, org="Acme", user_email="a@acme.com")
    b = await _seed(session_factory, org="Globex", user_email="b@globex.com")
    await EvaluationExecutionService(session_factory, _auth(a.tenant)).evaluate(a.evaluation_id)
    with pytest.raises(NotFoundError):
        await EvaluationExecutionService(session_factory, _auth(b.tenant)).evaluate(a.evaluation_id)
    with pytest.raises(NotFoundError):
        await EvaluationExecutionService(session_factory, _auth(b.tenant)).get_history(
            a.evaluation_id
        )
