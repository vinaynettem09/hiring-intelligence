"""Campaign enums. Lifecycle states are an enum, never string literals.

The transition rules between these states (draft → active → concluded) live on the
`Campaign` model as methods (Story 2.2), so they are defined in one place rather than
re-checked at every call site. See `docs/domain-invariants.md`.
"""

from enum import StrEnum


class CampaignStatus(StrEnum):
    DRAFT = "draft"  # being set up; role_profile editable. Campaigns are born here.
    ACTIVE = "active"  # calibration frozen (INV-003); candidates assessed against it.
    CONCLUDED = "concluded"  # closed; no new assessments.
