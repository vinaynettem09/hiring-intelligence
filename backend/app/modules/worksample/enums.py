"""Work-sample task types. Intentionally narrow for the MVP: text-first gives the
cleanest evidence for evaluation. New types are added here when the product needs
them — the aggregate is designed so that doesn't require a rewrite."""

from enum import StrEnum


class TaskType(StrEnum):
    TEXT_RESPONSE = "text_response"
