"""WorkSampleService tests — definition, lifecycle freeze, competency coverage, the
activation gate, and tenant isolation."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.campaigns.schemas import Competency, CreateCampaignRequest, RoleProfile
from app.modules.campaigns.service import CampaignService
from app.modules.worksample.schemas import DefineWorkSampleRequest, WorkSampleTaskInput
from app.modules.worksample.service import WorkSampleService
from app.shared.errors import (
    BusinessRuleViolation,
    ConflictError,
    NotFoundError,
    ValidationError,
)


async def _draft_campaign(
    session: AsyncSession, tenant: str = "org-a", *, competencies: tuple[str, ...] = ("SQL",)
) -> str:
    created = await CampaignService(session, tenant).create(
        CreateCampaignRequest(
            role_title="Data Engineer",
            role_profile=RoleProfile(
                competencies=[Competency(name=c) for c in competencies], bar="senior"
            ),
        )
    )
    return created.id


def _task(
    prompt: str = "Explain your approach.", competencies: tuple[str, ...] = ("SQL",)
) -> WorkSampleTaskInput:
    return WorkSampleTaskInput(
        prompt=prompt,
        evidence_intent="Look for structured, job-relevant reasoning.",
        competencies=list(competencies),
        expected_effort_minutes=10,
    )


async def test_define_and_get_work_sample(session: AsyncSession) -> None:
    campaign_id = await _draft_campaign(session)
    service = WorkSampleService(session, "org-a")

    await service.define(campaign_id, DefineWorkSampleRequest(title="Backend WS", tasks=[_task()]))
    got = await service.get(campaign_id)

    assert got.exists is True
    assert got.editable is True  # draft
    assert got.title == "Backend WS"
    assert len(got.tasks) == 1
    assert got.tasks[0].competencies == ["SQL"]
    assert got.estimated_minutes == 10
    assert got.coverage.covered == ["SQL"]
    assert got.coverage.uncovered == []


async def test_define_replaces_previous_tasks_while_draft(session: AsyncSession) -> None:
    campaign_id = await _draft_campaign(session)
    service = WorkSampleService(session, "org-a")
    await service.define(campaign_id, DefineWorkSampleRequest(title="v1", tasks=[_task("A")]))

    result = await service.define(
        campaign_id, DefineWorkSampleRequest(title="v2", tasks=[_task("B"), _task("C")])
    )

    assert result.title == "v2"
    assert [t.prompt for t in result.tasks] == ["B", "C"]  # replaced, ordered


async def test_task_referencing_unknown_competency_is_rejected(session: AsyncSession) -> None:
    campaign_id = await _draft_campaign(session, competencies=("SQL",))
    with pytest.raises(ValidationError) as exc:
        await WorkSampleService(session, "org-a").define(
            campaign_id,
            DefineWorkSampleRequest(title="WS", tasks=[_task(competencies=("Kubernetes",))]),
        )
    assert exc.value.code == "WORK_SAMPLE_INVALID"


async def test_cross_tenant_read_and_write_blocked(session: AsyncSession) -> None:
    campaign_id = await _draft_campaign(session, tenant="org-a")
    other = WorkSampleService(session, "org-b")

    with pytest.raises(NotFoundError) as read_exc:
        await other.get(campaign_id)
    assert read_exc.value.code == "CAMPAIGN_NOT_FOUND"
    with pytest.raises(NotFoundError) as write_exc:
        await other.define(campaign_id, DefineWorkSampleRequest(title="x", tasks=[_task()]))
    assert write_exc.value.code == "CAMPAIGN_NOT_FOUND"


async def test_activation_requires_a_work_sample(session: AsyncSession) -> None:
    campaign_id = await _draft_campaign(session)  # no work sample defined
    with pytest.raises(BusinessRuleViolation) as exc:
        await CampaignService(session, "org-a").activate(campaign_id)
    assert exc.value.code == "CAMPAIGN_INCOMPLETE"
    assert exc.value.metadata == {"missing": "work_sample"}


async def test_activation_requires_full_competency_coverage(session: AsyncSession) -> None:
    campaign_id = await _draft_campaign(session, competencies=("SQL", "Python"))
    # Work sample covers only SQL, not Python.
    await WorkSampleService(session, "org-a").define(
        campaign_id, DefineWorkSampleRequest(title="WS", tasks=[_task(competencies=("SQL",))])
    )
    with pytest.raises(BusinessRuleViolation) as exc:
        await CampaignService(session, "org-a").activate(campaign_id)
    assert exc.value.code == "CAMPAIGN_INCOMPLETE"
    assert exc.value.metadata == {"uncovered_competencies": ["Python"]}


async def test_activation_succeeds_and_freezes_work_sample(session: AsyncSession) -> None:
    campaign_id = await _draft_campaign(session, competencies=("SQL", "Python"))
    service = WorkSampleService(session, "org-a")
    await service.define(
        campaign_id,
        DefineWorkSampleRequest(
            title="WS",
            tasks=[_task(competencies=("SQL", "Python"))],  # one task covers both
        ),
    )

    activated = await CampaignService(session, "org-a").activate(campaign_id)
    assert activated.status.value == "active"

    # Frozen: the work sample can no longer be edited, and reads are read-only.
    with pytest.raises(ConflictError) as exc:
        await service.define(campaign_id, DefineWorkSampleRequest(title="edit", tasks=[_task()]))
    assert exc.value.code == "WORK_SAMPLE_LOCKED"
    got = await service.get(campaign_id)
    assert got.editable is False
    assert got.tasks[0].prompt == "Explain your approach."  # historical prompt unchanged
