"""Candidate-evaluation enums."""

from enum import StrEnum


class EvaluationStatus(StrEnum):
    # The candidate-evaluation lifecycle. Extends as later stories land.
    INVITED = "invited"  # added to the campaign
    SUBMITTED = "submitted"  # work sample completed + submitted → immutable Evidence exists
