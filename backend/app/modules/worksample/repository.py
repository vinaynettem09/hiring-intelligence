"""Work-sample persistence (tenant-scoped through the campaign, INV-000). Editing is
replace-all while the campaign is a draft, which is safe because no candidate evidence
references tasks until the campaign is active (and then it's frozen). Repositories
persist (`add`/`flush`); they never commit."""

from collections.abc import Sequence
from typing import Any

from sqlalchemy import delete, select

from app.modules.worksample.models import StructuredWorkSample, WorkSampleTask
from app.shared.ids import new_id
from app.shared.repository import TenantScopedRepository


class WorkSampleRepository(TenantScopedRepository):
    async def get_for_campaign(self, campaign_id: str) -> StructuredWorkSample | None:
        stmt = self._scoped(
            select(StructuredWorkSample).where(StructuredWorkSample.campaign_id == campaign_id),
            StructuredWorkSample.organization_id,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_tasks(self, work_sample_id: str) -> Sequence[WorkSampleTask]:
        stmt = self._scoped(
            select(WorkSampleTask).where(WorkSampleTask.work_sample_id == work_sample_id),
            WorkSampleTask.organization_id,
        ).order_by(WorkSampleTask.display_order)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def upsert_header(
        self, campaign_id: str, *, title: str, introduction: str | None
    ) -> StructuredWorkSample:
        work_sample = await self.get_for_campaign(campaign_id)
        if work_sample is None:
            work_sample = StructuredWorkSample(
                id=new_id(),
                organization_id=self.tenant_id,
                campaign_id=campaign_id,
                title=title,
                introduction=introduction,
            )
            self.session.add(work_sample)
        else:
            work_sample.title = title
            work_sample.introduction = introduction
        await self.session.flush()
        return work_sample

    async def replace_tasks(self, work_sample_id: str, tasks: list[dict[str, Any]]) -> None:
        """Delete existing tasks and insert the new set (draft-only replace)."""
        await self.session.execute(
            self._scoped(
                delete(WorkSampleTask).where(WorkSampleTask.work_sample_id == work_sample_id),
                WorkSampleTask.organization_id,
            )
        )
        for order, task in enumerate(tasks):
            self.session.add(
                WorkSampleTask(
                    id=new_id(),
                    organization_id=self.tenant_id,
                    work_sample_id=work_sample_id,
                    prompt=task["prompt"],
                    instructions=task["instructions"],
                    evidence_intent=task["evidence_intent"],
                    task_type=task["task_type"],
                    competencies=task["competencies"],
                    display_order=order,
                    expected_effort_minutes=task["expected_effort_minutes"],
                )
            )
        await self.session.flush()
