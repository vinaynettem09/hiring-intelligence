"""Invitation persistence.

- `InvitationRepository` (tenant-scoped) — the **recruiter** side: create + revoke.
- `resolve_by_token_hash` (NOT tenant-scoped) — the **candidate** side. This is the one
  deliberate cross-tenant read in the codebase: the candidate has no tenant and no JWT;
  authorization is possession of the unguessable token, which maps to exactly one
  invitation. It returns only that invitation's context. Documented, not an oversight.
"""

from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import select

from app.modules.campaigns.models import Campaign
from app.modules.candidates.models import Candidate, CandidateEvaluation
from app.modules.identity.models import Organization
from app.modules.invitations.models import Invitation
from app.shared.ids import new_id
from app.shared.repository import Repository, TenantScopedRepository


class InvitationRepository(TenantScopedRepository):
    async def create(
        self, *, candidate_evaluation_id: str, token_hash: str, expires_at: datetime
    ) -> Invitation:
        invitation = Invitation(
            id=new_id(),
            organization_id=self.tenant_id,
            candidate_evaluation_id=candidate_evaluation_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )
        self.session.add(invitation)
        await self.session.flush()
        return invitation

    async def list_for_evaluation(self, candidate_evaluation_id: str) -> Sequence[Invitation]:
        """All invitations for an evaluation, oldest first (re-invites included) — for the
        audit timeline. Tenant-scoped."""
        stmt = self._scoped(
            select(Invitation)
            .where(Invitation.candidate_evaluation_id == candidate_evaluation_id)
            .order_by(Invitation.created_at),
            Invitation.organization_id,
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def revoke_active_for_evaluation(self, candidate_evaluation_id: str) -> int:
        """Revoke any still-active invitations for this evaluation (re-invite replaces
        the previous link). Returns how many were revoked. Tenant-scoped."""
        stmt = self._scoped(
            select(Invitation).where(
                Invitation.candidate_evaluation_id == candidate_evaluation_id,
                Invitation.revoked.is_(False),
            ),
            Invitation.organization_id,
        )
        result = await self.session.execute(stmt)
        revoked = 0
        for invitation in result.scalars().all():
            invitation.revoked = True
            revoked += 1
        await self.session.flush()
        return revoked


class InvitationAccessRepository(Repository):
    """Candidate-side lookup by token hash — NOT tenant-scoped by design (see module
    docstring). The token is the authorization and scopes to exactly one invitation."""

    async def resolve_by_token_hash(
        self, token_hash: str
    ) -> tuple[Invitation, Campaign, Candidate, Organization] | None:
        stmt = (
            select(Invitation, Campaign, Candidate, Organization)
            .join(CandidateEvaluation, Invitation.candidate_evaluation_id == CandidateEvaluation.id)
            .join(Campaign, CandidateEvaluation.campaign_id == Campaign.id)
            .join(Candidate, CandidateEvaluation.candidate_id == Candidate.id)
            .join(Organization, Invitation.organization_id == Organization.id)
            .where(Invitation.token_hash == token_hash)
        )
        result = await self.session.execute(stmt)
        row = result.first()
        if row is None:
            return None
        return (row[0], row[1], row[2], row[3])
