"""Grounding + policy validation — the provider is untrusted, so its output must be
proven grounded and policy-clean before any of it becomes a proposal."""

from app.modules.intelligence.schemas import (
    CompetencyContext,
    EvaluationInput,
    EvidenceItem,
    RoleContext,
    TaskEvidenceInput,
)
from app.modules.intelligence.validators import validate_grounding, validate_policy
from app.platform.ai import (
    ProviderCitation,
    ProviderCompetencyAssessment,
    ProviderObservation,
    ProviderResult,
)


def _input() -> EvaluationInput:
    return EvaluationInput(
        evaluation_id="eval-1",
        role=RoleContext(
            role_title="Data Engineer",
            bar="senior",
            competencies=(CompetencyContext(name="SQL"),),
        ),
        tasks=(
            TaskEvidenceInput(
                task_id="task-1",
                prompt="p",
                evidence_intent="i",
                competencies=("SQL",),
                evidence=(EvidenceItem(evidence_id="ev-1", text="answer"),),
            ),
        ),
    )


def _result(**overrides: object) -> ProviderResult:
    base: dict[str, object] = {
        "competency_assessments": [
            ProviderCompetencyAssessment(
                competency="SQL", assessment="ok", citations=[ProviderCitation(evidence_id="ev-1")]
            )
        ],
        "recommendation": "PROCEED",
    }
    base.update(overrides)
    return ProviderResult(**base)  # type: ignore[arg-type]


# --- grounding --------------------------------------------------------------- #


def test_valid_citations_pass() -> None:
    assert validate_grounding(_result(), _input()).ok


def test_invented_evidence_id_rejected() -> None:
    result = _result(
        competency_assessments=[
            ProviderCompetencyAssessment(
                competency="SQL", assessment="x", citations=[ProviderCitation(evidence_id="ghost")]
            )
        ]
    )
    check = validate_grounding(result, _input())
    assert not check.ok
    assert any("unknown_evidence_id:ghost" in e for e in check.errors)


def test_evidence_from_another_evaluation_rejected() -> None:
    # An id that exists — but for a different evaluation — is simply not in THIS input.
    other_eval_evidence = _result(
        competency_assessments=[
            ProviderCompetencyAssessment(
                competency="SQL",
                assessment="x",
                citations=[ProviderCitation(evidence_id="ev-from-eval-2")],
            )
        ]
    )
    assert not validate_grounding(other_eval_evidence, _input()).ok


def test_assessment_without_citations_rejected() -> None:
    result = _result(
        competency_assessments=[
            ProviderCompetencyAssessment(competency="SQL", assessment="unsupported claim")
        ]
    )
    check = validate_grounding(result, _input())
    assert not check.ok
    assert any("assessment_without_citations" in e for e in check.errors)


def test_escalate_with_no_assessments_is_vacuously_grounded() -> None:
    # ESCALATE makes no competency claims → nothing to ground.
    result = ProviderResult(competency_assessments=[], recommendation="ESCALATE")
    assert validate_grounding(result, _input()).ok


def test_grounded_strength_passes() -> None:
    result = _result(
        strengths=[
            ProviderObservation(
                text="Strong SQL.", citations=[ProviderCitation(evidence_id="ev-1")]
            )
        ]
    )
    assert validate_grounding(result, _input()).ok


def test_uncited_strength_is_rejected() -> None:
    # The side channel the reviewer flagged: an uncited "excellent leadership" claim.
    result = _result(strengths=[ProviderObservation(text="Excellent leadership.", citations=[])])
    check = validate_grounding(result, _input())
    assert not check.ok
    assert any("strength_without_citations" in e for e in check.errors)


def test_concern_citing_unknown_evidence_is_rejected() -> None:
    result = _result(
        concerns=[
            ProviderObservation(text="Weak.", citations=[ProviderCitation(evidence_id="ghost")])
        ]
    )
    check = validate_grounding(result, _input())
    assert not check.ok
    assert any("unknown_evidence_id:ghost" in e for e in check.errors)


# --- policy ------------------------------------------------------------------ #


def test_valid_recommendation_and_signal_pass_policy() -> None:
    assert validate_policy(_result(provider_confidence=0.7), _input()).ok


def test_out_of_vocabulary_recommendation_fails_policy() -> None:
    assert not validate_policy(_result(recommendation="DEFINITELY_HIRE"), _input()).ok


def test_out_of_range_signal_fails_policy() -> None:
    assert not validate_policy(_result(provider_confidence=5.0), _input()).ok
