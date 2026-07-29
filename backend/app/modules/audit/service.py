"""Audit service — the one way to append an audit event. Insert-only (never updates
or deletes), so the trail is immutable. Callers pass already-safe details (no secrets,
no raw tokens, PII-minimized)."""

from typing import Any

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.audit.models import AuditEvent
from app.shared.ids import new_id


class AuditService:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def record(
        self,
        *,
        organization_id: str,
        actor_type: str,
        action: str,
        target_type: str,
        target_id: str,
        actor_user_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        event = AuditEvent(
            id=new_id(),
            organization_id=organization_id,
            actor_type=actor_type,
            actor_user_id=actor_user_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            details=details,
        )
        self._session.add(event)
        await self._session.flush()  # committed with the request
