"""FastAPI routes for candidate invitations — two distinct trust boundaries.

Recruiter (JWT):
- POST /evaluations/{id}/invitation — issue/replace an invitation for one of this org's
  candidate evaluations (Story 4.1).

Candidate (opaque token — NO recruiter auth):
- POST /candidate/invitation — resolve a magic-link token to the candidate view.
  Token is in the body (never the URL) so it isn't captured in access logs.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.invitations.schemas import (
    CandidateInvitationView,
    InvitationSummary,
    ResolveInvitationRequest,
)
from app.modules.invitations.service import CandidateAccessService, InvitationService
from app.platform.email import EmailProvider, get_email_provider
from app.shared.context import AuthContext, require_auth
from app.shared.db import get_session

router = APIRouter(tags=["invitations"])


@router.post("/evaluations/{evaluation_id}/invitation", status_code=201)
async def issue_invitation(
    evaluation_id: str,
    auth: AuthContext = Depends(require_auth),
    session: AsyncSession = Depends(get_session),
    email: EmailProvider = Depends(get_email_provider),
) -> InvitationSummary:
    return await InvitationService(session, auth.organization_id, email).issue(
        evaluation_id, actor_user_id=auth.user_id
    )


@router.post("/candidate/invitation")
async def resolve_invitation(
    payload: ResolveInvitationRequest,
    session: AsyncSession = Depends(get_session),
) -> CandidateInvitationView:
    # No auth: possession of the token is the authorization. Invalid/expired/revoked
    # all raise NotFoundError with a distinct code and leak nothing else.
    return await CandidateAccessService(session).resolve(payload.token)
