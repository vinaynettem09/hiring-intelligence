"""Structured Work Sample models — the evidence-collection instrument.

A `StructuredWorkSample` belongs to one Campaign and holds ordered `WorkSampleTask`s.
Each task exists to elicit evidence about one or more competencies from the campaign's
frozen Role Profile (`competencies` = names referencing that profile) and carries a
recruiter-facing `evidence_intent` — NOT an answer key, NOT scoring. Scoring/AI live
elsewhere (Epic 5). While the campaign is a draft the sample is editable; once the
campaign is active it is frozen (INV-003), so a candidate's response is always
interpretable against the exact task/prompt that produced it.
"""

from datetime import UTC, datetime

from sqlalchemy import JSON, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.db import Base


def _utcnow() -> datetime:
    return datetime.now(UTC)


class StructuredWorkSample(Base):
    __tablename__ = "structured_work_samples"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id"), nullable=False, index=True
    )
    # One work sample per campaign.
    campaign_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("campaigns.id"), nullable=False, unique=True, index=True
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    introduction: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow, nullable=False
    )


class WorkSampleTask(Base):
    __tablename__ = "work_sample_tasks"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    organization_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("organizations.id"), nullable=False, index=True
    )
    work_sample_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("structured_work_samples.id"), nullable=False, index=True
    )
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    instructions: Mapped[str | None] = mapped_column(Text, nullable=True)
    # What evidence this task is meant to elicit (recruiter-facing; not shown to candidates).
    evidence_intent: Mapped[str] = mapped_column(Text, nullable=False)
    task_type: Mapped[str] = mapped_column(String(32), nullable=False)
    # Competency names from the campaign's Role Profile this task measures (≥1).
    competencies: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    display_order: Mapped[int] = mapped_column(Integer, nullable=False)
    expected_effort_minutes: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow, nullable=False
    )
