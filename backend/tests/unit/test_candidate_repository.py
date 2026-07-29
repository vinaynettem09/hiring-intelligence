"""CandidateRepository + CandidateEvaluationRepository tests — isolation on both new
aggregates (the per-aggregate security-regression pattern)."""

from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.candidates.repository import (
    CandidateEvaluationRepository,
    CandidateRepository,
)


async def test_candidate_create_and_find_by_email(session: AsyncSession) -> None:
    repo = CandidateRepository(session, tenant_id="org-a")
    created = await repo.create(name="Ada", email="ada@x.com", resume_object_key=None)

    assert created.id
    assert created.organization_id == "org-a"
    found = await repo.get_by_email("ada@x.com")
    assert found is not None and found.id == created.id


async def test_candidate_is_tenant_isolated(session: AsyncSession) -> None:
    org_a = CandidateRepository(session, tenant_id="org-a")
    org_b = CandidateRepository(session, tenant_id="org-b")
    created = await org_a.create(name="Ada", email="ada@x.com", resume_object_key=None)

    # Same email, other tenant → its own (absent) identity space.
    assert await org_b.get_by_email("ada@x.com") is None
    assert await org_b.get(created.id) is None
    assert await org_a.get(created.id) is not None


async def test_evaluation_create_and_lookup(session: AsyncSession) -> None:
    repo = CandidateEvaluationRepository(session, tenant_id="org-a")
    created = await repo.create(campaign_id="camp-a", candidate_id="cand-a")

    assert created.status == "invited"
    found = await repo.get_for_candidate_in_campaign(campaign_id="camp-a", candidate_id="cand-a")
    assert found is not None and found.id == created.id


async def test_evaluation_is_tenant_isolated(session: AsyncSession) -> None:
    org_a = CandidateEvaluationRepository(session, tenant_id="org-a")
    org_b = CandidateEvaluationRepository(session, tenant_id="org-b")
    await org_a.create(campaign_id="camp-a", candidate_id="cand-a")

    assert (
        await org_b.get_for_candidate_in_campaign(campaign_id="camp-a", candidate_id="cand-a")
        is None
    )
    assert (
        await org_a.get_for_candidate_in_campaign(campaign_id="camp-a", candidate_id="cand-a")
        is not None
    )


async def test_roster_joins_candidates_and_counts(session: AsyncSession) -> None:
    candidates = CandidateRepository(session, tenant_id="org-a")
    evaluations = CandidateEvaluationRepository(session, tenant_id="org-a")
    ada = await candidates.create(name="Ada", email="ada@x.com", resume_object_key="r1")
    grace = await candidates.create(name="Grace", email="grace@x.com", resume_object_key=None)
    await evaluations.create(campaign_id="camp-a", candidate_id=ada.id)
    await evaluations.create(campaign_id="camp-a", candidate_id=grace.id)

    roster = await evaluations.list_roster(campaign_id="camp-a", limit=10, offset=0)

    assert {candidate.name for _, candidate in roster} == {"Ada", "Grace"}
    assert await evaluations.count_for_campaign("camp-a") == 2
    assert await evaluations.count_missing_resume("camp-a") == 1  # Grace has no résumé


async def test_roster_is_tenant_isolated(session: AsyncSession) -> None:
    candidates = CandidateRepository(session, tenant_id="org-a")
    org_a = CandidateEvaluationRepository(session, tenant_id="org-a")
    org_b = CandidateEvaluationRepository(session, tenant_id="org-b")
    ada = await candidates.create(name="Ada", email="ada@x.com", resume_object_key=None)
    await org_a.create(campaign_id="camp-a", candidate_id=ada.id)

    assert await org_b.list_roster(campaign_id="camp-a", limit=10, offset=0) == []
    assert await org_b.count_for_campaign("camp-a") == 0
    assert await org_a.count_for_campaign("camp-a") == 1
