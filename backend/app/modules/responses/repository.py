"""Draft-response persistence. Keyed by (candidate_evaluation_id, task_id), both
resolved server-side from the candidate's token (never client-supplied), so this sits
inside the candidate trust boundary. Upsert, so autosave never duplicates."""

from collections.abc import Sequence

from sqlalchemy import func, select

from app.modules.responses.models import WorkSampleResponse
from app.shared.ids import new_id
from app.shared.repository import Repository


class ResponseRepository(Repository):
    async def list_for_evaluation(self, evaluation_id: str) -> Sequence[WorkSampleResponse]:
        stmt = select(WorkSampleResponse).where(
            WorkSampleResponse.candidate_evaluation_id == evaluation_id
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def count_for_evaluation(self, evaluation_id: str) -> int:
        stmt = (
            select(func.count())
            .select_from(WorkSampleResponse)
            .where(WorkSampleResponse.candidate_evaluation_id == evaluation_id)
        )
        result = await self.session.execute(stmt)
        return int(result.scalar_one())

    async def upsert(
        self, *, organization_id: str, evaluation_id: str, task_id: str, response_text: str
    ) -> WorkSampleResponse:
        stmt = select(WorkSampleResponse).where(
            WorkSampleResponse.candidate_evaluation_id == evaluation_id,
            WorkSampleResponse.work_sample_task_id == task_id,
        )
        existing = (await self.session.execute(stmt)).scalar_one_or_none()
        if existing is not None:
            existing.response_text = response_text
            await self.session.flush()
            return existing
        response = WorkSampleResponse(
            id=new_id(),
            organization_id=organization_id,
            candidate_evaluation_id=evaluation_id,
            work_sample_task_id=task_id,
            response_text=response_text,
        )
        self.session.add(response)
        await self.session.flush()
        return response
