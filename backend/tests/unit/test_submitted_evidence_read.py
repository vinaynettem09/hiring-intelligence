"""Recruiter submitted-evidence read (Story 5.4B — the citation -> source trust anchor).

Proves: the recruiter can retrieve the verbatim submitted evidence behind an evaluation,
ordered by task, keyed by the same ids citations carry; and the read is tenant-scoped (a
cross-tenant id is a 404, never a leak).
"""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from support import submitted_evaluation

from app.modules.evidence.service import SubmittedEvidenceReadService
from app.shared.errors import NotFoundError


async def test_returns_submitted_evidence_in_task_order(session: AsyncSession) -> None:
    setup = await submitted_evaluation(
        session,
        competencies=("SQL", "Python"),
        answers=("My SQL windowed-CTE answer.", "My Python answer."),
    )
    result = await SubmittedEvidenceReadService(session, setup.tenant).get_for_candidate_evaluation(
        setup.evaluation_id
    )

    assert result.candidate_evaluation_id == setup.evaluation_id
    assert len(result.items) == 2
    # Ordered by the frozen task position: Task 1, Task 2.
    assert [item.task_number for item in result.items] == [1, 2]
    assert result.items[0].response_text == "My SQL windowed-CTE answer."
    assert result.items[1].response_text == "My Python answer."
    # Each item carries the ids a citation matches on + the task prompt/intent for context.
    for item in result.items:
        assert item.evidence_id
        assert item.task_id in set(setup.task_ids)
        assert item.task_prompt
        assert item.evidence_intent


async def test_evidence_read_is_tenant_scoped(session: AsyncSession) -> None:
    a = await submitted_evaluation(session, org="Acme", user_email="a@acme.com")
    b = await submitted_evaluation(session, org="Globex", user_email="b@globex.com")

    # Org B asking for Org A's evaluation must 404 — never confirm it exists, never leak text.
    with pytest.raises(NotFoundError) as exc:
        await SubmittedEvidenceReadService(session, b.tenant).get_for_candidate_evaluation(
            a.evaluation_id
        )
    assert exc.value.code == "CANDIDATE_EVALUATION_NOT_FOUND"


async def test_unknown_evaluation_is_not_found(session: AsyncSession) -> None:
    setup = await submitted_evaluation(session)
    with pytest.raises(NotFoundError):
        await SubmittedEvidenceReadService(session, setup.tenant).get_for_candidate_evaluation(
            "does-not-exist"
        )
