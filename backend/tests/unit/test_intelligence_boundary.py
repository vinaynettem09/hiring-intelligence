"""The AI boundary (INV-012): the assembler builds input ONLY from Role Profile +
Frozen Work Sample + Immutable Evidence, and NEVER from Candidate PII or draft responses.

These tests are the structural guarantee behind the answer to the reviewer's question —
"can a developer accidentally pass Candidate PII to AI using the normal pipeline?" —
which must be *no*.
"""

import ast
import inspect
import json
from pathlib import Path

import pytest
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from support import submitted_evaluation

import app.modules.intelligence.assembler as assembler_module
from app.modules.intelligence.assembler import EvaluationInputAssembler
from app.modules.intelligence.schemas import EvaluationInput
from app.platform.pii import MinimizationResult, PIIMinimizer
from app.shared.errors import BusinessRuleViolation

# --- structural: the assembler cannot even reach PII / drafts ---------------- #

_ASSEMBLER_SOURCE = Path(assembler_module.__file__).read_text(encoding="utf-8")


def _assembler_imports() -> tuple[set[str], set[str]]:
    """The assembler's ACTUAL imports (from the AST — prose in comments is ignored):
    the set of imported module paths and the set of imported symbol names."""
    tree = ast.parse(_ASSEMBLER_SOURCE)
    modules: set[str] = set()
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            modules.add(node.module or "")
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
    return modules, names


def test_assembler_does_not_import_candidate_pii_or_draft_models() -> None:
    modules, names = _assembler_imports()
    # It uses the *evaluation* repository/enum (no PII) — never the Candidate PII model…
    assert "Candidate" not in names, "assembler must not import the Candidate (PII) model"
    assert "app.modules.candidates.models" not in modules
    # …and never the mutable draft response (WorkSampleResponse / its repo / service).
    assert "WorkSampleResponse" not in names
    assert "ResponseRepository" not in names
    assert not any("responses" in module for module in modules), "assembler must not touch drafts"


def test_evaluation_input_dto_has_no_identity_fields() -> None:
    # Walk the whole input DTO tree and prove no field is named like candidate PII.
    # ("name" is intentionally allowed — it is the *competency/role* name, not a person.)
    pii_names = {
        "email",
        "phone",
        "resume",
        "resume_object_key",
        "candidate_name",
        "candidate_email",
        "ssn",
        "address",
    }
    seen: set[type] = set()

    def walk(model: type) -> None:
        if model in seen or not hasattr(model, "model_fields"):
            return
        seen.add(model)
        for field_name, field in model.model_fields.items():
            assert field_name not in pii_names, f"{model.__name__}.{field_name} looks like PII"
            annotation = field.annotation
            for candidate in (annotation, *getattr(annotation, "__args__", ())):
                if isinstance(candidate, type):
                    walk(candidate)

    walk(EvaluationInput)


def test_assembler_signature_takes_no_pii() -> None:
    # The only per-call argument is an evaluation id — never a candidate/name/email.
    params = set(inspect.signature(EvaluationInputAssembler.build).parameters) - {"self"}
    assert params == {"evaluation_id"}


# --- behavioral: real submitted evaluation → PII never crosses --------------- #


async def test_legal_input_path_excludes_pii(session: AsyncSession) -> None:
    setup = await submitted_evaluation(
        session,
        candidate_name="Grace Hopper",
        candidate_email="grace.hopper@navy.mil",
    )
    evaluation_input = await EvaluationInputAssembler(session, setup.tenant).build(
        setup.evaluation_id
    )
    blob = json.dumps(evaluation_input.model_dump(mode="json"))

    assert setup.candidate_name not in blob
    assert setup.candidate_email not in blob
    # But the legitimate, job-relevant context IS present.
    assert evaluation_input.role.role_title == "Data Engineer"
    assert {c.name for c in evaluation_input.role.competencies} == {"SQL", "Python"}
    assert len(evaluation_input.tasks) == 2
    assert all(task.evidence for task in evaluation_input.tasks)


async def test_evidence_text_is_pii_minimized_in_the_input(session: AsyncSession) -> None:
    setup = await submitted_evaluation(
        session,
        competencies=("SQL",),
        answers=("My name is Grace Hopper, email grace@navy.mil — I used a CTE to dedupe.",),
    )
    evaluation_input = await EvaluationInputAssembler(session, setup.tenant).build(
        setup.evaluation_id
    )
    text = evaluation_input.tasks[0].evidence[0].text
    assert "grace@navy.mil" not in text
    assert "Grace Hopper" not in text
    assert "[redacted:email]" in text
    assert "CTE to dedupe" in text  # the substance survives


async def test_input_is_immutable(session: AsyncSession) -> None:
    setup = await submitted_evaluation(session)
    evaluation_input = await EvaluationInputAssembler(session, setup.tenant).build(
        setup.evaluation_id
    )
    # Frozen DTO — a provider cannot mutate what it was handed.
    with pytest.raises(ValidationError):
        evaluation_input.evaluation_id = "hacked"


async def test_pii_minimizer_is_injected(session: AsyncSession) -> None:
    # The minimizer is a seam — a custom one is used if injected (swappable for the real story).
    class _ShoutMinimizer:
        def minimize(self, text: str) -> MinimizationResult:
            return MinimizationResult("MINIMIZED", 0)

    minimizer: PIIMinimizer = _ShoutMinimizer()
    setup = await submitted_evaluation(session, competencies=("SQL",))
    evaluation_input = await EvaluationInputAssembler(
        session, setup.tenant, minimizer=minimizer
    ).build(setup.evaluation_id)
    assert evaluation_input.tasks[0].evidence[0].text == "MINIMIZED"


async def test_minimizer_failure_fails_closed(session: AsyncSession) -> None:
    # If minimization raises, we must NOT egress raw Evidence — assembly fails closed.
    class _BoomMinimizer:
        def minimize(self, text: str) -> MinimizationResult:
            raise RuntimeError("boom")

    setup = await submitted_evaluation(session, competencies=("SQL",))
    with pytest.raises(BusinessRuleViolation) as exc:
        await EvaluationInputAssembler(session, setup.tenant, minimizer=_BoomMinimizer()).build(
            setup.evaluation_id
        )
    assert exc.value.code == "PII_MINIMIZATION_FAILED"
