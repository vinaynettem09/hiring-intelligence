"""Invitation service tests — issuance rules, security, and candidate resolution."""

import re
from datetime import UTC, datetime, timedelta

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from support import define_minimal_work_sample

from app.modules.audit.models import AuditEvent
from app.modules.campaigns.enums import CampaignStatus
from app.modules.campaigns.models import Campaign
from app.modules.campaigns.schemas import Competency, CreateCampaignRequest, RoleProfile
from app.modules.campaigns.service import CampaignService
from app.modules.candidates.schemas import AddCandidateRequest
from app.modules.candidates.service import CandidateService
from app.modules.identity.schemas import SignupRequest
from app.modules.identity.service import IdentityService
from app.modules.invitations.emails import build_invitation_email
from app.modules.invitations.models import Invitation
from app.modules.invitations.repository import InvitationRepository
from app.modules.invitations.service import CandidateAccessService, InvitationService
from app.platform.email import EmailMessage, SmtpEmailProvider, get_email_provider
from app.shared.errors import ConflictError, NotFoundError
from app.shared.tokens import generate_opaque_token, hash_opaque_token


class _FakeEmail:
    def __init__(self) -> None:
        self.sent: list[EmailMessage] = []

    async def send(self, message: EmailMessage) -> None:
        self.sent.append(message)


def _campaign_request() -> CreateCampaignRequest:
    return CreateCampaignRequest(
        role_title="Data Engineer",
        role_profile=RoleProfile(competencies=[Competency(name="SQL")], bar="senior"),
    )


async def _make_org(
    session: AsyncSession, *, name: str = "Acme", email: str = "founder@acme.com"
) -> str:
    signup = await IdentityService(session).signup(
        SignupRequest(organization_name=name, email=email, password="password123")
    )
    return signup.organization.id


async def _evaluation(session: AsyncSession, tenant: str) -> str:
    # A candidate can only be added to an active campaign (INV-008), so an evaluation
    # always starts life on an active campaign.
    service = CampaignService(session, tenant)
    campaign = await service.create(_campaign_request())
    await define_minimal_work_sample(session, tenant, campaign.id)  # required to activate
    await service.activate(campaign.id)
    result = await CandidateService(session, tenant).add_to_campaign(
        campaign.id, AddCandidateRequest(name="Ada Lovelace", email="ada@x.com")
    )
    return result.id


def _token_from_email(message: EmailMessage) -> str:
    match = re.search(r"/invite/(\S+)", message.text_body)
    assert match is not None
    return match.group(1)


async def test_issue_sends_email_and_stores_only_a_hash(session: AsyncSession) -> None:
    tenant = await _make_org(session)
    evaluation_id = await _evaluation(session, tenant)
    email = _FakeEmail()

    summary = await InvitationService(session, tenant, email).issue(
        evaluation_id, actor_user_id="user-1"
    )

    assert summary.candidate.email == "ada@x.com"
    assert summary.replaced_previous is False
    assert len(email.sent) == 1  # email-provider boundary exercised
    assert email.sent[0].to == "ada@x.com"

    # The raw token lives only in the link; the DB stores its hash and never the raw value.
    raw_token = _token_from_email(email.sent[0])
    stored = (await session.execute(select(Invitation))).scalars().all()
    assert len(stored) == 1
    assert stored[0].token_hash == hash_opaque_token(raw_token)
    assert stored[0].token_hash != raw_token
    assert "ada" not in raw_token.lower()  # token carries no PII

    events = (await session.execute(select(AuditEvent))).scalars().all()
    assert any(e.action == "invitation.issued" for e in events)
    assert all("token" not in str(e.details or {}) for e in events)


async def test_cannot_invite_when_campaign_not_active(session: AsyncSession) -> None:
    tenant = await _make_org(session)
    evaluation_id = await _evaluation(session, tenant)
    # Force the campaign out of `active` to exercise the guard (a future `concluded`
    # transition will produce this state; candidates can't be added to a draft).
    campaign = (await session.execute(select(Campaign))).scalars().one()
    campaign.status = CampaignStatus.DRAFT.value
    await session.flush()

    with pytest.raises(ConflictError) as exc:
        await InvitationService(session, tenant, _FakeEmail()).issue(
            evaluation_id, actor_user_id="user-1"
        )
    assert exc.value.code == "CAMPAIGN_NOT_ACTIVE"


async def test_cannot_invite_another_tenants_evaluation(session: AsyncSession) -> None:
    tenant_a = await _make_org(session, name="Acme", email="a@acme.com")
    evaluation_id = await _evaluation(session, tenant_a)
    tenant_b = await _make_org(session, name="Globex", email="b@globex.com")

    with pytest.raises(NotFoundError) as exc:
        await InvitationService(session, tenant_b, _FakeEmail()).issue(
            evaluation_id, actor_user_id="intruder"
        )
    assert exc.value.code == "EVALUATION_NOT_FOUND"


async def test_reinvite_replaces_previous_invitation(session: AsyncSession) -> None:
    tenant = await _make_org(session)
    evaluation_id = await _evaluation(session, tenant)
    email = _FakeEmail()
    service = InvitationService(session, tenant, email)

    await service.issue(evaluation_id, actor_user_id="user-1")
    second = await service.issue(evaluation_id, actor_user_id="user-1")

    assert second.replaced_previous is True
    first_token = _token_from_email(email.sent[0])
    second_token = _token_from_email(email.sent[1])
    with pytest.raises(NotFoundError) as exc:
        await CandidateAccessService(session).resolve(first_token)
    assert exc.value.code == "INVITATION_REVOKED"
    view = await CandidateAccessService(session).resolve(second_token)
    assert view.role_title == "Data Engineer"


async def test_resolve_returns_candidate_view_and_marks_accessed(session: AsyncSession) -> None:
    tenant = await _make_org(session)
    evaluation_id = await _evaluation(session, tenant)
    email = _FakeEmail()
    await InvitationService(session, tenant, email).issue(evaluation_id, actor_user_id="user-1")
    token = _token_from_email(email.sent[0])

    view = await CandidateAccessService(session).resolve(token)

    assert view.candidate_name == "Ada Lovelace"
    assert view.organization_name == "Acme"
    assert view.role_title == "Data Engineer"
    assert view.next_step == "consent"

    accessed = (await session.execute(select(Invitation))).scalars().one()
    assert accessed.accessed_at is not None
    events = (await session.execute(select(AuditEvent))).scalars().all()
    assert any(e.action == "invitation.accessed" and e.actor_type == "candidate" for e in events)


def test_email_provider_seam_defaults_to_smtp() -> None:
    assert isinstance(get_email_provider(), SmtpEmailProvider)


def test_invitation_email_has_link_and_hides_internal_terms() -> None:
    message = build_invitation_email(
        to="ada@x.com",
        candidate_name="Ada Lovelace",
        organization_name="Acme",
        role_title="Data Engineer",
        link="http://test/invite/tok123",
        expires_at=datetime(2030, 1, 1, tzinfo=UTC),
    )
    assert "http://test/invite/tok123" in message.text_body
    assert "http://test/invite/tok123" in message.html_body
    assert "Data Engineer" in message.subject
    assert "CandidateEvaluation" not in message.html_body  # no internal terminology


async def test_resolve_invalid_token_leaks_nothing(session: AsyncSession) -> None:
    with pytest.raises(NotFoundError) as exc:
        await CandidateAccessService(session).resolve("not-a-real-token")
    assert exc.value.code == "INVITATION_INVALID"


async def test_resolve_expired_token(session: AsyncSession) -> None:
    tenant = await _make_org(session)
    evaluation_id = await _evaluation(session, tenant)
    raw_token = generate_opaque_token()
    await InvitationRepository(session, tenant).create(
        candidate_evaluation_id=evaluation_id,
        token_hash=hash_opaque_token(raw_token),
        expires_at=datetime.now(UTC) - timedelta(days=1),  # already expired
    )
    with pytest.raises(NotFoundError) as exc:
        await CandidateAccessService(session).resolve(raw_token)
    assert exc.value.code == "INVITATION_EXPIRED"
