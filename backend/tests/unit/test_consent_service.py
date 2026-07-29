"""Consent service tests — append-only versioned grants, idempotency, the active-consent
gate, spoof protection, and audit."""

import re
from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from support import define_minimal_work_sample

from app.modules.audit.models import AuditEvent
from app.modules.campaigns.schemas import Competency, CreateCampaignRequest, RoleProfile
from app.modules.campaigns.service import CampaignService
from app.modules.candidates.models import CandidateEvaluation
from app.modules.candidates.schemas import AddCandidateRequest
from app.modules.candidates.service import CandidateService
from app.modules.consent.content import CURRENT_CONSENT_VERSION
from app.modules.consent.models import Consent
from app.modules.consent.schemas import ConsentTokenRequest
from app.modules.consent.service import ConsentService
from app.modules.identity.schemas import SignupRequest
from app.modules.identity.service import IdentityService
from app.modules.invitations.repository import InvitationRepository
from app.modules.invitations.service import InvitationService
from app.platform.email import EmailMessage
from app.shared.errors import NotFoundError
from app.shared.tokens import generate_opaque_token, hash_opaque_token


class _FakeEmail:
    def __init__(self) -> None:
        self.sent: list[EmailMessage] = []

    async def send(self, message: EmailMessage) -> None:
        self.sent.append(message)


async def _invited(
    session: AsyncSession, *, org: str = "Acme", user_email: str = "founder@acme.com"
) -> tuple[str, str]:
    """Set up an org → active campaign → candidate → invitation. Returns (token, eval_id)."""
    signup = await IdentityService(session).signup(
        SignupRequest(organization_name=org, email=user_email, password="password123")
    )
    tenant = signup.organization.id
    campaigns = CampaignService(session, tenant)
    campaign = await campaigns.create(
        CreateCampaignRequest(
            role_title="Data Engineer",
            role_profile=RoleProfile(competencies=[Competency(name="SQL")], bar="senior"),
        )
    )
    await define_minimal_work_sample(session, tenant, campaign.id)  # required to activate
    await campaigns.activate(campaign.id)
    result = await CandidateService(session, tenant).add_to_campaign(
        campaign.id, AddCandidateRequest(name="Ada Lovelace", email="ada@x.com")
    )
    email = _FakeEmail()
    await InvitationService(session, tenant, email).issue(result.id, actor_user_id="user-1")
    match = re.search(r"/invite/(\S+)", email.sent[0].text_body)
    assert match is not None
    return match.group(1), result.id


async def test_get_state_before_grant(session: AsyncSession) -> None:
    token, _ = await _invited(session)
    state = await ConsentService(session).get_state(token)

    assert state.consented is False
    assert state.organization_name == "Acme"
    assert state.role_title == "Data Engineer"
    assert state.candidate_name == "Ada Lovelace"
    assert state.disclosure.version == CURRENT_CONSENT_VERSION
    assert len(state.disclosure.sections) >= 5


async def test_grant_records_versioned_consent_and_gate_flips(session: AsyncSession) -> None:
    token, evaluation_id = await _invited(session)
    service = ConsentService(session)

    assert await service.has_active_consent(evaluation_id) is False  # before

    state = await service.grant(token)

    assert state.consented is True
    assert await service.has_active_consent(evaluation_id) is True  # after
    consent = (await session.execute(select(Consent))).scalars().one()
    assert consent.candidate_evaluation_id == evaluation_id
    assert consent.consent_version == CURRENT_CONSENT_VERSION
    assert consent.consented_at is not None
    assert consent.withdrawn_at is None


async def test_grant_is_idempotent_for_same_version(session: AsyncSession) -> None:
    token, _ = await _invited(session)
    service = ConsentService(session)

    await service.grant(token)
    await service.grant(token)  # again

    count = (await session.execute(select(func.count()).select_from(Consent))).scalar_one()
    assert count == 1  # no duplicate grant


async def test_grant_writes_audit_without_secrets(session: AsyncSession) -> None:
    token, evaluation_id = await _invited(session)
    await ConsentService(session).grant(token)

    events = (await session.execute(select(AuditEvent))).scalars().all()
    granted = [e for e in events if e.action == "consent.granted"]
    assert len(granted) == 1
    assert granted[0].actor_type == "candidate"
    assert granted[0].target_id == evaluation_id
    assert granted[0].details is not None
    assert granted[0].details.get("consent_version") == CURRENT_CONSENT_VERSION
    assert "token" not in str(granted[0].details)


async def test_invalid_token_cannot_read_or_grant(session: AsyncSession) -> None:
    service = ConsentService(session)
    with pytest.raises(NotFoundError) as read_exc:
        await service.get_state("bogus")
    assert read_exc.value.code == "INVITATION_INVALID"
    with pytest.raises(NotFoundError) as grant_exc:
        await service.grant("bogus")
    assert grant_exc.value.code == "INVITATION_INVALID"


async def test_expired_invitation_cannot_grant(session: AsyncSession) -> None:
    signup = await IdentityService(session).signup(
        SignupRequest(organization_name="Acme", email="f@acme.com", password="password123")
    )
    tenant = signup.organization.id
    campaigns = CampaignService(session, tenant)
    campaign = await campaigns.create(
        CreateCampaignRequest(
            role_title="Data Engineer",
            role_profile=RoleProfile(competencies=[Competency(name="SQL")], bar="senior"),
        )
    )
    await define_minimal_work_sample(session, tenant, campaign.id)  # required to activate
    await campaigns.activate(campaign.id)
    result = await CandidateService(session, tenant).add_to_campaign(
        campaign.id, AddCandidateRequest(name="Ada", email="ada@x.com")
    )
    raw = generate_opaque_token()
    await InvitationRepository(session, tenant).create(
        candidate_evaluation_id=result.id,
        token_hash=hash_opaque_token(raw),
        expires_at=datetime.now(UTC) - timedelta(days=1),
    )
    with pytest.raises(NotFoundError) as exc:
        await ConsentService(session).grant(raw)
    assert exc.value.code == "INVITATION_EXPIRED"


async def test_revoked_invitation_cannot_grant(session: AsyncSession) -> None:
    # Re-issue revokes the first link; granting via the first token must fail.
    signup = await IdentityService(session).signup(
        SignupRequest(organization_name="Acme", email="f@acme.com", password="password123")
    )
    tenant = signup.organization.id
    campaigns = CampaignService(session, tenant)
    campaign = await campaigns.create(
        CreateCampaignRequest(
            role_title="Data Engineer",
            role_profile=RoleProfile(competencies=[Competency(name="SQL")], bar="senior"),
        )
    )
    await define_minimal_work_sample(session, tenant, campaign.id)  # required to activate
    await campaigns.activate(campaign.id)
    result = await CandidateService(session, tenant).add_to_campaign(
        campaign.id, AddCandidateRequest(name="Ada", email="ada@x.com")
    )
    email = _FakeEmail()
    invitations = InvitationService(session, tenant, email)
    await invitations.issue(result.id, actor_user_id="u")
    await invitations.issue(result.id, actor_user_id="u")  # revokes the first
    first_token = re.search(r"/invite/(\S+)", email.sent[0].text_body).group(1)  # type: ignore[union-attr]

    with pytest.raises(NotFoundError) as exc:
        await ConsentService(session).grant(first_token)
    assert exc.value.code == "INVITATION_REVOKED"


def test_consent_is_not_a_boolean_and_evaluation_stays_pii_free() -> None:
    # Consent is an append-only record, never a mutable flag on the evaluation.
    assert not hasattr(CandidateEvaluation, "consented")
    # The AI-visible evaluation carries no candidate PII.
    assert not hasattr(CandidateEvaluation, "name")
    assert not hasattr(CandidateEvaluation, "email")


def test_consent_request_accepts_only_a_token() -> None:
    # No evaluation_id / organization_id inputs → cross-eval/tenant consent is impossible.
    assert set(ConsentTokenRequest.model_fields) == {"token"}
