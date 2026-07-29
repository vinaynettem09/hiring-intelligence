"""Evaluation execution — the recruiter-triggered orchestration that turns immutable
Evidence into a durable, immutable Evaluation.

**Production-safe execution boundary (TD-011, Story 5.3).** A real model call can take
5-30+ seconds, so this workflow must NOT hold a DB transaction open across it. It is the
one deliberate, documented exception to the one-request/one-session rule: it owns its own
session lifecycle via the session factory.

    Transaction A (short read):  authorize → load submitted evaluation → verify tenant →
                                 verify consent → assemble immutable, PII-safe input →
                                 (idempotency short-circuits here, before any provider call)
    ── release the transaction ──
    NO SESSION HELD:             call the AIProvider
    Transaction B (short write): reload → re-check consent (withdrawal race) → persist the
                                 immutable Evaluation + assessments + citations → audit → commit

Only a fully-validated `EvaluationProposal` is ever persisted. A provider/validation
failure persists nothing and writes no `evaluation.generated` — it raises a typed
`UpstreamServiceError` (502). ESCALATE (a valid proposal) is a success, not a failure.
"""

from collections.abc import Callable
from datetime import UTC, datetime

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.modules.audit.service import AuditService
from app.modules.candidates.repository import CandidateEvaluationRepository
from app.modules.consent.service import ConsentService
from app.modules.evaluations.models import Evaluation
from app.modules.evaluations.repository import EvaluationRepository
from app.modules.evaluations.schemas import (
    CitationView,
    CompetencyAssessmentView,
    EvaluationDetail,
    EvaluationHistoryResponse,
    EvaluationRunSummary,
    EvidenceCoverageView,
    ObservationView,
    ProvenanceView,
)
from app.modules.identity.enums import UserRole
from app.modules.intelligence.enums import EscalationReason, RecommendationProposal
from app.modules.intelligence.schemas import EvaluationOutcome
from app.modules.intelligence.service import IntelligenceService
from app.shared.context import AuthContext
from app.shared.errors import (
    AuthorizationError,
    ConflictError,
    NotFoundError,
    UpstreamServiceError,
)
from app.shared.logging import get_logger

_log = get_logger(__name__)

# Who may trigger/view an evaluation. Centralized (not scattered role checks).
_ALLOWED_ROLES = frozenset(
    {UserRole.ADMIN.value, UserRole.RECRUITER.value, UserRole.HIRING_MANAGER.value}
)

IntelligenceFactory = Callable[[AsyncSession], IntelligenceService]


class EvaluationExecutionService:
    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
        auth: AuthContext,
        *,
        intelligence_factory: IntelligenceFactory | None = None,
    ) -> None:
        self._factory = session_factory
        self._auth = auth
        self._tenant_id = auth.organization_id
        # Built per read transaction (bound to that transaction's session for assembly);
        # the provider call afterwards uses no session. Injectable for tests.
        self._make_intelligence: IntelligenceFactory = intelligence_factory or (
            lambda session: IntelligenceService(session, self._tenant_id)
        )

    async def evaluate(
        self, candidate_evaluation_id: str, *, idempotency_key: str | None = None
    ) -> EvaluationDetail:
        """Ensure an Evaluation exists and return it. Idempotent: a repeat (or repeated
        Idempotency-Key) returns the existing run WITHOUT calling the provider again."""
        self._authorize()

        # --- Transaction A: authority + consent + assemble (short read) ---
        async with self._factory() as read:
            await self._require_candidate_evaluation(read, candidate_evaluation_id)
            repo = EvaluationRepository(read, self._tenant_id)
            if idempotency_key is not None:
                keyed = await repo.find_by_idempotency_key(
                    candidate_evaluation_id=candidate_evaluation_id, idempotency_key=idempotency_key
                )
                if keyed is not None:
                    return self._to_detail(keyed)
            latest = await repo.get_latest_for_candidate_evaluation(candidate_evaluation_id)
            if latest is not None:  # evaluate is not a rerun — return the existing run
                return self._to_detail(latest)
            await self._require_consent(read, candidate_evaluation_id)  # consent gate #1
            intelligence = self._make_intelligence(read)
            evaluation_input = await intelligence.assemble(candidate_evaluation_id)

        # --- No transaction held: the (possibly long, external) provider call ---
        outcome = await intelligence.evaluate_assembled(evaluation_input)

        # --- Transaction B: re-check + persist (short write) ---
        return await self._persist(
            candidate_evaluation_id, run_number=1, idempotency_key=idempotency_key, outcome=outcome
        )

    async def rerun(self, candidate_evaluation_id: str) -> EvaluationDetail:
        """Explicitly produce a NEW immutable run. Never mutates prior runs."""
        self._authorize()
        async with self._factory() as read:
            await self._require_candidate_evaluation(read, candidate_evaluation_id)
            await self._require_consent(read, candidate_evaluation_id)
            run_number = (
                await EvaluationRepository(read, self._tenant_id).count_for_candidate_evaluation(
                    candidate_evaluation_id
                )
            ) + 1
            intelligence = self._make_intelligence(read)
            evaluation_input = await intelligence.assemble(candidate_evaluation_id)

        outcome = await intelligence.evaluate_assembled(evaluation_input)

        return await self._persist(
            candidate_evaluation_id, run_number=run_number, idempotency_key=None, outcome=outcome
        )

    async def get_history(self, candidate_evaluation_id: str) -> EvaluationHistoryResponse:
        self._authorize()
        async with self._factory() as read:
            await self._require_candidate_evaluation(read, candidate_evaluation_id)
            repo = EvaluationRepository(read, self._tenant_id)
            runs = await repo.list_for_candidate_evaluation(candidate_evaluation_id)
            latest = await repo.get_latest_for_candidate_evaluation(candidate_evaluation_id)
            return EvaluationHistoryResponse(
                candidate_evaluation_id=candidate_evaluation_id,
                run_count=len(runs),
                latest=self._to_detail(latest) if latest is not None else None,
                runs=[self._to_summary(run) for run in runs],
            )

    # --- persistence (Transaction B) ------------------------------------- #

    async def _persist(
        self,
        candidate_evaluation_id: str,
        *,
        run_number: int,
        idempotency_key: str | None,
        outcome: EvaluationOutcome,
    ) -> EvaluationDetail:
        if outcome.proposal is None:  # provider/validation failure — persist NOTHING
            reason = outcome.failure.reason.value if outcome.failure else "UNKNOWN"
            _log.warning(
                "evaluation.not_produced",
                candidate_evaluation_id=candidate_evaluation_id,
                reason=reason,
            )
            raise UpstreamServiceError(
                "The evaluation could not be generated.",
                code=reason,
                metadata={"reason": reason},
            )

        async with self._factory() as write:
            # Reload authoritative state in a fresh transaction; re-check consent (the
            # withdrawal race: consent may have changed during the provider call).
            await self._require_candidate_evaluation(write, candidate_evaluation_id)
            await self._require_consent(write, candidate_evaluation_id)  # consent gate #2
            try:
                evaluation = await EvaluationRepository(write, self._tenant_id).create_evaluation(
                    candidate_evaluation_id=candidate_evaluation_id,
                    run_number=run_number,
                    idempotency_key=idempotency_key,
                    proposal=outcome.proposal,
                    input_fingerprint=outcome.input_fingerprint,
                    usage=outcome.usage,
                )
            except IntegrityError as exc:  # unique(run)/unique(idempotency) backstop tripped
                raise ConflictError(
                    "A concurrent evaluation run conflicted; please retry.",
                    code="EVALUATION_RUN_CONFLICT",
                ) from exc

            await AuditService(write).record(
                organization_id=self._tenant_id,
                actor_type="recruiter",
                actor_user_id=self._auth.user_id,
                action="evaluation.generated",
                target_type="evaluation",
                target_id=evaluation.id,
                # Safe metadata only — NO evidence text, prompt, raw output, or PII.
                details={
                    "candidate_evaluation_id": candidate_evaluation_id,
                    "run_number": evaluation.run_number,
                    "recommendation": evaluation.recommendation,
                    "confidence": evaluation.confidence,
                    "provider": evaluation.provider,
                    "model": evaluation.model,
                    "prompt_version": evaluation.prompt_version,
                    "input_fingerprint": evaluation.input_fingerprint,
                    "input_tokens": evaluation.input_tokens,
                    "output_tokens": evaluation.output_tokens,
                },
            )
            detail = self._to_detail(evaluation)
            await write.commit()
        return detail

    # --- gates ------------------------------------------------------------ #

    def _authorize(self) -> None:
        if self._auth.role not in _ALLOWED_ROLES:
            raise AuthorizationError(
                "You are not allowed to run evaluations.", code="EVALUATION_FORBIDDEN"
            )

    async def _require_candidate_evaluation(
        self, session: AsyncSession, candidate_evaluation_id: str
    ) -> None:
        # Tenant-scoped: another org's evaluation reads as absent → 404, never 403.
        evaluation = await CandidateEvaluationRepository(session, self._tenant_id).get(
            candidate_evaluation_id
        )
        if evaluation is None:
            raise NotFoundError(
                "Candidate evaluation not found.", code="CANDIDATE_EVALUATION_NOT_FOUND"
            )

    async def _require_consent(self, session: AsyncSession, candidate_evaluation_id: str) -> None:
        # AI processing is a distinct processing action from submission — re-check consent.
        if not await ConsentService(session).has_active_consent(candidate_evaluation_id):
            raise AuthorizationError(
                "Active consent is required to evaluate this candidate.",
                code="CONSENT_REQUIRED",
            )

    # --- mapping (ORM → recruiter-safe DTO) ------------------------------- #

    def _to_detail(self, evaluation: Evaluation) -> EvaluationDetail:
        return EvaluationDetail(
            id=evaluation.id,
            candidate_evaluation_id=evaluation.candidate_evaluation_id,
            run_number=evaluation.run_number,
            # Stored as the enum's string value; coerce explicitly at the boundary.
            recommendation=RecommendationProposal(evaluation.recommendation),
            confidence=evaluation.confidence,
            confidence_rationale=evaluation.confidence_rationale,
            escalation_reason=(
                EscalationReason(evaluation.escalation_reason)
                if evaluation.escalation_reason is not None
                else None
            ),
            competency_assessments=[
                CompetencyAssessmentView(
                    competency=assessment.competency,
                    assessment=assessment.assessment,
                    provider_signal=assessment.provider_signal,
                    citations=[
                        CitationView(
                            evidence_id=citation.evidence_id, task_id=citation.work_sample_task_id
                        )
                        for citation in assessment.citations
                    ],
                )
                for assessment in evaluation.assessments
            ],
            strengths=_observation_views(evaluation.strengths),
            concerns=_observation_views(evaluation.concerns),
            evidence_coverage=EvidenceCoverageView(
                competencies_total=evaluation.coverage_competencies_total,
                competencies_assessed=evaluation.coverage_competencies_assessed,
                tasks_total=evaluation.coverage_tasks_total,
                tasks_with_evidence=evaluation.coverage_tasks_with_evidence,
            ),
            provenance=ProvenanceView(
                provider=evaluation.provider,
                model=evaluation.model,
                model_version=evaluation.model_version,
                prompt_version=evaluation.prompt_version,
                input_schema_version=evaluation.input_schema_version,
                output_schema_version=evaluation.output_schema_version,
                confidence_algorithm_version=evaluation.confidence_algorithm_version,
                generated_at=_utc(evaluation.generated_at),
            ),
            input_fingerprint=evaluation.input_fingerprint,
            input_tokens=evaluation.input_tokens,
            output_tokens=evaluation.output_tokens,
            created_at=_utc(evaluation.created_at),
        )

    @staticmethod
    def _to_summary(evaluation: Evaluation) -> EvaluationRunSummary:
        return EvaluationRunSummary(
            id=evaluation.id,
            run_number=evaluation.run_number,
            recommendation=RecommendationProposal(evaluation.recommendation),
            confidence=evaluation.confidence,
            model=evaluation.model,
            prompt_version=evaluation.prompt_version,
            created_at=_utc(evaluation.created_at),
        )


def _utc(value: datetime) -> datetime:
    # SQLite returns naive datetimes; treat stored timestamps as UTC for a stable contract.
    return value if value.tzinfo is not None else value.replace(tzinfo=UTC)


def _observation_views(stored: list[dict[str, object]]) -> list[ObservationView]:
    """Map persisted strength/concern JSON ({text, citations:[{evidence_id, task_id}]}) to
    the recruiter DTO — every observation carries its grounding citations."""
    views: list[ObservationView] = []
    for item in stored:
        raw_citations = item.get("citations", [])
        citations = raw_citations if isinstance(raw_citations, list) else []
        views.append(
            ObservationView(
                text=str(item.get("text", "")),
                citations=[
                    CitationView(
                        evidence_id=str(c.get("evidence_id")), task_id=str(c.get("task_id"))
                    )
                    for c in citations
                    if isinstance(c, dict)
                ],
            )
        )
    return views
