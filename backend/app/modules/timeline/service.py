"""Hiring-timeline service — assembles the audit trail, introduces NO business logic.

It reads the authoritative, append-only records for one candidate evaluation (invitations,
consent, submission, evaluation runs, decisions) and normalizes them into one chronological
timeline. Everything is derived; nothing is stored. Tenant authority is enforced first
(a cross-tenant id reads as 404). This is the "prove exactly what happened" view.
"""

from datetime import UTC, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.campaigns.repository import CampaignRepository
from app.modules.candidates.repository import (
    CandidateEvaluationRepository,
    CandidateRepository,
)
from app.modules.consent.repository import ConsentRepository
from app.modules.decisions.repository import DecisionRepository
from app.modules.evaluations.repository import EvaluationRepository
from app.modules.evidence.repository import EvidenceRepository
from app.modules.invitations.repository import InvitationRepository
from app.modules.timeline.enums import TimelineEventKind
from app.modules.timeline.schemas import HiringTimelineResponse, TimelineEntry
from app.shared.errors import NotFoundError


class TimelineService:
    def __init__(self, session: AsyncSession, tenant_id: str) -> None:
        self._session = session
        self._tenant_id = tenant_id

    async def get_timeline(self, candidate_evaluation_id: str) -> HiringTimelineResponse:
        evaluation = await CandidateEvaluationRepository(self._session, self._tenant_id).get(
            candidate_evaluation_id
        )
        if evaluation is None:
            raise NotFoundError(
                "Candidate evaluation not found.", code="CANDIDATE_EVALUATION_NOT_FOUND"
            )
        candidate = await CandidateRepository(self._session, self._tenant_id).get(
            evaluation.candidate_id
        )
        campaign = await CampaignRepository(self._session, self._tenant_id).get(
            evaluation.campaign_id
        )

        entries: list[TimelineEntry] = []

        for invitation in await InvitationRepository(
            self._session, self._tenant_id
        ).list_for_evaluation(candidate_evaluation_id):
            entries.append(
                TimelineEntry(
                    kind=TimelineEventKind.INVITATION_SENT,
                    at=_utc(invitation.created_at),
                    actor_type="recruiter",
                    actor=None,
                    summary="Invitation sent to the candidate.",
                )
            )
            if invitation.accessed_at is not None:
                entries.append(
                    TimelineEntry(
                        kind=TimelineEventKind.INVITATION_OPENED,
                        at=_utc(invitation.accessed_at),
                        actor_type="candidate",
                        actor=None,
                        summary="Candidate opened the invitation.",
                    )
                )

        for consent in await ConsentRepository(self._session).list_for_evaluation(
            candidate_evaluation_id
        ):
            entries.append(
                TimelineEntry(
                    kind=TimelineEventKind.CONSENT_GRANTED,
                    at=_utc(consent.consented_at),
                    actor_type="candidate",
                    actor=None,
                    summary=f"Candidate granted consent (version {consent.consent_version}).",
                )
            )
            if consent.withdrawn_at is not None:
                entries.append(
                    TimelineEntry(
                        kind=TimelineEventKind.CONSENT_WITHDRAWN,
                        at=_utc(consent.withdrawn_at),
                        actor_type="candidate",
                        actor=None,
                        summary="Candidate withdrew consent.",
                    )
                )

        if evaluation.submitted_at is not None:
            count = await EvidenceRepository(self._session).count_for_evaluation(
                candidate_evaluation_id
            )
            entries.append(
                TimelineEntry(
                    kind=TimelineEventKind.WORK_SAMPLE_SUBMITTED,
                    at=_utc(evaluation.submitted_at),
                    actor_type="candidate",
                    actor=None,
                    summary=f"Candidate submitted the work sample ({count} "
                    f"response{'' if count == 1 else 's'}).",
                )
            )

        for run in await EvaluationRepository(
            self._session, self._tenant_id
        ).list_for_candidate_evaluation(candidate_evaluation_id):
            entries.append(
                TimelineEntry(
                    kind=TimelineEventKind.EVALUATION_GENERATED,
                    at=_utc(run.created_at),
                    actor_type="system",
                    actor=None,
                    summary=f"AI evaluation run {run.run_number}: {run.recommendation} "
                    f"(evidence confidence {run.confidence:.2f}) via {run.model}.",
                )
            )

        for row in await DecisionRepository(
            self._session, self._tenant_id
        ).list_for_candidate_evaluation(candidate_evaluation_id):
            decision, email, run_number = row[0], row[1], row[2]
            informed = f", informed by run {run_number}" if run_number is not None else ""
            rationale = " (with rationale)" if decision.rationale else ""
            entries.append(
                TimelineEntry(
                    kind=TimelineEventKind.DECISION_RECORDED,
                    at=_utc(decision.decided_at),
                    actor_type="recruiter",
                    actor=email,
                    summary=f"Decision recorded: {decision.decision}{informed}{rationale}.",
                )
            )

        # Chronological (oldest first). Stable sort keeps the lifecycle build order for ties.
        entries.sort(key=lambda e: e.at)

        return HiringTimelineResponse(
            candidate_evaluation_id=candidate_evaluation_id,
            candidate_name=candidate.name if candidate else "",
            candidate_email=candidate.email if candidate else "",
            role_title=campaign.role_title if campaign else "",
            entries=entries,
        )


def _utc(value: datetime) -> datetime:
    return value if value.tzinfo is not None else value.replace(tzinfo=UTC)
