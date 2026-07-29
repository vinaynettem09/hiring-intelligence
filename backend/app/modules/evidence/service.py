"""Recruiter-facing read of submitted evidence — the trust anchor behind an evaluation.

A recruiter drilling into an evaluation citation needs to see the *actual* submitted
answer. Authority is enforced first: the candidate evaluation must belong to the caller's
tenant (a cross-tenant id reads as 404, never confirming existence). Evidence is immutable
and PII-free at the response level; recruiter authority over the candidate is what makes
showing the verbatim response appropriate here (this is NOT the AI's minimized input).
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.candidates.repository import CandidateEvaluationRepository
from app.modules.evidence.repository import EvidenceRepository
from app.modules.evidence.schemas import SubmittedEvidenceItem, SubmittedEvidenceResponse
from app.shared.errors import NotFoundError


class SubmittedEvidenceReadService:
    def __init__(self, session: AsyncSession, tenant_id: str) -> None:
        self._session = session
        self._tenant_id = tenant_id

    async def get_for_candidate_evaluation(
        self, candidate_evaluation_id: str
    ) -> SubmittedEvidenceResponse:
        # Authority gate: tenant-scoped — another org's evaluation is indistinguishable
        # from a missing one (404, never 403).
        owned = await CandidateEvaluationRepository(self._session, self._tenant_id).get(
            candidate_evaluation_id
        )
        if owned is None:
            raise NotFoundError(
                "Candidate evaluation not found.", code="CANDIDATE_EVALUATION_NOT_FOUND"
            )

        rows = await EvidenceRepository(self._session).list_with_tasks_for_evaluation(
            candidate_evaluation_id=candidate_evaluation_id, organization_id=self._tenant_id
        )
        return SubmittedEvidenceResponse(
            candidate_evaluation_id=candidate_evaluation_id,
            items=[
                SubmittedEvidenceItem(
                    evidence_id=evidence.id,
                    task_id=task.id,
                    task_number=task.display_order + 1,
                    task_prompt=task.prompt,
                    evidence_intent=task.evidence_intent,
                    response_text=evidence.response_text,
                    captured_at=evidence.captured_at,
                )
                for evidence, task in rows
            ],
        )
