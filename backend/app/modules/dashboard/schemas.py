"""Dashboard read DTOs. A purpose-built read model for the recruiter home — the
backend assembles the tenant's metrics; the frontend never stitches them together
from many calls. Every field is derived from data we actually have (no AI, no
fabricated velocity/confidence/outcomes)."""

from datetime import datetime

from pydantic import BaseModel

from app.modules.campaigns.enums import CampaignStatus


class DashboardMetrics(BaseModel):
    total_campaigns: int
    active_campaigns: int
    draft_campaigns: int
    total_candidates: int
    candidates_missing_resume: int


class DashboardAttention(BaseModel):
    """Counts for "needs attention" — the frontend shows only the ones > 0."""

    draft_campaigns: int  # waiting for activation
    active_campaigns_without_candidates: int  # live but empty
    candidates_missing_resume: int


class DashboardCampaign(BaseModel):
    id: str
    role_title: str
    status: CampaignStatus
    created_at: datetime


class DashboardCandidate(BaseModel):
    evaluation_id: str
    name: str
    email: str
    campaign_id: str
    campaign_role_title: str
    created_at: datetime


class DashboardResponse(BaseModel):
    metrics: DashboardMetrics
    attention: DashboardAttention
    recent_campaigns: list[DashboardCampaign]
    recent_candidates: list[DashboardCandidate]
