"""CandidateService tests (Story 3.1) — active-only intake, identity reuse, dedupe."""

import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from support import define_minimal_work_sample

from app.modules.campaigns.schemas import Competency, CreateCampaignRequest, RoleProfile
from app.modules.campaigns.service import CampaignService
from app.modules.candidates.enums import EvaluationStatus
from app.modules.candidates.schemas import AddCandidateRequest
from app.modules.candidates.service import CandidateService
from app.shared.errors import ConflictError, NotFoundError


def _campaign_request() -> CreateCampaignRequest:
    return CreateCampaignRequest(
        role_title="Data Engineer",
        role_profile=RoleProfile(competencies=[Competency(name="SQL")], bar="senior"),
    )


async def _active_campaign(session: AsyncSession, tenant: str = "org-a") -> str:
    service = CampaignService(session, tenant)
    created = await service.create(_campaign_request())
    await define_minimal_work_sample(session, tenant, created.id)  # required to activate
    await service.activate(created.id)
    return created.id


def _candidate(email: str = "ada@x.com") -> AddCandidateRequest:
    return AddCandidateRequest(name="Ada Lovelace", email=email, resume_object_key=None)


async def test_add_candidate_to_active_campaign(session: AsyncSession) -> None:
    campaign_id = await _active_campaign(session)

    result = await CandidateService(session, "org-a").add_to_campaign(campaign_id, _candidate())

    assert result.status is EvaluationStatus.INVITED
    assert result.campaign_id == campaign_id
    assert result.candidate.email == "ada@x.com"
    assert result.candidate.name == "Ada Lovelace"


async def test_same_email_reuses_identity_across_campaigns(session: AsyncSession) -> None:
    c1 = await _active_campaign(session)
    c2 = await _active_campaign(session)
    service = CandidateService(session, "org-a")

    r1 = await service.add_to_campaign(c1, _candidate())
    r2 = await service.add_to_campaign(c2, _candidate())

    assert r1.candidate.id == r2.candidate.id  # one identity record, reused
    assert r1.id != r2.id  # but distinct per-campaign evaluations


async def test_cannot_add_to_draft_campaign(session: AsyncSession) -> None:
    service = CampaignService(session, "org-a")
    draft = await service.create(_campaign_request())  # never activated

    with pytest.raises(ConflictError) as exc:
        await CandidateService(session, "org-a").add_to_campaign(draft.id, _candidate())
    assert exc.value.code == "CAMPAIGN_NOT_ACTIVE"


async def test_duplicate_candidate_in_campaign_is_rejected(session: AsyncSession) -> None:
    campaign_id = await _active_campaign(session)
    service = CandidateService(session, "org-a")
    await service.add_to_campaign(campaign_id, _candidate())

    with pytest.raises(ConflictError) as exc:
        await service.add_to_campaign(campaign_id, _candidate())
    assert exc.value.code == "CANDIDATE_ALREADY_IN_CAMPAIGN"


async def test_add_to_missing_campaign_raises_not_found(session: AsyncSession) -> None:
    with pytest.raises(NotFoundError) as exc:
        await CandidateService(session, "org-a").add_to_campaign("nope", _candidate())
    assert exc.value.code == "CAMPAIGN_NOT_FOUND"


async def test_cannot_add_to_another_tenants_campaign(session: AsyncSession) -> None:
    campaign_id = await _active_campaign(session, tenant="org-a")

    with pytest.raises(NotFoundError) as exc:
        await CandidateService(session, "org-b").add_to_campaign(campaign_id, _candidate())
    assert exc.value.code == "CAMPAIGN_NOT_FOUND"


async def test_import_reports_imported_skipped_failed(session: AsyncSession) -> None:
    campaign_id = await _active_campaign(session)
    service = CandidateService(session, "org-a")
    rows = [
        {"name": "Ada Lovelace", "email": "ada@x.com"},  # imported
        {"name": "Grace Hopper", "email": "grace@x.com"},  # imported
        {"name": "Bad Row", "email": "not-an-email"},  # failed (invalid email)
        {"name": "", "email": "noname@x.com"},  # failed (missing name)
        {"name": "Ada Again", "email": "ada@x.com"},  # skipped (dup within file)
    ]

    summary = await service.import_candidates(campaign_id, rows)

    assert summary.total == 5
    assert summary.imported == 2
    assert summary.failed == 2
    assert summary.skipped == 1
    outcomes = {issue.row: issue.outcome for issue in summary.issues}
    assert outcomes == {3: "failed", 4: "failed", 5: "skipped"}


async def test_import_reuses_identity_and_skips_existing(session: AsyncSession) -> None:
    campaign_id = await _active_campaign(session)
    service = CandidateService(session, "org-a")
    await service.add_to_campaign(campaign_id, _candidate("ada@x.com"))  # already present

    summary = await service.import_candidates(
        campaign_id,
        [{"name": "Ada", "email": "ada@x.com"}, {"name": "Grace", "email": "grace@x.com"}],
    )

    assert summary.imported == 1  # grace
    assert summary.skipped == 1  # ada already in campaign


async def test_import_to_draft_campaign_is_rejected(session: AsyncSession) -> None:
    draft = await CampaignService(session, "org-a").create(_campaign_request())
    with pytest.raises(ConflictError) as exc:
        await CandidateService(session, "org-a").import_candidates(
            draft.id, [{"name": "Ada", "email": "ada@x.com"}]
        )
    assert exc.value.code == "CAMPAIGN_NOT_ACTIVE"


async def test_import_to_another_tenants_campaign_is_not_found(session: AsyncSession) -> None:
    campaign_id = await _active_campaign(session, tenant="org-a")
    with pytest.raises(NotFoundError) as exc:
        await CandidateService(session, "org-b").import_candidates(
            campaign_id, [{"name": "Ada", "email": "ada@x.com"}]
        )
    assert exc.value.code == "CAMPAIGN_NOT_FOUND"


async def test_roster_returns_entries_and_attention_counts(session: AsyncSession) -> None:
    campaign_id = await _active_campaign(session)
    service = CandidateService(session, "org-a")
    await service.add_to_campaign(campaign_id, _candidate("ada@x.com"))  # no résumé
    await service.add_to_campaign(
        campaign_id, AddCandidateRequest(name="Grace", email="grace@x.com", resume_object_key="r")
    )

    roster = await service.list_roster(campaign_id, limit=10, offset=0)

    assert roster.total == 2
    assert roster.missing_resume == 1  # ada
    assert {entry.candidate.email for entry in roster.items} == {"ada@x.com", "grace@x.com"}
    assert {entry.status for entry in roster.items} == {EvaluationStatus.INVITED}


async def test_roster_of_missing_campaign_is_not_found(session: AsyncSession) -> None:
    with pytest.raises(NotFoundError) as exc:
        await CandidateService(session, "org-a").list_roster("nope", limit=10, offset=0)
    assert exc.value.code == "CAMPAIGN_NOT_FOUND"


async def test_cannot_view_another_tenants_roster(session: AsyncSession) -> None:
    campaign_id = await _active_campaign(session, tenant="org-a")
    with pytest.raises(NotFoundError) as exc:
        await CandidateService(session, "org-b").list_roster(campaign_id, limit=10, offset=0)
    assert exc.value.code == "CAMPAIGN_NOT_FOUND"
