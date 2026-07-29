"""Evaluation persistence — **append-only**, tenant-scoped.

Speaks domain language (`create_evaluation`, `get_latest_for_candidate_evaluation`,
`list_for_candidate_evaluation`) and exposes **no update/delete/save**: a persisted
Evaluation is an immutable historical fact, and a rerun is a *new* row. Every read routes
through the tenant filter (`_scoped`) so Org B can never read/list Org A's Evaluations
(INV-000). Repositories persist (`add`/`flush`); they never commit.
"""

from collections.abc import Sequence
from typing import Any

from sqlalchemy import Select, func, select
from sqlalchemy.orm import selectinload

from app.modules.evaluations.models import (
    Evaluation,
    EvaluationCitation,
    EvaluationCompetencyAssessment,
)
from app.modules.intelligence.schemas import EvaluationProposal, GroundedObservation
from app.platform.ai import ProviderUsage
from app.shared.ids import new_id
from app.shared.repository import TenantScopedRepository


def _observations_json(
    observations: tuple[GroundedObservation, ...],
) -> list[dict[str, Any]]:
    """Serialize grounded strengths/concerns for the JSON column — text + its citations,
    so a persisted observation stays as groundable as it was when produced."""
    return [
        {
            "text": observation.text,
            "citations": [
                {"evidence_id": c.evidence_id, "task_id": c.task_id}
                for c in observation.evidence_citations
            ],
        }
        for observation in observations
    ]


class EvaluationRepository(TenantScopedRepository):
    async def create_evaluation(
        self,
        *,
        candidate_evaluation_id: str,
        run_number: int,
        idempotency_key: str | None,
        proposal: EvaluationProposal,
        input_fingerprint: str,
        usage: ProviderUsage | None = None,
    ) -> Evaluation:
        """Persist ONE validated proposal as an immutable Evaluation run (+ its
        competency assessments and evidence citations). The proposal has already passed
        schema/grounding/policy validation and honesty-floor enforcement upstream — this
        method records it, it does not re-judge it."""
        provenance = proposal.provenance
        coverage = proposal.evidence_coverage
        evaluation_id = new_id()
        evaluation = Evaluation(
            id=evaluation_id,
            organization_id=self.tenant_id,
            candidate_evaluation_id=candidate_evaluation_id,
            run_number=run_number,
            idempotency_key=idempotency_key,
            recommendation=proposal.recommendation.value,
            confidence=proposal.confidence,
            confidence_rationale=proposal.confidence_rationale,
            escalation_reason=(
                proposal.escalation_reason.value if proposal.escalation_reason else None
            ),
            strengths=_observations_json(proposal.strengths),
            concerns=_observations_json(proposal.concerns),
            coverage_competencies_total=coverage.competencies_total,
            coverage_competencies_assessed=coverage.competencies_assessed,
            coverage_tasks_total=coverage.tasks_total,
            coverage_tasks_with_evidence=coverage.tasks_with_evidence,
            provider=provenance.provider,
            model=provenance.model,
            model_version=provenance.model_version,
            prompt_version=provenance.prompt_version,
            input_schema_version=provenance.input_schema_version,
            output_schema_version=provenance.output_schema_version,
            confidence_algorithm_version=provenance.confidence_algorithm_version,
            generated_at=provenance.generated_at,
            input_fingerprint=input_fingerprint,
            input_tokens=usage.input_tokens if usage else None,
            output_tokens=usage.output_tokens if usage else None,
        )
        self.session.add(evaluation)

        for order, assessment in enumerate(proposal.competency_assessments):
            assessment_id = new_id()
            self.session.add(
                EvaluationCompetencyAssessment(
                    id=assessment_id,
                    organization_id=self.tenant_id,
                    evaluation_id=evaluation_id,
                    competency=assessment.competency,
                    assessment=assessment.assessment,
                    provider_signal=assessment.provider_signal,
                    display_order=order,
                )
            )
            for citation in assessment.evidence_citations:
                self.session.add(
                    EvaluationCitation(
                        id=new_id(),
                        organization_id=self.tenant_id,
                        evaluation_id=evaluation_id,
                        competency_assessment_id=assessment_id,
                        evidence_id=citation.evidence_id,
                        work_sample_task_id=citation.task_id,
                    )
                )

        # flush surfaces the unique(run) / unique(idempotency_key) backstops here, inside
        # the caller's transaction, so a racing duplicate fails before commit.
        await self.session.flush()
        return await self._load(evaluation_id)

    async def get_evaluation(self, evaluation_id: str) -> Evaluation | None:
        stmt = self._scoped(
            self._with_children(select(Evaluation)).where(Evaluation.id == evaluation_id),
            Evaluation.organization_id,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_latest_for_candidate_evaluation(
        self, candidate_evaluation_id: str
    ) -> Evaluation | None:
        stmt = (
            self._scoped(
                self._with_children(select(Evaluation)).where(
                    Evaluation.candidate_evaluation_id == candidate_evaluation_id
                ),
                Evaluation.organization_id,
            )
            .order_by(Evaluation.run_number.desc())
            .limit(1)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_by_idempotency_key(
        self, *, candidate_evaluation_id: str, idempotency_key: str
    ) -> Evaluation | None:
        stmt = self._scoped(
            self._with_children(select(Evaluation)).where(
                Evaluation.candidate_evaluation_id == candidate_evaluation_id,
                Evaluation.idempotency_key == idempotency_key,
            ),
            Evaluation.organization_id,
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_for_candidate_evaluation(
        self, candidate_evaluation_id: str
    ) -> Sequence[Evaluation]:
        """All runs, newest first — summary rows (children NOT eagerly loaded)."""
        stmt = self._scoped(
            select(Evaluation).where(Evaluation.candidate_evaluation_id == candidate_evaluation_id),
            Evaluation.organization_id,
        ).order_by(Evaluation.run_number.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def latest_for_candidate_evaluations(
        self, candidate_evaluation_ids: Sequence[str]
    ) -> dict[str, Evaluation]:
        """Map each given candidate_evaluation_id → its LATEST run (highest run_number),
        tenant-scoped. Used by the roster to show evaluation status in one query instead
        of N reads. Children are NOT eager-loaded (the roster needs only summary fields)."""
        ids = list(candidate_evaluation_ids)
        if not ids:
            return {}
        latest = (
            self._scoped(
                select(
                    Evaluation.candidate_evaluation_id.label("cid"),
                    func.max(Evaluation.run_number).label("rn"),
                ),
                Evaluation.organization_id,
            )
            .where(Evaluation.candidate_evaluation_id.in_(ids))
            .group_by(Evaluation.candidate_evaluation_id)
            .subquery()
        )
        stmt = self._scoped(select(Evaluation), Evaluation.organization_id).join(
            latest,
            (Evaluation.candidate_evaluation_id == latest.c.cid)
            & (Evaluation.run_number == latest.c.rn),
        )
        result = await self.session.execute(stmt)
        return {ev.candidate_evaluation_id: ev for ev in result.scalars().all()}

    async def count_for_candidate_evaluation(self, candidate_evaluation_id: str) -> int:
        stmt = self._scoped(
            select(func.count()).select_from(Evaluation), Evaluation.organization_id
        ).where(Evaluation.candidate_evaluation_id == candidate_evaluation_id)
        result = await self.session.execute(stmt)
        return int(result.scalar_one())

    async def _load(self, evaluation_id: str) -> Evaluation:
        evaluation = await self.get_evaluation(evaluation_id)
        assert evaluation is not None  # noqa: S101 - just created within this session
        return evaluation

    @staticmethod
    def _with_children(stmt: Select[tuple[Evaluation]]) -> Select[tuple[Evaluation]]:
        # Eager-load assessments and their citations for full-detail reads.
        return stmt.options(
            selectinload(Evaluation.assessments).selectinload(
                EvaluationCompetencyAssessment.citations
            )
        )
