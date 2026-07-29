"""FastAPI routes for the Structured Work Sample (recruiter).

- GET /campaigns/{id}/work-sample — the current definition + coverage + editability.
- PUT /campaigns/{id}/work-sample — define the whole work sample (draft campaigns only).

The application operation is "define the work sample", not granular question CRUD.
Protected: tenant comes from the verified token.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.worksample.schemas import DefineWorkSampleRequest, WorkSampleResponse
from app.modules.worksample.service import WorkSampleService
from app.shared.context import AuthContext, require_auth
from app.shared.db import get_session

router = APIRouter(tags=["work-sample"])


@router.get("/campaigns/{campaign_id}/work-sample")
async def get_work_sample(
    campaign_id: str,
    auth: AuthContext = Depends(require_auth),
    session: AsyncSession = Depends(get_session),
) -> WorkSampleResponse:
    return await WorkSampleService(session, auth.organization_id).get(campaign_id)


@router.put("/campaigns/{campaign_id}/work-sample")
async def define_work_sample(
    campaign_id: str,
    payload: DefineWorkSampleRequest,
    auth: AuthContext = Depends(require_auth),
    session: AsyncSession = Depends(get_session),
) -> WorkSampleResponse:
    return await WorkSampleService(session, auth.organization_id).define(campaign_id, payload)
