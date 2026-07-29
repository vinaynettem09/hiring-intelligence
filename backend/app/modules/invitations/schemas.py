"""DTOs for candidate invitations.

Two audiences, two shapes:
- `InvitationSummary` — recruiter-facing (never includes the raw token).
- `CandidateInvitationView` — candidate-facing; shows only what the candidate may see
  (their own name, the company, the role, what's next). No internal IDs, no calibration,
  no scoring config, no AI, no other candidates.
"""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from app.modules.candidates.schemas import CandidateSummary


class InvitationSummary(BaseModel):
    id: str
    candidate: CandidateSummary
    expires_at: datetime
    created_at: datetime
    replaced_previous: bool  # true if this re-invite superseded an active invitation


class ResolveInvitationRequest(BaseModel):
    token: str


class CandidateInvitationView(BaseModel):
    candidate_name: str
    organization_name: str
    role_title: str
    # Story 4.1 stops at access; the next real step is consent (Story 4.2).
    next_step: Literal["consent"] = "consent"
    expires_at: datetime
