"""Invitation services.

- `InvitationService` (recruiter, tenant-scoped): issue a fresh invitation for one of
  this org's candidate evaluations — campaign must be active, previous active link is
  revoked (re-invite replaces), email sent via the EmailProvider seam, action audited.
- `CandidateAccessService` (candidate trust boundary, NOT tenant-scoped): resolve a raw
  token to the candidate-facing view. Invalid/expired/revoked all fail safely with a
  distinct code and no leak of other data.
"""

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import get_settings
from app.modules.audit.service import AuditService
from app.modules.campaigns.enums import CampaignStatus
from app.modules.campaigns.models import Campaign
from app.modules.campaigns.repository import CampaignRepository
from app.modules.candidates.models import Candidate
from app.modules.candidates.repository import CandidateEvaluationRepository, CandidateRepository
from app.modules.candidates.schemas import CandidateSummary
from app.modules.identity.models import Organization
from app.modules.identity.repository import OrganizationRepository
from app.modules.invitations.emails import build_invitation_email
from app.modules.invitations.models import Invitation
from app.modules.invitations.repository import InvitationAccessRepository, InvitationRepository
from app.modules.invitations.schemas import CandidateInvitationView, InvitationSummary
from app.platform.email import EmailProvider
from app.shared.errors import ConflictError, NotFoundError
from app.shared.tokens import generate_opaque_token, hash_opaque_token


class InvitationService:
    def __init__(self, session: AsyncSession, tenant_id: str, email: EmailProvider) -> None:
        self._tenant_id = tenant_id
        self._email = email
        self._invitations = InvitationRepository(session, tenant_id)
        self._evaluations = CandidateEvaluationRepository(session, tenant_id)
        self._campaigns = CampaignRepository(session, tenant_id)
        self._candidates = CandidateRepository(session, tenant_id)
        self._organizations = OrganizationRepository(session)
        self._audit = AuditService(session)

    async def issue(self, evaluation_id: str, *, actor_user_id: str) -> InvitationSummary:
        # Scoped lookups → another tenant's evaluation is simply "not found" (404).
        evaluation = await self._evaluations.get(evaluation_id)
        if evaluation is None:
            raise NotFoundError("Evaluation not found.", code="EVALUATION_NOT_FOUND")
        campaign = await self._campaigns.get(evaluation.campaign_id)
        if campaign is None:  # pragma: no cover - FK guarantees presence
            raise NotFoundError("Evaluation not found.", code="EVALUATION_NOT_FOUND")
        if campaign.status != CampaignStatus.ACTIVE.value:
            raise ConflictError(
                "Candidates can only be invited on an active campaign.",
                code="CAMPAIGN_NOT_ACTIVE",
                metadata={"current_status": campaign.status},
            )
        candidate = await self._candidates.get(evaluation.candidate_id)
        if candidate is None:  # pragma: no cover - FK guarantees presence
            raise NotFoundError("Evaluation not found.", code="EVALUATION_NOT_FOUND")
        organization = await self._organizations.get(self._tenant_id)
        if organization is None:  # pragma: no cover - tenant from verified token
            raise NotFoundError("Organization not found.", code="EVALUATION_NOT_FOUND")

        # Re-invite replaces: revoke any active link, then mint a fresh one.
        replaced = await self._invitations.revoke_active_for_evaluation(evaluation_id)

        settings = get_settings()
        raw_token = generate_opaque_token()  # returned only via the email link, never stored
        invitation = await self._invitations.create(
            candidate_evaluation_id=evaluation_id,
            token_hash=hash_opaque_token(raw_token),
            expires_at=datetime.now(UTC) + timedelta(seconds=settings.invitation_ttl_seconds),
        )

        await self._audit.record(
            organization_id=self._tenant_id,
            actor_type="recruiter",
            actor_user_id=actor_user_id,
            action="invitation.issued",
            target_type="candidate_evaluation",
            target_id=evaluation_id,
            details={"invitation_id": invitation.id, "replaced_previous": replaced > 0},
        )

        link = f"{settings.frontend_base_url.rstrip('/')}/invite/{raw_token}"
        await self._email.send(
            build_invitation_email(
                to=candidate.email,
                candidate_name=candidate.name,
                organization_name=organization.name,
                role_title=campaign.role_title,
                link=link,
                expires_at=invitation.expires_at,
            )
        )

        return InvitationSummary(
            id=invitation.id,
            candidate=CandidateSummary(id=candidate.id, name=candidate.name, email=candidate.email),
            expires_at=invitation.expires_at,
            created_at=invitation.created_at,
            replaced_previous=replaced > 0,
        )


@dataclass(frozen=True)
class ResolvedInvitation:
    """A validated invitation plus its context — the reusable candidate-boundary result
    that other candidate-side services (e.g. consent) build on."""

    invitation: Invitation
    campaign: Campaign
    candidate: Candidate
    organization: Organization


class CandidateAccessService:
    """The candidate trust boundary. No tenant, no JWT — the token is the authorization."""

    def __init__(self, session: AsyncSession) -> None:
        self._access = InvitationAccessRepository(session)
        self._audit = AuditService(session)

    async def resolve_invitation(self, token: str) -> ResolvedInvitation:
        """Validate a token → its invitation context. Raises with a distinct, non-leaky
        code for invalid/expired/revoked. Does NOT mutate (no access marking) so it's
        safe to reuse from any candidate-side flow (consent, work sample, …)."""
        resolved = await self._access.resolve_by_token_hash(hash_opaque_token(token))
        if resolved is None:
            # No match — reveal nothing about whether any candidate/campaign exists.
            raise NotFoundError("This invitation link is not valid.", code="INVITATION_INVALID")
        invitation, campaign, candidate, organization = resolved

        if invitation.revoked:
            raise NotFoundError("This invitation is no longer active.", code="INVITATION_REVOKED")
        expires_at = invitation.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=UTC)  # sqlite returns naive; treat as UTC
        if expires_at < datetime.now(UTC):
            raise NotFoundError("This invitation has expired.", code="INVITATION_EXPIRED")

        return ResolvedInvitation(invitation, campaign, candidate, organization)

    async def resolve(self, token: str) -> CandidateInvitationView:
        resolved = await self.resolve_invitation(token)
        invitation = resolved.invitation

        if invitation.accessed_at is None:
            invitation.accessed_at = datetime.now(UTC)  # committed with the request
            await self._audit.record(
                organization_id=invitation.organization_id,
                actor_type="candidate",
                action="invitation.accessed",
                target_type="candidate_evaluation",
                target_id=invitation.candidate_evaluation_id,
                details={"invitation_id": invitation.id},
            )

        expires_at = invitation.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=UTC)
        return CandidateInvitationView(
            candidate_name=resolved.candidate.name,
            organization_name=resolved.organization.name,
            role_title=resolved.campaign.role_title,
            expires_at=expires_at,
        )
