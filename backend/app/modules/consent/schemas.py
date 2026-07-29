"""Candidate-facing consent DTOs. No internal IDs, no tenant selection — the disclosure
content is served from the governed source, and consent state reflects the evaluation
resolved from the candidate's token."""

from typing import Literal

from pydantic import BaseModel


class ConsentTokenRequest(BaseModel):
    # The candidate's magic-link token — the ONLY input. The evaluation and tenant are
    # resolved server-side from it; the client never chooses them.
    token: str


class ConsentSectionDTO(BaseModel):
    key: str
    title: str
    body: str


class ConsentDisclosureDTO(BaseModel):
    version: str
    sections: list[ConsentSectionDTO]


class ConsentStateResponse(BaseModel):
    organization_name: str
    role_title: str
    candidate_name: str
    disclosure: ConsentDisclosureDTO
    consented: bool  # true when active consent exists for this evaluation
    next_step: Literal["work_sample"] = "work_sample"
