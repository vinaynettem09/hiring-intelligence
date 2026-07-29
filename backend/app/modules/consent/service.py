"""Consent service — the one authoritative place consent is read, granted, and checked.

Consent is only reachable through a valid candidate access context: the invitation
token resolves the CandidateEvaluation server-side, so a candidate can never grant
(or read) consent for another evaluation or tenant — those are structurally impossible.

`has_active_consent(evaluation_id)` is the gate later stories consume: no active consent
→ no work-sample processing → no evidence → no AI (INV-010 / corpus INV-11). It fails
closed (returns False) whenever active consent cannot be established.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.audit.service import AuditService
from app.modules.consent.content import CONSENT_SECTIONS, CURRENT_CONSENT_VERSION
from app.modules.consent.repository import ConsentRepository
from app.modules.consent.schemas import (
    ConsentDisclosureDTO,
    ConsentSectionDTO,
    ConsentStateResponse,
)
from app.modules.invitations.service import CandidateAccessService, ResolvedInvitation


def _disclosure() -> ConsentDisclosureDTO:
    return ConsentDisclosureDTO(
        version=CURRENT_CONSENT_VERSION,
        sections=[
            ConsentSectionDTO(key=s.key, title=s.title, body=s.body) for s in CONSENT_SECTIONS
        ],
    )


class ConsentService:
    def __init__(self, session: AsyncSession) -> None:
        self._access = CandidateAccessService(session)
        self._repo = ConsentRepository(session)
        self._audit = AuditService(session)

    async def get_state(self, token: str) -> ConsentStateResponse:
        resolved = await self._access.resolve_invitation(token)
        active = await self._repo.active_for_evaluation(resolved.invitation.candidate_evaluation_id)
        return self._state(resolved, consented=active is not None)

    async def grant(self, token: str) -> ConsentStateResponse:
        resolved = await self._access.resolve_invitation(token)
        evaluation_id = resolved.invitation.candidate_evaluation_id

        # Idempotent for the same active version: return the existing grant, never a
        # duplicate, and never mutate the previous record's meaning.
        existing = await self._repo.active_for_version(evaluation_id, CURRENT_CONSENT_VERSION)
        if existing is None:
            consent = await self._repo.create(
                organization_id=resolved.invitation.organization_id,
                candidate_evaluation_id=evaluation_id,
                consent_version=CURRENT_CONSENT_VERSION,
            )
            await self._audit.record(
                organization_id=resolved.invitation.organization_id,
                actor_type="candidate",
                action="consent.granted",
                target_type="candidate_evaluation",
                target_id=evaluation_id,
                details={
                    "consent_id": consent.id,
                    "consent_version": CURRENT_CONSENT_VERSION,
                    "invitation_id": resolved.invitation.id,
                },
            )
        return self._state(resolved, consented=True)

    async def has_active_consent(self, candidate_evaluation_id: str) -> bool:
        """Authoritative gate for downstream stories. Fails closed."""
        return await self._repo.active_for_evaluation(candidate_evaluation_id) is not None

    @staticmethod
    def _state(resolved: ResolvedInvitation, *, consented: bool) -> ConsentStateResponse:
        return ConsentStateResponse(
            organization_name=resolved.organization.name,
            role_title=resolved.campaign.role_title,
            candidate_name=resolved.candidate.name,
            disclosure=_disclosure(),
            consented=consented,
        )
