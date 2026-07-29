"""FastAPI routes for the campaigns module.

- POST /campaigns                 — create a draft evaluation campaign (Story 2.1).
- POST /campaigns/{id}/activate   — draft → active, freezing configuration (Story 2.2).
- GET  /campaigns                 — list this org's campaigns, newest first (Story 2.3).
- GET  /campaigns/{id}            — one campaign's full detail (Story 2.3).

Protected: `require_auth` supplies the caller's tenant (from the verified token).
The tenant is passed to the service; it is never read from the request body or path.
"""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.campaigns.schemas import (
    CampaignListResponse,
    CampaignResponse,
    CreateCampaignRequest,
)
from app.modules.campaigns.service import CampaignService
from app.shared.context import AuthContext, require_auth
from app.shared.db import get_session

router = APIRouter(tags=["campaigns"])


@router.post("/campaigns", status_code=201)
async def create_campaign(
    payload: CreateCampaignRequest,
    auth: AuthContext = Depends(require_auth),
    session: AsyncSession = Depends(get_session),
) -> CampaignResponse:
    # Tenant comes from the verified token (auth.organization_id), never the body.
    return await CampaignService(session, auth.organization_id).create(payload)


@router.post("/campaigns/{campaign_id}/activate")
async def activate_campaign(
    campaign_id: str,
    auth: AuthContext = Depends(require_auth),
    session: AsyncSession = Depends(get_session),
) -> CampaignResponse:
    # Scoped to the caller's tenant: activating another org's campaign 404s.
    return await CampaignService(session, auth.organization_id).activate(campaign_id)


# Declared before the /{campaign_id} route so the static path matches first.
@router.get("/campaigns")
async def list_campaigns(
    auth: AuthContext = Depends(require_auth),
    session: AsyncSession = Depends(get_session),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> CampaignListResponse:
    # Only ever this org's campaigns (tenant from the token).
    return await CampaignService(session, auth.organization_id).list_campaigns(
        limit=limit, offset=offset
    )


@router.get("/campaigns/{campaign_id}")
async def get_campaign(
    campaign_id: str,
    auth: AuthContext = Depends(require_auth),
    session: AsyncSession = Depends(get_session),
) -> CampaignResponse:
    # Another org's campaign is indistinguishable from a missing one → 404.
    return await CampaignService(session, auth.organization_id).get(campaign_id)
