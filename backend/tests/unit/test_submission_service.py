"""Submission → immutable Evidence tests — atomicity, idempotency, completeness,
immutability, PII boundary, ordering, gates, and cross-candidate isolation."""

import re

import pytest
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.audit.models import AuditEvent
from app.modules.campaigns.schemas import Competency, CreateCampaignRequest, RoleProfile
from app.modules.campaigns.service import CampaignService
from app.modules.candidates.enums import EvaluationStatus
from app.modules.candidates.models import CandidateEvaluation
from app.modules.candidates.schemas import AddCandidateRequest
from app.modules.candidates.service import CandidateService
from app.modules.consent.service import ConsentService
from app.modules.evidence.models import Evidence
from app.modules.evidence.repository import EvidenceRepository
from app.modules.identity.schemas import SignupRequest
from app.modules.identity.service import IdentityService
from app.modules.invitations.service import InvitationService
from app.modules.responses.schemas import SubmitWorkSampleRequest
from app.modules.responses.service import CandidateWorkSampleService
from app.modules.worksample.schemas import DefineWorkSampleRequest, WorkSampleTaskInput
from app.modules.worksample.service import WorkSampleService
from app.platform.email import EmailMessage
from app.shared.errors import (
    AuthorizationError,
    BusinessRuleViolation,
    ConflictError,
    NotFoundError,
)


class _FakeEmail:
    def __init__(self) -> None:
        self.sent: list[EmailMessage] = []

    async def send(self, message: EmailMessage) -> None:
        self.sent.append(message)


async def _invited(
    session: AsyncSession, *, org: str = "Acme", user_email: str = "founder@acme.com"
) -> str:
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
            title="WS",
            tasks=[
                WorkSampleTaskInput(prompt="A", evidence_intent="x", competencies=["SQL"]),
                WorkSampleTaskInput(prompt="B", evidence_intent="y", competencies=["Python"]),
            ],
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


async def _consented(session: AsyncSession, **kwargs: str) -> str:
    token = await _invited(session, **kwargs)
    await ConsentService(session).grant(token)
    return token


async def _answer_all(session: AsyncSession, token: str) -> None:
    service = CandidateWorkSampleService(session)
    ws = await service.get_work_sample(token)
    for task in ws.tasks:
        await service.save_response(token, task.task_id, f"answer {task.order}")


async def test_submit_creates_immutable_ordered_evidence(session: AsyncSession) -> None:
    token = await _consented(session)
    await _answer_all(session, token)

    result = await CandidateWorkSampleService(session).submit(token)

    assert result.evidence_count == 2
    assert result.submitted_at is not None
    candidate_evaluation_id = (
        (await session.execute(select(Evidence.candidate_evaluation_id))).scalars().first()
    )
    assert candidate_evaluation_id is not None
    evidence = await EvidenceRepository(session).list_for_evaluation(candidate_evaluation_id)
    assert [e.response_text for e in evidence] == ["answer 1", "answer 2"]  # snapshot, task order
    assert all(e.source_type == "work_sample_response" for e in evidence)

    evaluation = (await session.execute(select(CandidateEvaluation))).scalars().one()
    assert evaluation.status == EvaluationStatus.SUBMITTED.value
    assert evaluation.submitted_at is not None


async def test_submit_blocks_further_edits(session: AsyncSession) -> None:
    token = await _consented(session)
    await _answer_all(session, token)
    service = CandidateWorkSampleService(session)
    ws = await service.get_work_sample(token)
    await service.submit(token)

    with pytest.raises(ConflictError) as exc:
        await service.save_response(token, ws.tasks[0].task_id, "sneaky edit")
    assert exc.value.code == "WORK_SAMPLE_ALREADY_SUBMITTED"


async def test_incomplete_submission_is_atomic_and_rejected(session: AsyncSession) -> None:
    token = await _consented(session)
    service = CandidateWorkSampleService(session)
    ws = await service.get_work_sample(token)
    await service.save_response(token, ws.tasks[0].task_id, "only task 1")  # task 2 blank

    with pytest.raises(BusinessRuleViolation) as exc:
        await service.submit(token)
    assert exc.value.code == "WORK_SAMPLE_INCOMPLETE"
    assert exc.value.metadata == {
        "total_tasks": 2,
        "answered_tasks": 1,
        "missing_task_positions": [2],
    }
    # Nothing partial committed.
    assert (await session.execute(select(func.count()).select_from(Evidence))).scalar_one() == 0
    evaluation = (await session.execute(select(CandidateEvaluation))).scalars().one()
    assert evaluation.status == EvaluationStatus.INVITED.value
    submitted_audits = (
        await session.execute(
            select(func.count())
            .select_from(AuditEvent)
            .where(AuditEvent.action == "work_sample.submitted")
        )
    ).scalar_one()
    assert submitted_audits == 0


async def test_whitespace_only_response_is_incomplete(session: AsyncSession) -> None:
    token = await _consented(session)
    service = CandidateWorkSampleService(session)
    ws = await service.get_work_sample(token)
    await service.save_response(token, ws.tasks[0].task_id, "real")
    await service.save_response(token, ws.tasks[1].task_id, "    ")  # whitespace only

    with pytest.raises(BusinessRuleViolation) as exc:
        await service.submit(token)
    assert exc.value.code == "WORK_SAMPLE_INCOMPLETE"


async def test_submit_requires_consent(session: AsyncSession) -> None:
    token = await _invited(session)  # not consented
    with pytest.raises(AuthorizationError) as exc:
        await CandidateWorkSampleService(session).submit(token)
    assert exc.value.code == "CONSENT_REQUIRED"


async def test_submit_invalid_token(session: AsyncSession) -> None:
    with pytest.raises(NotFoundError) as exc:
        await CandidateWorkSampleService(session).submit("bogus")
    assert exc.value.code == "INVITATION_INVALID"


async def test_second_submission_is_idempotent(session: AsyncSession) -> None:
    token = await _consented(session)
    await _answer_all(session, token)
    service = CandidateWorkSampleService(session)

    first = await service.submit(token)
    second = await service.submit(token)  # double-submit / retry

    assert second.submitted_at == first.submitted_at
    assert (await session.execute(select(func.count()).select_from(Evidence))).scalar_one() == 2
    submitted_audits = (
        await session.execute(
            select(func.count())
            .select_from(AuditEvent)
            .where(AuditEvent.action == "work_sample.submitted")
        )
    ).scalar_one()
    assert submitted_audits == 1  # no duplicate audit fact


async def test_one_candidate_submission_does_not_affect_another(session: AsyncSession) -> None:
    token_a = await _consented(session, org="Acme", user_email="a@acme.com")
    token_b = await _consented(session, org="Globex", user_email="b@globex.com")
    await _answer_all(session, token_a)
    await CandidateWorkSampleService(session).submit(token_a)

    ws_b = await CandidateWorkSampleService(session).get_work_sample(token_b)
    assert ws_b.submitted is False


def test_evidence_has_no_pii_and_is_append_only() -> None:
    for field in ("name", "email", "phone", "candidate_name", "candidate_email"):
        assert not hasattr(Evidence, field)
    # Domain-language repository — no generic mutation.
    assert not hasattr(EvidenceRepository, "update")
    assert not hasattr(EvidenceRepository, "delete")


def test_submit_request_accepts_only_a_token() -> None:
    # No task ids / evaluation id from the client — spoofing can't influence submission.
    assert set(SubmitWorkSampleRequest.model_fields) == {"token"}
