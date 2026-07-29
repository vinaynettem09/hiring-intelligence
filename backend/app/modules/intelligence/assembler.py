"""The **only** builder of AI input (INV-012).

`EvaluationInputAssembler` assembles an `EvaluationInput` from exactly three
authoritative sources:

    Frozen Role Profile (Campaign)  +  Frozen Work-Sample Tasks  +  Immutable Evidence

and nothing else. It applies the `PIIMinimizer` to every piece of candidate-authored
evidence text on the way out, so what leaves this module is already PII-minimized.

By construction this module does **not import or query `Candidate` (PII) or
`WorkSampleResponse` (mutable draft)** — it depends only on the evaluation record (which
holds no PII), the campaign, the frozen work sample, and immutable Evidence. A developer
following the normal pipeline therefore *cannot* route candidate PII to the AI: there is
no code path here that reaches it. (A structural test asserts these exclusions.)
"""

from collections import defaultdict

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.campaigns.repository import CampaignRepository
from app.modules.candidates.enums import EvaluationStatus
from app.modules.candidates.repository import CandidateEvaluationRepository
from app.modules.evidence.repository import EvidenceRepository
from app.modules.intelligence.schemas import (
    CompetencyContext,
    EvaluationInput,
    EvidenceItem,
    RoleContext,
    TaskEvidenceInput,
)
from app.modules.worksample.repository import WorkSampleRepository
from app.platform.pii import PIIMinimizer, get_pii_minimizer
from app.shared.errors import BusinessRuleViolation, NotFoundError
from app.shared.logging import get_logger

_log = get_logger(__name__)


class EvaluationInputAssembler:
    def __init__(
        self,
        session: AsyncSession,
        tenant_id: str,
        *,
        minimizer: PIIMinimizer | None = None,
    ) -> None:
        # Note the repositories used: evaluation (no PII), campaign, work sample, evidence.
        # Candidate (PII) and WorkSampleResponse (draft) repositories are intentionally absent.
        self._evaluations = CandidateEvaluationRepository(session, tenant_id)
        self._campaigns = CampaignRepository(session, tenant_id)
        self._work_samples = WorkSampleRepository(session, tenant_id)
        self._evidence = EvidenceRepository(session)
        self._minimizer = minimizer or get_pii_minimizer()

    async def build(self, evaluation_id: str) -> EvaluationInput:
        evaluation = await self._evaluations.get(evaluation_id)  # tenant-scoped; carries no PII
        if evaluation is None:
            raise NotFoundError("Evaluation not found.", code="EVALUATION_NOT_FOUND")
        # The AI only ever evaluates *submitted* evidence — never drafts, never mid-flight.
        if evaluation.status != EvaluationStatus.SUBMITTED.value:
            raise BusinessRuleViolation(
                "This evaluation has not been submitted; there is no evidence to evaluate.",
                code="EVALUATION_NOT_SUBMITTED",
                metadata={"status": evaluation.status},
            )

        campaign = await self._campaigns.get(evaluation.campaign_id)
        if campaign is None:  # pragma: no cover - an evaluation always has its campaign
            raise NotFoundError("Campaign not found.", code="CAMPAIGN_NOT_FOUND")
        role = self._build_role(campaign.role_title, campaign.role_profile or {})

        work_sample = await self._work_samples.get_for_campaign(campaign.id)
        tasks = (
            await self._work_samples.list_tasks(work_sample.id) if work_sample is not None else []
        )

        evidence_by_task: dict[str, list[EvidenceItem]] = defaultdict(list)
        total_redactions = 0
        for row in await self._evidence.list_for_evaluation(evaluation_id):
            # Minimize here — the raw Evidence row is never mutated; this is a projection.
            # FAIL CLOSED: if minimization raises we must NOT send raw Evidence downstream.
            try:
                minimized = self._minimizer.minimize(row.response_text)
            except Exception as exc:
                raise BusinessRuleViolation(
                    "Evidence could not be safely minimized for evaluation.",
                    code="PII_MINIMIZATION_FAILED",
                ) from exc
            total_redactions += minimized.redactions
            evidence_by_task[row.work_sample_task_id].append(
                EvidenceItem(evidence_id=row.id, text=minimized.text)
            )

        # Safe operational signal only — the COUNT, never what was redacted.
        _log.info(
            "intelligence.input_assembled",
            evaluation_id=evaluation_id,
            pii_redactions_count=total_redactions,
        )

        task_inputs = tuple(
            TaskEvidenceInput(
                task_id=task.id,
                prompt=task.prompt,
                evidence_intent=task.evidence_intent,
                competencies=tuple(task.competencies),
                evidence=tuple(evidence_by_task.get(task.id, [])),
            )
            for task in tasks
        )
        return EvaluationInput(evaluation_id=evaluation_id, role=role, tasks=task_inputs)

    @staticmethod
    def _build_role(role_title: str, role_profile: dict[str, object]) -> RoleContext:
        raw = role_profile.get("competencies")
        raw_competencies = raw if isinstance(raw, list) else []
        competencies = tuple(
            CompetencyContext(
                name=str(competency.get("name", "")),
                definition=competency.get("description"),
            )
            for competency in raw_competencies
            if isinstance(competency, dict)
        )
        return RoleContext(
            role_title=role_title,
            bar=str(role_profile.get("bar", "")),
            competencies=competencies,
        )
