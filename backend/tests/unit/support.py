"""Shared test helpers. From Story 4.3, activating a campaign requires a valid
Structured Work Sample that covers every competency (INV-011). These helpers define a
minimal valid work sample so activation-dependent tests reflect the real product flow.

From Story 5.1, `submitted_evaluation` drives the whole evidence-generation pipeline
(signup → campaign → work sample → activate → add candidate → invite → consent → answer
→ submit) so intelligence tests can start from a real, submitted evaluation with
immutable Evidence — exactly what the AI boundary consumes.
"""

import re
from dataclasses import dataclass

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.campaigns.schemas import Competency, CreateCampaignRequest, RoleProfile
from app.modules.campaigns.service import CampaignService
from app.modules.candidates.schemas import AddCandidateRequest
from app.modules.candidates.service import CandidateService
from app.modules.consent.service import ConsentService
from app.modules.identity.schemas import SignupRequest
from app.modules.identity.service import IdentityService
from app.modules.invitations.service import InvitationService
from app.modules.responses.service import CandidateWorkSampleService
from app.modules.worksample.schemas import DefineWorkSampleRequest, WorkSampleTaskInput
from app.modules.worksample.service import WorkSampleService
from app.platform.email import EmailMessage


async def define_minimal_work_sample(
    session: AsyncSession, tenant: str, campaign_id: str, competencies: tuple[str, ...] = ("SQL",)
) -> None:
    """One task covering every competency — the smallest instrument that can activate."""
    await WorkSampleService(session, tenant).define(
        campaign_id,
        DefineWorkSampleRequest(
            title="Work sample",
            tasks=[
                WorkSampleTaskInput(
                    prompt="Describe how you would approach this problem.",
                    evidence_intent="Look for structured, job-relevant reasoning.",
                    competencies=list(competencies),
                )
            ],
        ),
    )


def _auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


async def define_minimal_work_sample_via_api(
    client: AsyncClient,
    token: str,
    campaign_id: str,
    competencies: tuple[str, ...] = ("SQL",),
) -> None:
    await client.put(
        f"/campaigns/{campaign_id}/work-sample",
        json={
            "title": "Work sample",
            "tasks": [
                {
                    "prompt": "Describe how you would approach this problem.",
                    "evidence_intent": "Look for structured, job-relevant reasoning.",
                    "competencies": list(competencies),
                }
            ],
        },
        headers=_auth(token),
    )


class _FakeEmail:
    def __init__(self) -> None:
        self.sent: list[EmailMessage] = []

    async def send(self, message: EmailMessage) -> None:
        self.sent.append(message)


@dataclass
class SubmittedEvaluation:
    """A real, submitted evaluation + the PII we deliberately fed in, so tests can assert
    that PII never appears in the AI input the assembler builds from it."""

    tenant: str
    evaluation_id: str
    campaign_id: str
    token: str
    candidate_name: str
    candidate_email: str
    task_ids: list[str]


async def submitted_evaluation(
    session: AsyncSession,
    *,
    org: str = "Acme",
    user_email: str = "founder@acme.com",
    candidate_name: str = "Ada Lovelace",
    candidate_email: str = "ada.lovelace@example.com",
    competencies: tuple[str, ...] = ("SQL", "Python"),
    answers: tuple[str, ...] | None = None,
    submit: bool = True,
) -> SubmittedEvaluation:
    """Run the full pipeline to a submitted evaluation. One task per competency; `answers`
    (defaulted) become the immutable Evidence text, in task order. With `submit=False` the
    evaluation is left `invited` (no consent/evidence) — for asserting the AI refuses to
    run before submission."""
    signup = await IdentityService(session).signup(
        SignupRequest(organization_name=org, email=user_email, password="password123")
    )
    tenant = signup.organization.id
    campaigns = CampaignService(session, tenant)
    campaign = await campaigns.create(
        CreateCampaignRequest(
            role_title="Data Engineer",
            role_profile=RoleProfile(
                competencies=[
                    Competency(name=name, description=f"Ability in {name}.")
                    for name in competencies
                ],
                bar="Senior: ships production-quality work independently.",
            ),
        )
    )
    await WorkSampleService(session, tenant).define(
        campaign.id,
        DefineWorkSampleRequest(
            title="Work sample",
            tasks=[
                WorkSampleTaskInput(
                    prompt=f"Task for {name}.",
                    evidence_intent=f"Elicit evidence of {name}.",
                    competencies=[name],
                )
                for name in competencies
            ],
        ),
    )
    await campaigns.activate(campaign.id)
    evaluation = await CandidateService(session, tenant).add_to_campaign(
        campaign.id, AddCandidateRequest(name=candidate_name, email=candidate_email)
    )
    email = _FakeEmail()
    await InvitationService(session, tenant, email).issue(evaluation.id, actor_user_id="u")
    match = re.search(r"/invite/(\S+)", email.sent[0].text_body)
    assert match is not None
    token = match.group(1)

    task_ids: list[str] = []
    if submit:
        await ConsentService(session).grant(token)
        candidate_service = CandidateWorkSampleService(session)
        work_sample = await candidate_service.get_work_sample(token)
        replies = answers or tuple(
            f"My detailed answer for task {t.order}." for t in work_sample.tasks
        )
        task_ids = [t.task_id for t in work_sample.tasks]
        for task, reply in zip(work_sample.tasks, replies, strict=True):
            await candidate_service.save_response(token, task.task_id, reply)
        await candidate_service.submit(token)

    return SubmittedEvaluation(
        tenant=tenant,
        evaluation_id=evaluation.id,
        campaign_id=campaign.id,
        token=token,
        candidate_name=candidate_name,
        candidate_email=candidate_email,
        task_ids=task_ids,
    )
