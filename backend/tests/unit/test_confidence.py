"""Confidence v2 (Story 5.4A) — platform-computed, deterministic, honest.

``confidence = sufficiency x decisiveness`` (capped when the provider escalated). These
tests pin the reviewer's point-12 properties: coverage alone no longer implies certainty;
evidence length is never a proxy for quality; a clearly-supported negative call keeps HIGH
confidence; mixed evidence lowers it; insufficient evidence caps and escalates; the model's
self-confidence can never drive the number; and identical validated inputs are deterministic.
"""

from datetime import UTC, datetime

from app.modules.intelligence.confidence import DeterministicConfidenceCalculator
from app.modules.intelligence.enums import EscalationReason, RecommendationProposal
from app.modules.intelligence.schemas import (
    CompetencyContext,
    EvaluationInput,
    EvaluationProposal,
    EvidenceCoverage,
    EvidenceItem,
    Provenance,
    RoleContext,
    TaskEvidenceInput,
)
from app.modules.intelligence.service import _apply_honesty_floor
from app.platform.ai import (
    ProviderCitation,
    ProviderCompetencyAssessment,
    ProviderObservation,
    ProviderResult,
)

CALC = DeterministicConfidenceCalculator()


def _input(
    *, competencies: tuple[str, ...], evidence_for: set[str], text: str = "x"
) -> EvaluationInput:
    """One task per competency; a task carries evidence only if its competency is in
    `evidence_for` (lets us model missing evidence for some competencies)."""
    return EvaluationInput(
        evaluation_id="e",
        role=RoleContext(
            role_title="r",
            bar="b",
            competencies=tuple(CompetencyContext(name=c) for c in competencies),
        ),
        tasks=tuple(
            TaskEvidenceInput(
                task_id=f"t-{c}",
                prompt="p",
                evidence_intent="i",
                competencies=(c,),
                evidence=(
                    (EvidenceItem(evidence_id=f"ev-{c}", text=text),) if c in evidence_for else ()
                ),
            )
            for c in competencies
        ),
    )


def _obs(n: int) -> list[ProviderObservation]:
    """n grounded observations (their citations are irrelevant to the calc — it counts them)."""
    return [ProviderObservation(text="o", citations=[ProviderCitation(evidence_id="ev")])] * n


def _result(
    assessed: tuple[str, ...],
    *,
    recommendation: str = "PROCEED",
    strengths: int = 0,
    concerns: int = 0,
    provider_confidence: float | None = None,
) -> ProviderResult:
    return ProviderResult(
        competency_assessments=[
            ProviderCompetencyAssessment(
                competency=c, assessment="ok", citations=[ProviderCitation(evidence_id=f"ev-{c}")]
            )
            for c in assessed
        ],
        strengths=_obs(strengths),
        concerns=_obs(concerns),
        recommendation=recommendation,
        provider_confidence=provider_confidence,
    )


# --- sufficiency x decisiveness --------------------------------------------------------- #


def test_full_coverage_decisive_is_high_and_deterministic() -> None:
    inp = _input(competencies=("SQL", "Python"), evidence_for={"SQL", "Python"})
    result = _result(("SQL", "Python"), strengths=2)  # one-sided → decisive
    assert CALC.compute(inp, result) == 1.0
    assert CALC.compute(inp, result) == CALC.compute(inp, result)  # same inputs → same number


def test_missing_competency_evidence_lowers_confidence() -> None:
    full = CALC.compute(
        _input(competencies=("SQL", "Python"), evidence_for={"SQL", "Python"}),
        _result(("SQL", "Python"), strengths=1),
    )
    partial = CALC.compute(
        _input(competencies=("SQL", "Python"), evidence_for={"SQL"}),
        _result(("SQL",), strengths=1),  # only one competency assessed/grounded
    )
    assert partial < full


def test_mixed_evidence_lowers_confidence_below_one_sided() -> None:
    inp = _input(competencies=("SQL", "Python"), evidence_for={"SQL", "Python"})
    decisive = CALC.compute(inp, _result(("SQL", "Python"), strengths=2))  # one-sided
    mixed = CALC.compute(inp, _result(("SQL", "Python"), strengths=1, concerns=1))  # both sides
    assert mixed < decisive
    assert mixed == 0.5  # full coverage x maximally-ambiguous decisiveness floor


def test_confidence_is_orthogonal_to_recommendation_direction() -> None:
    """Same structure, opposite direction → same confidence. Direction never moves it."""
    inp = _input(competencies=("SQL",), evidence_for={"SQL"})
    proceed = CALC.compute(
        inp, _result(("SQL",), recommendation="PROCEED", strengths=1, concerns=1)
    )
    reject = CALC.compute(
        inp, _result(("SQL",), recommendation="DO_NOT_PROCEED", strengths=1, concerns=1)
    )
    assert proceed == reject


def test_one_sided_negative_keeps_high_confidence() -> None:
    """A clearly-supported DO_NOT_PROCEED (concerns only, full coverage) stays HIGH — the
    honesty floor must not touch it. High confidence + negative direction is valid."""
    inp = _input(competencies=("SQL",), evidence_for={"SQL"})
    result = _result(("SQL",), recommendation="DO_NOT_PROCEED", concerns=3)  # one-sided
    confidence = CALC.compute(inp, result)
    assert confidence == 1.0
    proposal = _apply_honesty_floor(
        _proposal(RecommendationProposal.DO_NOT_PROCEED, confidence), 0.5
    )
    assert proposal.recommendation == RecommendationProposal.DO_NOT_PROCEED


def test_provider_escalation_caps_confidence_low() -> None:
    inp = _input(competencies=("SQL", "Python"), evidence_for={"SQL", "Python"})
    escalated = CALC.compute(
        inp, _result(("SQL", "Python"), recommendation="ESCALATE", strengths=2)
    )
    assert escalated <= 0.2


# --- point 12(f): provider self-confidence cannot control platform confidence ----------- #


def test_provider_self_confidence_is_not_platform_confidence() -> None:
    inp = _input(competencies=("SQL",), evidence_for=set())  # no evidence at all
    result = _result((), recommendation="PROCEED", provider_confidence=0.99)  # model near-certain
    assert CALC.compute(inp, result) == 0.0  # platform ignores the model's self-confidence


def test_provider_self_confidence_cannot_raise_a_mixed_result() -> None:
    inp = _input(competencies=("SQL",), evidence_for={"SQL"})
    mixed = _result(("SQL",), strengths=1, concerns=1)
    confident = mixed.model_copy(update={"provider_confidence": 0.99})
    assert CALC.compute(inp, mixed) == CALC.compute(inp, confident) == 0.5


# --- point 12(b)/(c): length is never a proxy for quality ------------------------------- #


def test_confidence_ignores_evidence_length() -> None:
    """Verbose fluff cannot raise confidence and a concise answer cannot lower it — the
    calculator never reads evidence text, only structure. Two inputs identical except the
    length of the evidence text produce the SAME confidence."""
    concise = _input(competencies=("SQL",), evidence_for={"SQL"}, text="rn=1 per user.")
    verbose = _input(competencies=("SQL",), evidence_for={"SQL"}, text="deduplication " * 200)
    result = _result(("SQL",), strengths=1)
    assert CALC.compute(concise, result) == CALC.compute(verbose, result)


# --- point 12(a): coverage alone no longer yields certainty (TD-016 fix) ---------------- #


def test_coverage_alone_no_longer_yields_certainty() -> None:
    """The v1 flaw (TD-016): full coverage → confidence ~1.0 even for genuinely mixed
    evidence. Under v2, full coverage with a balanced strength/concern split is 0.5, not
    ~1.0 — coverage is necessary but no longer sufficient for certainty."""
    inp = _input(competencies=("SQL", "Python"), evidence_for={"SQL", "Python"})
    mixed = _result(("SQL", "Python"), strengths=1, concerns=1)
    assert CALC.compute(inp, mixed) < 1.0


def test_no_observations_is_thin_signal() -> None:
    """A grounded assessment that surfaces NO strength or concern is thin: decisiveness
    floors, so full coverage alone caps at 0.5 rather than reading as near-certain."""
    inp = _input(competencies=("SQL",), evidence_for={"SQL"})
    assert CALC.compute(inp, _result(("SQL",))) == 0.5


def test_substanceless_evidence_escalated_by_model_scores_low_and_escalates() -> None:
    """When the model behaves correctly on substanceless evidence it ESCALATEs; that caps
    confidence low and the honesty floor keeps the exposed outcome an ESCALATE. (A model
    that instead fabricates a clean assessment is a model-quality failure caught by the A-G
    behavioral gates, not by this number — see TD-016 residual.)"""
    inp = _input(competencies=("SQL",), evidence_for={"SQL"}, text="SQL is useful.")
    confidence = CALC.compute(inp, _result(("SQL",), recommendation="ESCALATE", concerns=1))
    assert confidence <= 0.2
    floored = _apply_honesty_floor(_proposal(RecommendationProposal.ESCALATE, confidence), 0.5)
    assert floored.recommendation == RecommendationProposal.ESCALATE


# --- honesty floor (unchanged contract) ------------------------------------------------- #


def test_honesty_floor_forces_escalate_below_threshold() -> None:
    floored = _apply_honesty_floor(_proposal(RecommendationProposal.PROCEED, 0.3), floor=0.5)
    assert floored.recommendation == RecommendationProposal.ESCALATE
    assert floored.escalation_reason == EscalationReason.LOW_CONFIDENCE


def test_honesty_floor_leaves_confident_proposal_untouched() -> None:
    floored = _apply_honesty_floor(_proposal(RecommendationProposal.DO_NOT_PROCEED, 0.9), floor=0.5)
    # High confidence + DO_NOT_PROCEED is valid — direction and confidence are orthogonal.
    assert floored.recommendation == RecommendationProposal.DO_NOT_PROCEED
    assert floored.escalation_reason is None


def test_high_confidence_proceed_is_valid() -> None:
    floored = _apply_honesty_floor(_proposal(RecommendationProposal.PROCEED, 0.95), floor=0.5)
    assert floored.recommendation == RecommendationProposal.PROCEED


def _proposal(recommendation: RecommendationProposal, confidence: float) -> EvaluationProposal:
    provenance = Provenance(
        provider="mock",
        model="deterministic-mock",
        model_version="v1",
        prompt_version="eval-prompt-v3",
        input_schema_version="eval-input-v1",
        output_schema_version="eval-proposal-v1",
        confidence_algorithm_version="confidence-v2",
        generated_at=datetime(2026, 1, 1, tzinfo=UTC),
    )
    return EvaluationProposal(
        recommendation=recommendation,
        confidence=confidence,
        confidence_rationale="test",
        competency_assessments=(),
        strengths=(),
        concerns=(),
        evidence_coverage=EvidenceCoverage(
            competencies_total=1, competencies_assessed=1, tasks_total=1, tasks_with_evidence=1
        ),
        provenance=provenance,
    )
