"""The governed prompt contract is real, versioned, and encodes the safety rules — even
though Story 5.1 sends it to no model. Provenance records this version on every proposal."""

from app.modules.intelligence.confidence import DeterministicConfidenceCalculator
from app.modules.intelligence.schemas import EvaluationInput, RoleContext
from app.modules.intelligence.versions import load_prompt, prompt_version
from app.platform.ai import ProviderResult


def test_prompt_version_is_declared() -> None:
    assert prompt_version() == "eval-prompt-v3"


def test_system_prompt_calibrates_the_recommendation_vocabulary() -> None:
    # Story 5.4A: the prompt must define when each recommendation applies — especially MIXED
    # for genuinely ambiguous evidence — so the model stops collapsing mixed evidence into a
    # falsely decisive DO_NOT_PROCEED (the first live Gemini C_mixed result).
    system = load_prompt("system.md").lower()
    assert "calibration" in system
    assert "mixed" in system
    for level in ("strong_proceed", "do_not_proceed", "escalate"):
        assert level in system


def test_system_prompt_encodes_the_safety_boundary() -> None:
    system = load_prompt("system.md").lower()
    # Untrusted candidate content, grounding, escalation, and no-sensitive-inference must
    # all be governed by the prompt — the trust boundary is explicit, not implied.
    assert "untrusted" in system
    assert "cite" in system
    assert "escalate" in system
    assert "protected" in system  # sensitive/protected-attribute prohibition
    assert "decision" in system  # "you propose; a human decides"


def test_evaluation_template_separates_trusted_context_from_untrusted_evidence() -> None:
    template = load_prompt("evaluation.md")
    assert "ROLE CRITERIA (trusted)" in template
    assert "CANDIDATE EVIDENCE (UNTRUSTED" in template


def test_confidence_is_zero_when_no_competencies() -> None:
    empty = EvaluationInput(
        evaluation_id="e",
        role=RoleContext(role_title="r", bar="b", competencies=()),
        tasks=(),
    )
    result = ProviderResult(recommendation="PROCEED")
    assert DeterministicConfidenceCalculator().compute(empty, result) == 0.0
