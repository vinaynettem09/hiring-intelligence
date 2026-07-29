"""Candidate intake service.

Adding a candidate to a campaign, in one tenant-scoped transaction:
  1. the campaign must be **active** (draft is still being calibrated; concluded is
     closed) — candidates are assessed against frozen criteria (INV-003 / INV-008);
  2. reuse the org's identity record for the person if one exists, else create it
     (identity is separate from — and outlives — any single campaign, INV-006);
  3. one evaluation per candidate per campaign (no double invites, INV-007).

Bulk import applies the same rules per row, independently: a bad row is reported, never
allowed to reject the whole file.
"""

from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.campaigns.enums import CampaignStatus
from app.modules.campaigns.models import Campaign
from app.modules.campaigns.repository import CampaignRepository
from app.modules.candidates.enums import EvaluationStatus
from app.modules.candidates.models import Candidate, CandidateEvaluation
from app.modules.candidates.repository import (
    CandidateEvaluationRepository,
    CandidateRepository,
)
from app.modules.candidates.schemas import (
    AddCandidateRequest,
    CandidateEvaluationResponse,
    CandidateImportIssue,
    CandidateImportSummary,
    CandidateSummary,
    RosterEntry,
    RosterResponse,
)
from app.modules.evaluations.repository import EvaluationRepository
from app.shared.errors import ConflictError, NotFoundError


def _describe(error: ValidationError) -> str:
    """A short, human reason for a rejected import row (no stack, no dumped JSON)."""
    first = error.errors()[0]
    field = str(first["loc"][0]) if first["loc"] else "row"
    return f"{field}: {first['msg']}"


class CandidateService:
    def __init__(self, session: AsyncSession, tenant_id: str) -> None:
        self._candidates = CandidateRepository(session, tenant_id)
        self._evaluations = CandidateEvaluationRepository(session, tenant_id)
        self._campaigns = CampaignRepository(session, tenant_id)
        # Read-only: lets the roster show evaluation status (Generate vs. View) in one query.
        self._runs = EvaluationRepository(session, tenant_id)

    async def add_to_campaign(
        self, campaign_id: str, request: AddCandidateRequest
    ) -> CandidateEvaluationResponse:
        await self._require_active_campaign(campaign_id)

        candidate = await self._identity_for(request)
        if (
            await self._evaluations.get_for_candidate_in_campaign(
                campaign_id=campaign_id, candidate_id=candidate.id
            )
            is not None
        ):
            raise ConflictError(
                "This candidate is already in the campaign.",
                code="CANDIDATE_ALREADY_IN_CAMPAIGN",
            )

        evaluation = await self._evaluations.create(
            campaign_id=campaign_id, candidate_id=candidate.id
        )
        return self._to_response(evaluation, candidate)

    async def import_candidates(
        self, campaign_id: str, rows: list[dict[str, str]]
    ) -> CandidateImportSummary:
        """Bulk-add candidates from parsed CSV rows. The active-campaign check happens
        once; each row is then validated and added independently (INV-007/008 per row)."""
        await self._require_active_campaign(campaign_id)

        imported = skipped = failed = 0
        issues: list[CandidateImportIssue] = []

        for line, row in enumerate(rows, start=1):
            email = (row.get("email") or "").strip()
            try:
                request = AddCandidateRequest(
                    name=(row.get("name") or "").strip(),
                    email=email,
                    resume_object_key=(row.get("resume_object_key") or "").strip() or None,
                )
            except ValidationError as exc:
                failed += 1
                issues.append(
                    CandidateImportIssue(
                        row=line, email=email or None, outcome="failed", reason=_describe(exc)
                    )
                )
                continue

            candidate = await self._candidates.get_by_email(request.email)
            if candidate is not None and await self._evaluations.get_for_candidate_in_campaign(
                campaign_id=campaign_id, candidate_id=candidate.id
            ):
                skipped += 1
                issues.append(
                    CandidateImportIssue(
                        row=line,
                        email=request.email,
                        outcome="skipped",
                        reason="Already in this campaign",
                    )
                )
                continue

            if candidate is None:
                candidate = await self._candidates.create(
                    name=request.name,
                    email=request.email,
                    resume_object_key=request.resume_object_key,
                )
            await self._evaluations.create(campaign_id=campaign_id, candidate_id=candidate.id)
            imported += 1

        return CandidateImportSummary(
            total=len(rows), imported=imported, skipped=skipped, failed=failed, issues=issues
        )

    async def list_roster(self, campaign_id: str, *, limit: int, offset: int) -> RosterResponse:
        """The campaign's roster (any status — viewing is not gated on active). 404 if
        the campaign isn't this tenant's."""
        if await self._campaigns.get(campaign_id) is None:
            raise NotFoundError("Campaign not found.", code="CAMPAIGN_NOT_FOUND")

        rows = await self._evaluations.list_roster(
            campaign_id=campaign_id, limit=limit, offset=offset
        )
        latest = await self._runs.latest_for_candidate_evaluations([e.id for e, _ in rows])
        items = [
            RosterEntry(
                evaluation_id=evaluation.id,
                candidate=CandidateSummary(
                    id=candidate.id, name=candidate.name, email=candidate.email
                ),
                status=EvaluationStatus(evaluation.status),
                has_resume=candidate.resume_object_key is not None,
                created_at=evaluation.created_at,
                has_evaluation=evaluation.id in latest,
                latest_recommendation=(
                    latest[evaluation.id].recommendation if evaluation.id in latest else None
                ),
                latest_run_number=(
                    latest[evaluation.id].run_number if evaluation.id in latest else None
                ),
            )
            for evaluation, candidate in rows
        ]
        return RosterResponse(
            items=items,
            total=await self._evaluations.count_for_campaign(campaign_id),
            missing_resume=await self._evaluations.count_missing_resume(campaign_id),
            limit=limit,
            offset=offset,
        )

    async def _require_active_campaign(self, campaign_id: str) -> Campaign:
        campaign = await self._campaigns.get(campaign_id)  # tenant-scoped → 404 if not ours
        if campaign is None:
            raise NotFoundError("Campaign not found.", code="CAMPAIGN_NOT_FOUND")
        if campaign.status != CampaignStatus.ACTIVE.value:
            raise ConflictError(
                "Candidates can only be added to an active campaign.",
                code="CAMPAIGN_NOT_ACTIVE",
                metadata={"current_status": campaign.status},
            )
        return campaign

    async def _identity_for(self, request: AddCandidateRequest) -> Candidate:
        # One identity record per (org, email), reused across campaigns (INV-006).
        candidate = await self._candidates.get_by_email(request.email)
        if candidate is None:
            candidate = await self._candidates.create(
                name=request.name,
                email=request.email,
                resume_object_key=request.resume_object_key,
            )
        return candidate

    @staticmethod
    def _to_response(
        evaluation: CandidateEvaluation, candidate: Candidate
    ) -> CandidateEvaluationResponse:
        return CandidateEvaluationResponse(
            id=evaluation.id,
            campaign_id=evaluation.campaign_id,
            candidate=CandidateSummary(id=candidate.id, name=candidate.name, email=candidate.email),
            status=EvaluationStatus(evaluation.status),
            created_at=evaluation.created_at,
        )
