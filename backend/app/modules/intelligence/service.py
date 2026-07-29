"""Intelligence orchestrator — the one place the evaluation pipeline is wired.

Pipeline (each stage can only *reduce* trust; nothing skips ahead):

    assembler.build            → immutable, PII-minimized EvaluationInput  (INV-012)
    provider.evaluate          → raw, UNTRUSTED ProviderResult
    schema/vocabulary check    → INVALID_PROVIDER_OUTPUT on failure
    grounding check            → UNGROUNDED_OUTPUT on failure
    policy check               → POLICY_VIOLATION on failure
    confidence (platform-owned)→ [0, 1] reliability signal
    honesty floor              → forces ESCALATE when confidence < floor
    → EvaluationProposal + Provenance, wrapped in an EvaluationOutcome

The orchestrator persists nothing and depends only on the `AIProvider` seam (defaults to
the deterministic mock; `anthropic` is selectable via config from Story 5.3). `assemble`
(DB) and `evaluate_assembled` (no DB, the provider call) are split so the execution
boundary can release its transaction before a long external call (TD-011).
"""

from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.modules.intelligence.assembler import EvaluationInputAssembler
from app.modules.intelligence.confidence import (
    ConfidenceCalculator,
    DeterministicConfidenceCalculator,
)
from app.modules.intelligence.enums import (
    EscalationReason,
    EvaluationFailureReason,
    RecommendationProposal,
)
from app.modules.intelligence.fingerprint import fingerprint_input
from app.modules.intelligence.schemas import (
    CompetencyAssessment,
    EvaluationFailure,
    EvaluationInput,
    EvaluationOutcome,
    EvaluationProposal,
    EvidenceCitation,
    EvidenceCoverage,
    GroundedObservation,
    Provenance,
)
from app.modules.intelligence.validators import (
    evidence_to_task,
    validate_grounding,
    validate_policy,
)
from app.modules.intelligence.versions import (
    CONFIDENCE_ALGORITHM_VERSION,
    INPUT_SCHEMA_VERSION,
    OUTPUT_SCHEMA_VERSION,
    prompt_version,
)
from app.platform.ai import (
    AIProvider,
    ProviderError,
    ProviderObservation,
    ProviderResult,
    get_ai_provider,
)
from app.platform.pii import PIIMinimizer
from app.shared.logging import get_logger

_log = get_logger(__name__)


class IntelligenceService:
    """Orchestrates one evaluation. Tenant-scoped (the assembler only reaches this
    tenant's data). Provider / confidence calculator / minimizer are injectable — the
    orchestrator itself names no concrete provider."""

    def __init__(
        self,
        session: AsyncSession,
        tenant_id: str,
        *,
        provider: AIProvider | None = None,
        minimizer: PIIMinimizer | None = None,
        confidence_calculator: ConfidenceCalculator | None = None,
        confidence_floor: float | None = None,
    ) -> None:
        self._assembler = EvaluationInputAssembler(session, tenant_id, minimizer=minimizer)
        self._provider = provider or get_ai_provider()
        self._confidence = confidence_calculator or DeterministicConfidenceCalculator()
        self._floor = (
            confidence_floor
            if confidence_floor is not None
            else get_settings().evaluation_confidence_floor
        )

    async def assemble(self, evaluation_id: str) -> EvaluationInput:
        """The ONLY DB-touching step: build the immutable, PII-safe input. Kept separate
        from `evaluate_assembled` so the execution boundary can release its DB transaction
        before the (potentially long, external) provider call (TD-011)."""
        return await self._assembler.build(evaluation_id)

    async def evaluate(self, evaluation_id: str) -> EvaluationOutcome:
        """Assemble + evaluate in one call (no external-call transaction concern — used
        where the caller isn't managing a split transaction boundary, e.g. Story 5.1/5.2
        unit paths)."""
        return await self.evaluate_assembled(await self.assemble(evaluation_id))

    async def evaluate_assembled(self, evaluation_input: EvaluationInput) -> EvaluationOutcome:
        """Provider call + validation + platform confidence + honesty floor. Touches **no**
        database — safe to run with no transaction held. `evaluation_id` for logs is taken
        from the input."""
        evaluation_id = evaluation_input.evaluation_id
        provenance = self._provenance()
        # Fingerprint the exact PII-safe input now, so every outcome (success or failure)
        # carries a durable, reproducible identity of what the provider was given.
        fingerprint = fingerprint_input(evaluation_input)
        _log.info(
            "intelligence.evaluate.start",
            evaluation_id=evaluation_id,
            provider=provenance.provider,
            model=provenance.model,
            prompt_version=provenance.prompt_version,
            input_fingerprint=fingerprint,
            # Safe aggregates only — never evidence text or PII.
            evidence_count=sum(len(task.evidence) for task in evaluation_input.tasks),
        )

        try:
            result = await self._provider.evaluate(evaluation_input)
        except ProviderError:
            return self._fail(
                EvaluationFailureReason.PROVIDER_UNAVAILABLE,
                provenance,
                fingerprint,
                "The evaluation provider was unavailable.",
                evaluation_id,
            )

        # 1) Schema / vocabulary: the recommendation must be a known proposal.
        try:
            recommendation = RecommendationProposal(result.recommendation)
        except ValueError:
            return self._fail(
                EvaluationFailureReason.INVALID_PROVIDER_OUTPUT,
                provenance,
                fingerprint,
                "The provider returned an unrecognized result.",
                evaluation_id,
            )

        # 2) Grounding: every claim must cite present evidence.
        if not validate_grounding(result, evaluation_input).ok:
            return self._fail(
                EvaluationFailureReason.UNGROUNDED_OUTPUT,
                provenance,
                fingerprint,
                "The provider's assessment was not grounded in the submitted evidence.",
                evaluation_id,
            )

        # 3) Policy: governed structural checks.
        if not validate_policy(result, evaluation_input).ok:
            return self._fail(
                EvaluationFailureReason.POLICY_VIOLATION,
                provenance,
                fingerprint,
                "The provider's result violated a governed policy check.",
                evaluation_id,
            )

        # 4) Confidence is OURS, then 5) the honesty floor can override direction.
        confidence = self._confidence.compute(evaluation_input, result)
        proposal = self._build_proposal(
            result, recommendation, confidence, evaluation_input, provenance
        )
        proposal = _apply_honesty_floor(proposal, self._floor)

        _log.info(
            "intelligence.evaluate.done",
            evaluation_id=evaluation_id,
            recommendation=proposal.recommendation.value,
            confidence=proposal.confidence,
            escalation_reason=(
                proposal.escalation_reason.value if proposal.escalation_reason else None
            ),
        )
        return EvaluationOutcome(
            provenance=provenance,
            input_fingerprint=fingerprint,
            proposal=proposal,
            usage=result.usage,
        )

    # --- helpers ---------------------------------------------------------- #

    def _build_proposal(
        self,
        result: ProviderResult,
        recommendation: RecommendationProposal,
        confidence: float,
        evaluation_input: EvaluationInput,
        provenance: Provenance,
    ) -> EvaluationProposal:
        task_of = evidence_to_task(evaluation_input)
        assessments = tuple(
            CompetencyAssessment(
                competency=assessment.competency,
                assessment=assessment.assessment,
                # Derive the task link ourselves; keep only citations to present evidence.
                evidence_citations=tuple(
                    EvidenceCitation(evidence_id=c.evidence_id, task_id=task_of[c.evidence_id])
                    for c in assessment.citations
                    if c.evidence_id in task_of
                ),
                provider_signal=assessment.signal,
            )
            for assessment in result.competency_assessments
        )
        escalation_reason = (
            EscalationReason.INSUFFICIENT_EVIDENCE
            if recommendation == RecommendationProposal.ESCALATE
            else None
        )
        return EvaluationProposal(
            recommendation=recommendation,
            confidence=confidence,
            confidence_rationale=(
                "Evidence-reliability signal: how sufficient (competency + evidence "
                "coverage) and how decisive (one-sided vs. mixed grounded observations) "
                "the evidence is. NOT a probability of on-the-job success, and orthogonal "
                "to the direction of the recommendation."
            ),
            escalation_reason=escalation_reason,
            competency_assessments=assessments,
            strengths=self._observations(result.strengths, task_of),
            concerns=self._observations(result.concerns, task_of),
            evidence_coverage=self._coverage(evaluation_input, assessments),
            provenance=provenance,
        )

    @staticmethod
    def _observations(
        raw: list[ProviderObservation], task_of: dict[str, str]
    ) -> tuple[GroundedObservation, ...]:
        # Derive the task link ourselves; keep only citations to present evidence.
        return tuple(
            GroundedObservation(
                text=item.text,
                evidence_citations=tuple(
                    EvidenceCitation(evidence_id=c.evidence_id, task_id=task_of[c.evidence_id])
                    for c in item.citations
                    if c.evidence_id in task_of
                ),
            )
            for item in raw
        )

    @staticmethod
    def _coverage(
        evaluation_input: EvaluationInput,
        assessments: tuple[CompetencyAssessment, ...],
    ) -> EvidenceCoverage:
        competencies = {c.name for c in evaluation_input.role.competencies}
        assessed = {a.competency for a in assessments if a.evidence_citations} & competencies
        return EvidenceCoverage(
            competencies_total=len(competencies),
            competencies_assessed=len(assessed),
            tasks_total=len(evaluation_input.tasks),
            tasks_with_evidence=sum(1 for t in evaluation_input.tasks if t.evidence),
        )

    def _provenance(self) -> Provenance:
        descriptor = self._provider.descriptor
        return Provenance(
            provider=descriptor.provider,
            model=descriptor.model,
            model_version=descriptor.model_version,
            prompt_version=prompt_version(),
            input_schema_version=INPUT_SCHEMA_VERSION,
            output_schema_version=OUTPUT_SCHEMA_VERSION,
            confidence_algorithm_version=CONFIDENCE_ALGORITHM_VERSION,
            generated_at=datetime.now(UTC),
        )

    @staticmethod
    def _fail(
        reason: EvaluationFailureReason,
        provenance: Provenance,
        fingerprint: str,
        message: str,
        evaluation_id: str,
    ) -> EvaluationOutcome:
        _log.warning(
            "intelligence.evaluate.failed",
            evaluation_id=evaluation_id,
            reason=reason.value,
            provider=provenance.provider,
            model=provenance.model,
        )
        return EvaluationOutcome(
            provenance=provenance,
            input_fingerprint=fingerprint,
            failure=EvaluationFailure(reason=reason, message=message),
        )


def _apply_honesty_floor(proposal: EvaluationProposal, floor: float) -> EvaluationProposal:
    """The provider does not get to overrule uncertainty. If platform confidence is below
    the governed floor, the exposed proposal becomes ESCALATE (LOW_CONFIDENCE) regardless
    of what the provider proposed. An already-ESCALATE proposal is left as-is."""
    if proposal.recommendation == RecommendationProposal.ESCALATE:
        return proposal
    if proposal.confidence >= floor:
        return proposal
    return proposal.model_copy(
        update={
            "recommendation": RecommendationProposal.ESCALATE,
            "escalation_reason": EscalationReason.LOW_CONFIDENCE,
        }
    )
