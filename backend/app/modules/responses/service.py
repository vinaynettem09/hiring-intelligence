"""Candidate work-sample service.

Every authoritative operation re-checks THREE gates, server-side, failing closed:
  1. valid invitation (the token resolves the evaluation/campaign/org — the client never
     supplies ids),
  2. ACTIVE consent (checked every time — not assumed from an earlier page),
  3. an ACTIVE campaign with a frozen work sample.

Drafts are mutable. **Submission** (Story 4.5) is the explicit, atomic, irreversible
promotion of the final drafts into immutable Evidence — not a status flag on the draft.
No AI call anywhere here.
"""

from collections.abc import Sequence
from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.audit.service import AuditService
from app.modules.campaigns.enums import CampaignStatus
from app.modules.candidates.enums import EvaluationStatus
from app.modules.candidates.models import CandidateEvaluation
from app.modules.candidates.repository import CandidateEvaluationRepository
from app.modules.consent.service import ConsentService
from app.modules.evidence.repository import EvidenceRepository
from app.modules.invitations.service import CandidateAccessService, ResolvedInvitation
from app.modules.responses.repository import ResponseRepository
from app.modules.responses.schemas import (
    CandidateTaskView,
    CandidateWorkSample,
    SavedResponse,
    SubmissionResult,
)
from app.modules.worksample.models import StructuredWorkSample, WorkSampleTask
from app.modules.worksample.repository import WorkSampleRepository
from app.shared.errors import (
    AuthorizationError,
    BusinessRuleViolation,
    ConflictError,
    NotFoundError,
)


class _Ready:
    """The validated candidate context for one request."""

    def __init__(
        self,
        resolved: ResolvedInvitation,
        evaluation: CandidateEvaluation,
        work_sample: StructuredWorkSample,
        tasks: Sequence[WorkSampleTask],
    ) -> None:
        self.resolved = resolved
        self.evaluation = evaluation
        self.work_sample = work_sample
        self.tasks = tasks

    @property
    def evaluation_id(self) -> str:
        return self.evaluation.id

    @property
    def organization_id(self) -> str:
        return self.resolved.invitation.organization_id

    @property
    def submitted(self) -> bool:
        return self.evaluation.status == EvaluationStatus.SUBMITTED.value


class CandidateWorkSampleService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session
        self._access = CandidateAccessService(session)
        self._consent = ConsentService(session)
        self._responses = ResponseRepository(session)
        self._evidence = EvidenceRepository(session)
        self._audit = AuditService(session)

    async def get_work_sample(self, token: str) -> CandidateWorkSample:
        ready = await self._ready(token)
        drafts = {
            r.work_sample_task_id: r.response_text
            for r in await self._responses.list_for_evaluation(ready.evaluation_id)
        }
        return CandidateWorkSample(
            organization_name=ready.resolved.organization.name,
            role_title=ready.resolved.campaign.role_title,
            title=ready.work_sample.title,
            introduction=ready.work_sample.introduction,
            estimated_minutes=sum(t.expected_effort_minutes or 0 for t in ready.tasks),
            tasks=[
                CandidateTaskView(
                    task_id=task.id,
                    order=index + 1,
                    prompt=task.prompt,
                    instructions=task.instructions,
                    expected_effort_minutes=task.expected_effort_minutes,
                    response_text=drafts.get(task.id, ""),
                )
                for index, task in enumerate(ready.tasks)
            ],
            submitted=ready.submitted,
            submitted_at=ready.evaluation.submitted_at,
        )

    async def save_response(self, token: str, task_id: str, response_text: str) -> SavedResponse:
        ready = await self._ready(token)
        if ready.submitted:
            raise ConflictError(
                "This work sample has already been submitted and can no longer be edited.",
                code="WORK_SAMPLE_ALREADY_SUBMITTED",
            )
        if task_id not in {task.id for task in ready.tasks}:
            raise NotFoundError("Task not found.", code="TASK_NOT_FOUND")

        if await self._responses.count_for_evaluation(ready.evaluation_id) == 0:
            await self._audit.record(
                organization_id=ready.organization_id,
                actor_type="candidate",
                action="work_sample.started",
                target_type="candidate_evaluation",
                target_id=ready.evaluation_id,
                details={"work_sample_id": ready.work_sample.id},
            )

        response = await self._responses.upsert(
            organization_id=ready.organization_id,
            evaluation_id=ready.evaluation_id,
            task_id=task_id,
            response_text=response_text,
        )
        return SavedResponse(task_id=task_id, updated_at=response.updated_at)

    async def submit(self, token: str) -> SubmissionResult:
        """The authoritative transition. Atomic within the request transaction: validate
        everything → snapshot Evidence → mark submitted → audit. Any failure raises
        before committing, so nothing partial persists. Idempotent: a second submission
        returns the existing result without creating duplicate Evidence or audit."""
        ready = await self._ready(token)  # re-checks access + consent + active/frozen

        if ready.submitted:  # idempotent — no duplicate Evidence, no second audit
            return self._result(
                ready, await self._evidence.count_for_evaluation(ready.evaluation_id)
            )

        drafts = {
            r.work_sample_task_id: r.response_text
            for r in await self._responses.list_for_evaluation(ready.evaluation_id)
        }
        missing = [
            index + 1
            for index, task in enumerate(ready.tasks)
            if not (drafts.get(task.id) or "").strip()
        ]
        if missing:
            raise BusinessRuleViolation(
                "Answer every task before submitting.",
                code="WORK_SAMPLE_INCOMPLETE",
                metadata={
                    "total_tasks": len(ready.tasks),
                    "answered_tasks": len(ready.tasks) - len(missing),
                    "missing_task_positions": missing,
                },
            )

        # Snapshot verbatim, in task order → immutable Evidence.
        evidence = await self._evidence.create_submission_evidence(
            organization_id=ready.organization_id,
            candidate_evaluation_id=ready.evaluation_id,
            snapshots=[(task.id, drafts[task.id]) for task in ready.tasks],
        )
        ready.evaluation.status = EvaluationStatus.SUBMITTED.value
        ready.evaluation.submitted_at = datetime.now(UTC)
        await self._audit.record(
            organization_id=ready.organization_id,
            actor_type="candidate",
            action="work_sample.submitted",
            target_type="candidate_evaluation",
            target_id=ready.evaluation_id,
            details={
                "work_sample_id": ready.work_sample.id,
                "task_count": len(ready.tasks),
                "evidence_count": len(evidence),
            },
        )
        return self._result(ready, len(evidence))

    @staticmethod
    def _result(ready: "_Ready", evidence_count: int) -> SubmissionResult:
        # `_result` is only reached once the evaluation is submitted, so submitted_at is set.
        submitted_at = ready.evaluation.submitted_at or datetime.now(UTC)
        if submitted_at.tzinfo is None:
            submitted_at = submitted_at.replace(tzinfo=UTC)  # sqlite returns naive; treat as UTC
        return SubmissionResult(
            organization_name=ready.resolved.organization.name,
            role_title=ready.resolved.campaign.role_title,
            submitted_at=submitted_at,
            evidence_count=evidence_count,
        )

    async def _ready(self, token: str) -> _Ready:
        resolved = await self._access.resolve_invitation(token)  # gate 1 (INVITATION_*)
        evaluation_id = resolved.invitation.candidate_evaluation_id

        if not await self._consent.has_active_consent(evaluation_id):  # gate 2 — every time
            raise AuthorizationError(
                "Consent is required before continuing.", code="CONSENT_REQUIRED"
            )
        if resolved.campaign.status != CampaignStatus.ACTIVE.value:  # gate 3
            raise ConflictError("This work sample isn't available.", code="WORK_SAMPLE_UNAVAILABLE")
        org_id = resolved.invitation.organization_id
        work_samples = WorkSampleRepository(self._session, org_id)
        work_sample = await work_samples.get_for_campaign(resolved.campaign.id)
        if work_sample is None:
            raise ConflictError("This work sample isn't available.", code="WORK_SAMPLE_UNAVAILABLE")
        evaluation = await CandidateEvaluationRepository(self._session, org_id).get(evaluation_id)
        if evaluation is None:  # pragma: no cover - resolved from a valid invitation
            raise NotFoundError("Evaluation not found.", code="EVALUATION_NOT_FOUND")
        tasks = await work_samples.list_tasks(work_sample.id)
        return _Ready(resolved, evaluation, work_sample, tasks)
