"""Evidence provenance. `source_type` makes explicit where a piece of evidence came
from, so the evaluation pipeline (Epic 5) can reason about it. Extends as new sensors
are added."""

from enum import StrEnum


class EvidenceSourceType(StrEnum):
    WORK_SAMPLE_RESPONSE = "work_sample_response"
