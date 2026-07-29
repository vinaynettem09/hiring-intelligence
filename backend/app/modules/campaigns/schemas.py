"""Pydantic request/response DTOs for the campaigns module.

These — not ORM models — cross the API boundary. The `RoleProfile` shape (at least
one competency, a stated bar) is validated here; ownership and lifecycle rules live
in the service/model.
"""

from datetime import datetime

from pydantic import BaseModel, Field

from app.modules.campaigns.enums import CampaignStatus


class Competency(BaseModel):
    """A single thing the role is evaluated on."""

    name: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=500)


class RoleProfile(BaseModel):
    """A campaign's calibration: what we assess (competencies) and the bar to clear.

    Validated at creation; frozen once the campaign is activated (INV-003, Story 2.2).
    """

    competencies: list[Competency] = Field(min_length=1, max_length=20)
    bar: str = Field(min_length=1, max_length=500)  # the hiring standard, in words


class CreateCampaignRequest(BaseModel):
    role_title: str = Field(min_length=1, max_length=255)
    role_profile: RoleProfile


class CampaignResponse(BaseModel):
    """Full detail — includes the (frozen-once-active) role profile. Used by GET
    /campaigns/{id} and the create/activate responses."""

    id: str
    role_title: str
    role_profile: RoleProfile
    status: CampaignStatus
    created_at: datetime


class CampaignSummary(BaseModel):
    """Lightweight row for the list endpoint — deliberately **omits** `role_profile`
    so the list stays small and the detail view can grow independently. (A
    `candidate_count` naturally belongs here once candidates exist — Epic 3.)"""

    id: str
    role_title: str
    status: CampaignStatus
    created_at: datetime


class CampaignListResponse(BaseModel):
    items: list[CampaignSummary]
    total: int  # total campaigns for this tenant (so the client can paginate)
    limit: int
    offset: int
