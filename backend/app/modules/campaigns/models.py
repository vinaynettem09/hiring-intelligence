"""Campaign ORM model. Tiny — only what Story 2.1 needs.

A Campaign is the first **tenant-owned** business resource: it belongs to exactly
one organization (INV-001) and is only ever reached through a tenant-scoped read.
Like the identity models, it never leaves the repository/service layer — the API
sees Pydantic DTOs (schemas.py).
"""

from datetime import UTC, datetime
from typing import Any

from sqlalchemy import JSON, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.modules.campaigns.enums import CampaignStatus
from app.shared.db import Base
from app.shared.errors import BusinessRuleViolation, ConflictError


def _utcnow() -> datetime:
    return datetime.now(UTC)


class Campaign(Base):
    """An evaluation campaign: a role, its calibration (role_profile), and a status.

    `organization_id` is the tenant owner and is never reassigned after creation
    (INV-001). `status` stores a `CampaignStatus` value; a campaign is born `draft`.
    `role_profile` is the calibration (competencies + hiring bar) — stored as JSON
    (JSONB on Postgres) so it can evolve without a migration while still draft.
    """

    __tablename__ = "campaigns"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id"), nullable=False, index=True
    )
    role_title: Mapped[str] = mapped_column(String(255), nullable=False)
    # Calibration for the role. Shape is validated at the API boundary (RoleProfile
    # DTO); persisted as an opaque document here.
    role_profile: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow, nullable=False
    )

    # --- Lifecycle (the state machine lives here, in one place — Story 2.2) ---
    # Legal transitions:  draft --activate()--> active --conclude()--> concluded
    # Anything else raises. Once past draft, configuration is frozen forever
    # (INV-003) and the campaign can never return to an earlier state (INV-005).

    def assert_can_activate(self) -> None:
        """The model's own activation preconditions (non-mutating): must be a draft
        (INV-005 no reopening) and have the minimum a viable evaluation requires. The
        service layer adds cross-aggregate readiness (a valid work sample) between this
        check and the actual transition."""
        if self.status != CampaignStatus.DRAFT.value:
            # Covers both "already active" and "concluded" (no reopening, INV-005).
            raise ConflictError(
                "Only a draft campaign can be activated.",
                code="CAMPAIGN_NOT_DRAFT",
                metadata={"current_status": self.status},
            )
        self._assert_ready_for_activation()

    def activate(self) -> None:
        """Transition draft → active. A **point of no return**: it freezes the role
        profile / calibration as the trusted input to evaluation (INV-003), and there is
        no path back to draft (INV-005)."""
        self.assert_can_activate()
        self.status = CampaignStatus.ACTIVE.value

    def _assert_ready_for_activation(self) -> None:
        """The minimum a campaign needs to be a trustworthy evaluation. Today a draft
        already satisfies this (creation validates the role profile), but activation
        is the gate that *guarantees* it — so the rule survives future changes that
        might allow thinner drafts."""
        profile = self.role_profile or {}
        if not self.role_title.strip() or not profile.get("competencies") or not profile.get("bar"):
            raise BusinessRuleViolation(
                "Campaign is missing information required for activation "
                "(a role title, at least one competency, and a hiring bar).",
                code="CAMPAIGN_INCOMPLETE",
            )
