"""Work Sample application service.

Owns the whole definition operation and the readiness rules — the frontend mirrors
these for UX but the backend is authoritative. Small `_validate_*` helpers, orchestrated.

Boundaries kept clean: the work sample derives from the campaign (competency names come
from the campaign's Role Profile); it never redefines what "good" means, and it holds no
scoring/AI. Editable only while the campaign is a draft; frozen once active (INV-003).
"""

from collections.abc import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.campaigns.enums import CampaignStatus
from app.modules.campaigns.models import Campaign
from app.modules.campaigns.repository import CampaignRepository
from app.modules.worksample.models import WorkSampleTask
from app.modules.worksample.repository import WorkSampleRepository
from app.modules.worksample.schemas import (
    CompetencyCoverage,
    DefineWorkSampleRequest,
    WorkSampleResponse,
    WorkSampleTaskResponse,
)
from app.shared.errors import (
    BusinessRuleViolation,
    ConflictError,
    NotFoundError,
    ValidationError,
)


def _campaign_competencies(campaign: Campaign) -> list[str]:
    profile = campaign.role_profile or {}
    return [c["name"] for c in profile.get("competencies", []) if c.get("name")]


def _coverage(
    competency_names: Sequence[str], tasks: Sequence[WorkSampleTask]
) -> CompetencyCoverage:
    measured = {name for task in tasks for name in task.competencies}
    covered = [n for n in competency_names if n in measured]
    uncovered = [n for n in competency_names if n not in measured]
    return CompetencyCoverage(total=len(competency_names), covered=covered, uncovered=uncovered)


def _validate_definition(request: DefineWorkSampleRequest, competency_names: list[str]) -> None:
    """Per-task validity checked at save (a task must be well-formed and reference real
    competencies). Overall completeness (≥1 task, full coverage) is an activation gate."""
    known = set(competency_names)
    for index, task in enumerate(request.tasks):
        if not task.prompt.strip():
            raise ValidationError(
                "Each task needs a candidate prompt.",
                code="WORK_SAMPLE_INVALID",
                metadata={"task": index, "field": "prompt"},
            )
        if not task.evidence_intent.strip():
            raise ValidationError(
                "Each task needs an evidence intent.",
                code="WORK_SAMPLE_INVALID",
                metadata={"task": index, "field": "evidence_intent"},
            )
        unknown = [c for c in task.competencies if c not in known]
        if unknown:
            raise ValidationError(
                "A task references competencies that aren't in this campaign.",
                code="WORK_SAMPLE_INVALID",
                metadata={"task": index, "unknown_competencies": unknown},
            )


class WorkSampleService:
    def __init__(self, session: AsyncSession, tenant_id: str) -> None:
        self._repo = WorkSampleRepository(session, tenant_id)
        self._campaigns = CampaignRepository(session, tenant_id)

    async def get(self, campaign_id: str) -> WorkSampleResponse:
        campaign = await self._require_campaign(campaign_id)
        work_sample = await self._repo.get_for_campaign(campaign_id)
        tasks = await self._repo.list_tasks(work_sample.id) if work_sample else []
        return self._to_response(campaign, work_sample, tasks)

    async def define(
        self, campaign_id: str, request: DefineWorkSampleRequest
    ) -> WorkSampleResponse:
        campaign = await self._require_campaign(campaign_id)
        if campaign.status != CampaignStatus.DRAFT.value:
            raise ConflictError(
                "The work sample can only be edited while the campaign is a draft.",
                code="WORK_SAMPLE_LOCKED",
                metadata={"current_status": campaign.status},
            )
        _validate_definition(request, _campaign_competencies(campaign))

        work_sample = await self._repo.upsert_header(
            campaign_id, title=request.title.strip(), introduction=request.introduction
        )
        await self._repo.replace_tasks(
            work_sample.id,
            [
                {
                    "prompt": task.prompt.strip(),
                    "instructions": task.instructions,
                    "evidence_intent": task.evidence_intent.strip(),
                    "task_type": task.task_type.value,
                    "competencies": task.competencies,
                    "expected_effort_minutes": task.expected_effort_minutes,
                }
                for task in request.tasks
            ],
        )
        tasks = await self._repo.list_tasks(work_sample.id)
        return self._to_response(campaign, work_sample, tasks)

    async def assert_ready_for_activation(
        self, campaign_id: str, competency_names: list[str]
    ) -> None:
        """Activation gate (called by CampaignService): a valid evidence instrument must
        exist — ≥1 task and every campaign competency covered (INV-011). Fails closed."""
        work_sample = await self._repo.get_for_campaign(campaign_id)
        if work_sample is None:
            raise BusinessRuleViolation(
                "Add a structured work sample before activating.",
                code="CAMPAIGN_INCOMPLETE",
                metadata={"missing": "work_sample"},
            )
        tasks = await self._repo.list_tasks(work_sample.id)
        if not tasks:
            raise BusinessRuleViolation(
                "The work sample needs at least one task.",
                code="CAMPAIGN_INCOMPLETE",
                metadata={"missing": "tasks"},
            )
        coverage = _coverage(competency_names, tasks)
        if coverage.uncovered:
            raise BusinessRuleViolation(
                "Every competency needs at least one task before activation.",
                code="CAMPAIGN_INCOMPLETE",
                metadata={"uncovered_competencies": coverage.uncovered},
            )

    async def _require_campaign(self, campaign_id: str) -> Campaign:
        campaign = await self._campaigns.get(campaign_id)  # tenant-scoped → 404 if not ours
        if campaign is None:
            raise NotFoundError("Campaign not found.", code="CAMPAIGN_NOT_FOUND")
        return campaign

    @staticmethod
    def _to_response(
        campaign: Campaign,
        work_sample: object | None,
        tasks: Sequence[WorkSampleTask],
    ) -> WorkSampleResponse:
        names = _campaign_competencies(campaign)
        return WorkSampleResponse(
            exists=work_sample is not None,
            editable=campaign.status == CampaignStatus.DRAFT.value,
            campaign_id=campaign.id,
            role_title=campaign.role_title,
            title=getattr(work_sample, "title", ""),
            introduction=getattr(work_sample, "introduction", None),
            tasks=[
                WorkSampleTaskResponse(
                    id=task.id,
                    prompt=task.prompt,
                    instructions=task.instructions,
                    evidence_intent=task.evidence_intent,
                    task_type=task.task_type,  # type: ignore[arg-type]
                    competencies=list(task.competencies),
                    display_order=task.display_order,
                    expected_effort_minutes=task.expected_effort_minutes,
                )
                for task in tasks
            ],
            estimated_minutes=sum(t.expected_effort_minutes or 0 for t in tasks),
            coverage=_coverage(names, tasks),
        )
