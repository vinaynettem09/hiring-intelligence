"""Campaign lifecycle state-machine tests (Story 2.2).

Pure domain — no database. The transitions and their guards live on the model, so
they can be tested by constructing a Campaign in memory. This is where the product's
lifecycle promises (INV-003 freeze-on-activate, INV-005 no-reopening) are proven.
"""

import pytest

from app.modules.campaigns.enums import CampaignStatus
from app.modules.campaigns.models import Campaign
from app.shared.errors import BusinessRuleViolation, ConflictError

_PROFILE = {"competencies": [{"name": "SQL"}], "bar": "senior"}


def _campaign(status: CampaignStatus, *, profile: dict[str, object] | None = None) -> Campaign:
    return Campaign(
        id="c1",
        organization_id="org-a",
        role_title="Data Engineer",
        role_profile=_PROFILE if profile is None else profile,
        status=status.value,
    )


def test_draft_activates() -> None:
    campaign = _campaign(CampaignStatus.DRAFT)
    campaign.activate()
    assert campaign.status == CampaignStatus.ACTIVE.value


def test_activating_an_active_campaign_is_rejected() -> None:
    campaign = _campaign(CampaignStatus.ACTIVE)
    with pytest.raises(ConflictError) as exc:
        campaign.activate()
    assert exc.value.code == "CAMPAIGN_NOT_DRAFT"
    assert campaign.status == CampaignStatus.ACTIVE.value  # unchanged


def test_concluded_campaign_cannot_be_reactivated() -> None:
    # INV-005: once past draft there is no way back. A concluded campaign never
    # returns to active — you create a successor instead.
    campaign = _campaign(CampaignStatus.CONCLUDED)
    with pytest.raises(ConflictError) as exc:
        campaign.activate()
    assert exc.value.code == "CAMPAIGN_NOT_DRAFT"


def test_incomplete_campaign_cannot_activate() -> None:
    campaign = _campaign(CampaignStatus.DRAFT, profile={"competencies": [], "bar": ""})
    with pytest.raises(BusinessRuleViolation) as exc:
        campaign.activate()
    assert exc.value.code == "CAMPAIGN_INCOMPLETE"
    assert campaign.status == CampaignStatus.DRAFT.value  # stays draft
