"""Consent persistence. Append-only: `create` inserts a grant; nothing here updates or
deletes one. Keyed by `candidate_evaluation_id`, which is always resolved server-side
from the candidate's token (never client-supplied), so this is inside the candidate
trust boundary rather than tenant-scoped."""

from collections.abc import Sequence
from datetime import UTC, datetime

from sqlalchemy import select

from app.modules.consent.models import Consent
from app.shared.ids import new_id
from app.shared.repository import Repository


class ConsentRepository(Repository):
    async def list_for_evaluation(self, candidate_evaluation_id: str) -> Sequence[Consent]:
        """All consent records for an evaluation, oldest first — the append-only consent
        history (grants + withdrawals) for the audit timeline."""
        stmt = (
            select(Consent)
            .where(Consent.candidate_evaluation_id == candidate_evaluation_id)
            .order_by(Consent.created_at)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def active_for_evaluation(self, candidate_evaluation_id: str) -> Consent | None:
        """The current active grant (not withdrawn), if any — the basis of active consent."""
        stmt = (
            select(Consent)
            .where(
                Consent.candidate_evaluation_id == candidate_evaluation_id,
                Consent.withdrawn_at.is_(None),
            )
            .order_by(Consent.created_at.desc())
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def active_for_version(
        self, candidate_evaluation_id: str, consent_version: str
    ) -> Consent | None:
        stmt = select(Consent).where(
            Consent.candidate_evaluation_id == candidate_evaluation_id,
            Consent.consent_version == consent_version,
            Consent.withdrawn_at.is_(None),
        )
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def create(
        self, *, organization_id: str, candidate_evaluation_id: str, consent_version: str
    ) -> Consent:
        consent = Consent(
            id=new_id(),
            organization_id=organization_id,
            candidate_evaluation_id=candidate_evaluation_id,
            consent_version=consent_version,
            consented_at=datetime.now(UTC),
        )
        self.session.add(consent)
        await self.session.flush()
        return consent
