"""Evidence persistence — **append-only**. The repository deliberately speaks domain
language (`create_submission_evidence`, `list_for_evaluation`) and exposes **no update
or delete**. Once created, evidence is never mutated. Keyed by evaluation (resolved
server-side); org id is stored for later tenant-scoped recruiter/AI reads."""

from collections.abc import Sequence
from datetime import UTC, datetime

from sqlalchemy import func, select

from app.modules.evidence.enums import EvidenceSourceType
from app.modules.evidence.models import Evidence
from app.modules.worksample.models import WorkSampleTask
from app.shared.ids import new_id
from app.shared.repository import Repository


class EvidenceRepository(Repository):
    async def create_submission_evidence(
        self,
        *,
        organization_id: str,
        candidate_evaluation_id: str,
        snapshots: Sequence[tuple[str, str]],  # (work_sample_task_id, response_text) in task order
    ) -> list[Evidence]:
        captured_at = datetime.now(UTC)
        created: list[Evidence] = []
        for task_id, response_text in snapshots:
            evidence = Evidence(
                id=new_id(),
                organization_id=organization_id,
                candidate_evaluation_id=candidate_evaluation_id,
                work_sample_task_id=task_id,
                response_text=response_text,
                source_type=EvidenceSourceType.WORK_SAMPLE_RESPONSE.value,
                captured_at=captured_at,
            )
            self.session.add(evidence)
            created.append(evidence)
        await self.session.flush()  # unique(eval, task) enforces no duplicate here
        return created

    async def list_for_evaluation(self, candidate_evaluation_id: str) -> Sequence[Evidence]:
        # Deterministic order by the frozen task's position — Task 1 → Evidence 1, …
        stmt = (
            select(Evidence)
            .join(WorkSampleTask, Evidence.work_sample_task_id == WorkSampleTask.id)
            .where(Evidence.candidate_evaluation_id == candidate_evaluation_id)
            .order_by(WorkSampleTask.display_order)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def list_with_tasks_for_evaluation(
        self, *, candidate_evaluation_id: str, organization_id: str
    ) -> Sequence[tuple[Evidence, WorkSampleTask]]:
        """Recruiter read: each evidence snapshot with its frozen task (prompt + intent +
        order), org-scoped for defense in depth. Ordered by the task's position so the
        recruiter sees Task 1, Task 2, ... The caller must first confirm the candidate
        evaluation belongs to the tenant."""
        stmt = (
            select(Evidence, WorkSampleTask)
            .join(WorkSampleTask, Evidence.work_sample_task_id == WorkSampleTask.id)
            .where(
                Evidence.candidate_evaluation_id == candidate_evaluation_id,
                Evidence.organization_id == organization_id,
            )
            .order_by(WorkSampleTask.display_order)
        )
        result = await self.session.execute(stmt)
        return [(row[0], row[1]) for row in result.all()]

    async def count_for_evaluation(self, candidate_evaluation_id: str) -> int:
        stmt = (
            select(func.count())
            .select_from(Evidence)
            .where(Evidence.candidate_evaluation_id == candidate_evaluation_id)
        )
        result = await self.session.execute(stmt)
        return int(result.scalar_one())
