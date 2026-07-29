"""Candidate work-sample service tests — the three gates, candidate-safe DTO, autosave
upsert, resume, and cross-evaluation isolation."""

import re

import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.audit.models import AuditEvent
from app.modules.campaigns.schemas import Competency, CreateCampaignRequest, RoleProfile
from app.modules.campaigns.service import CampaignService
from app.modules.candidates.schemas import AddCandidateRequest
from app.modules.candidates.service import CandidateService
from app.modules.consent.service import ConsentService
from app.modules.identity.schemas import SignupRequest
from app.modules.identity.service import IdentityService
from app.modules.invitations.service import InvitationService
from app.modules.responses.models import WorkSampleResponse
from app.modules.responses.schemas import CandidateTaskView
from app.modules.responses.service import CandidateWorkSampleService
from app.modules.worksample.schemas import DefineWorkSampleRequest, WorkSampleTaskInput
from app.modules.worksample.service import WorkSampleService
from app.platform.email import EmailMessage
from app.shared.errors import AuthorizationError, NotFoundError


class _FakeEmail:
    def __init__(self) -> None:
        self.sent: list[EmailMessage] = []

    async def send(self, message: EmailMessage) -> None:
        self.sent.append(message)


def _task(prompt: str, competency: str) -> WorkSampleTaskInput:
    return WorkSampleTaskInput(
        prompt=prompt, evidence_intent="Look for reasoning.", competencies=[competency]
    )


async def _invited(
    session: AsyncSession, *, org: str = "Acme", user_email: str = "founder@acme.com"
) -> str:
    """Full setup → returns the candidate's invitation token (no consent yet)."""
    signup = await IdentityService(session).signup(
        SignupRequest(organization_name=org, email=user_email, password="password123")
    )
    tenant = signup.organization.id
    campaigns = CampaignService(session, tenant)
    campaign = await campaigns.create(
        CreateCampaignRequest(
            role_title="Data Engineer",
            role_profile=RoleProfile(
                competencies=[Competency(name="SQL"), Competency(name="Python")], bar="senior"
            ),
        )
    )
    await WorkSampleService(session, tenant).define(
        campaign.id,
        DefineWorkSampleRequest(
            title="WS", tasks=[_task("Task A", "SQL"), _task("Task B", "Python")]
        ),
    )
    await campaigns.activate(campaign.id)
    result = await CandidateService(session, tenant).add_to_campaign(
        campaign.id, AddCandidateRequest(name="Ada Lovelace", email="ada@x.com")
    )
    email = _FakeEmail()
    await InvitationService(session, tenant, email).issue(result.id, actor_user_id="u")
    match = re.search(r"/invite/(\S+)", email.sent[0].text_body)
    assert match is not None
    return match.group(1)


async def test_load_denied_without_consent(session: AsyncSession) -> None:
    token = await _invited(session)  # no consent granted
    with pytest.raises(AuthorizationError) as exc:
        await CandidateWorkSampleService(session).get_work_sample(token)
    assert exc.value.code == "CONSENT_REQUIRED"


async def test_load_after_consent_returns_candidate_view(session: AsyncSession) -> None:
    token = await _invited(session)
    await ConsentService(session).grant(token)

    ws = await CandidateWorkSampleService(session).get_work_sample(token)

    assert ws.organization_name == "Acme"
    assert ws.role_title == "Data Engineer"
    assert len(ws.tasks) == 2
    assert ws.tasks[0].order == 1
    assert ws.tasks[0].response_text == ""  # not started


async def test_save_upserts_and_survives_reload(session: AsyncSession) -> None:
    token = await _invited(session)
    await ConsentService(session).grant(token)
    service = CandidateWorkSampleService(session)
    ws = await service.get_work_sample(token)
    task_id = ws.tasks[0].task_id

    await service.save_response(token, task_id, "first draft")
    await service.save_response(token, task_id, "revised draft")  # autosave again

    count = (
        await session.execute(select(func.count()).select_from(WorkSampleResponse))
    ).scalar_one()
    assert count == 1  # upsert, not duplicate

    # A fresh service (new "session/request") sees the saved draft — server is authoritative.
    reloaded = await CandidateWorkSampleService(session).get_work_sample(token)
    saved = next(t for t in reloaded.tasks if t.task_id == task_id)
    assert saved.response_text == "revised draft"


async def test_task_from_another_work_sample_is_rejected(session: AsyncSession) -> None:
    token = await _invited(session)
    await ConsentService(session).grant(token)
    with pytest.raises(NotFoundError) as exc:
        await CandidateWorkSampleService(session).save_response(token, "not-a-real-task", "x")
    assert exc.value.code == "TASK_NOT_FOUND"


async def test_candidate_cannot_see_another_candidates_drafts(session: AsyncSession) -> None:
    token_a = await _invited(session, org="Acme", user_email="a@acme.com")
    token_b = await _invited(session, org="Globex", user_email="b@globex.com")
    await ConsentService(session).grant(token_a)
    await ConsentService(session).grant(token_b)
    service = CandidateWorkSampleService(session)
    ws_a = await service.get_work_sample(token_a)
    await service.save_response(token_a, ws_a.tasks[0].task_id, "A's private answer")

    ws_b = await service.get_work_sample(token_b)
    assert all(t.response_text == "" for t in ws_b.tasks)  # B sees none of A's work


async def test_invalid_token_denied(session: AsyncSession) -> None:
    service = CandidateWorkSampleService(session)
    with pytest.raises(NotFoundError) as exc:
        await service.get_work_sample("bogus")
    assert exc.value.code == "INVITATION_INVALID"


async def test_autosave_does_not_audit_every_save(session: AsyncSession) -> None:
    token = await _invited(session)
    await ConsentService(session).grant(token)
    service = CandidateWorkSampleService(session)
    ws = await service.get_work_sample(token)

    await service.save_response(token, ws.tasks[0].task_id, "one")
    await service.save_response(token, ws.tasks[0].task_id, "two")
    await service.save_response(token, ws.tasks[1].task_id, "three")

    started = (
        await session.execute(
            select(func.count())
            .select_from(AuditEvent)
            .where(AuditEvent.action == "work_sample.started")
        )
    ).scalar_one()
    assert started == 1  # once, not per save


def test_candidate_task_view_hides_recruiter_only_fields() -> None:
    fields = set(CandidateTaskView.model_fields)
    assert "evidence_intent" not in fields
    assert "competencies" not in fields
