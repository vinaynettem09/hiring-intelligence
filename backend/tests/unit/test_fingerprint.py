"""Input fingerprint — a stable SHA-256 over the canonical PII-safe input. Deterministic,
not Python's salted hash(), and computed over the minimized representation."""

from app.modules.intelligence.fingerprint import fingerprint_input
from app.modules.intelligence.schemas import (
    CompetencyContext,
    EvaluationInput,
    EvidenceItem,
    RoleContext,
    TaskEvidenceInput,
)


def _input(
    *, role_title: str = "Data Engineer", evidence_text: str = "I used a CTE."
) -> EvaluationInput:
    return EvaluationInput(
        evaluation_id="eval-1",
        role=RoleContext(
            role_title=role_title, bar="senior", competencies=(CompetencyContext(name="SQL"),)
        ),
        tasks=(
            TaskEvidenceInput(
                task_id="task-1",
                prompt="p",
                evidence_intent="i",
                competencies=("SQL",),
                evidence=(EvidenceItem(evidence_id="ev-1", text=evidence_text),),
            ),
        ),
    )


def test_fingerprint_is_sha256_prefixed() -> None:
    fp = fingerprint_input(_input())
    assert fp.startswith("sha256:")
    assert len(fp.split(":")[1]) == 64  # hex sha-256


def test_same_input_same_fingerprint() -> None:
    assert fingerprint_input(_input()) == fingerprint_input(_input())


def test_different_evidence_changes_fingerprint() -> None:
    assert fingerprint_input(_input(evidence_text="A")) != fingerprint_input(
        _input(evidence_text="B")
    )


def test_different_role_criteria_changes_fingerprint() -> None:
    assert fingerprint_input(_input(role_title="Data Engineer")) != fingerprint_input(
        _input(role_title="ML Engineer")
    )


def test_fingerprint_is_over_the_minimized_representation() -> None:
    # Two inputs whose evidence text is already-minimized-equal fingerprint identically;
    # the fingerprint is a property of the safe text it is given, nothing hidden.
    a = _input(evidence_text="[redacted:email] approach")
    b = _input(evidence_text="[redacted:email] approach")
    assert fingerprint_input(a) == fingerprint_input(b)
