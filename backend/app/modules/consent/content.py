"""The governed consent disclosure — the single source of truth for **what** a
candidate is agreeing to. The version stamped onto every grant refers to exactly this
content. Changing the wording MUST mean bumping `CURRENT_CONSENT_VERSION` (a new
version), never silently altering what an existing consent record meant.

Plain language, honest scope. No unsupported legal or regulatory-compliance claims.
"""

from dataclasses import dataclass

CURRENT_CONSENT_VERSION = "mvp-2026-01"


@dataclass(frozen=True)
class ConsentSection:
    key: str
    title: str
    body: str


CONSENT_SECTIONS: tuple[ConsentSection, ...] = (
    ConsentSection(
        key="what",
        title="What you'll do",
        body="Complete a short, structured work sample relevant to the role — at your own pace.",
    ),
    ConsentSection(
        key="how_used",
        title="How it will be used",
        body=(
            "Your submission is evaluated to help the hiring team understand job-relevant "
            "evidence of your skills."
        ),
    ),
    ConsentSection(
        key="ai_assistance",
        title="AI assistance",
        body=(
            "AI may help analyze your submitted work. It does not make the hiring decision "
            "and does not act on its own."
        ),
    ),
    ConsentSection(
        key="human_decision",
        title="A person decides",
        body="A member of the hiring team remains responsible for the hiring decision.",
    ),
    ConsentSection(
        key="data_used",
        title="What data is used",
        body="Only the information needed for this evaluation is processed by the workflow.",
    ),
    ConsentSection(
        key="your_control",
        title="Your control",
        body=(
            "Your consent is recorded with the date and version you agreed to. If you want to "
            "withdraw it, you can contact the company — withdrawal is handled with care."
        ),
    ),
    ConsentSection(
        key="privacy",
        title="Privacy",
        body=(
            "Your submission is used for this evaluation and handled respectfully. We aim to "
            "process only what's necessary."
        ),
    ),
)
