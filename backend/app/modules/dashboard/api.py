"""FastAPI route for the recruiter dashboard read model.

- GET /dashboard — the authenticated tenant's home metrics (Story D1).

Protected: `require_auth` supplies the tenant from the verified token.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.dashboard.schemas import DashboardResponse
from app.modules.dashboard.service import DashboardService
from app.shared.context import AuthContext, require_auth
from app.shared.db import get_session

router = APIRouter(tags=["dashboard"])


@router.get("/dashboard")
async def get_dashboard(
    auth: AuthContext = Depends(require_auth),
    session: AsyncSession = Depends(get_session),
) -> DashboardResponse:
    return await DashboardService(session, auth.organization_id).get()
