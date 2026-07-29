"""Human hiring-decision vocabulary.

A decision is the accountable HUMAN act — deliberately distinct from the AI's
`RecommendationProposal`. The AI proposes (PROCEED/MIXED/…); a person decides
(ADVANCE/HOLD/DECLINE). There is no path by which an AI recommendation becomes a decision.
"""

from enum import StrEnum


class DecisionType(StrEnum):
    ADVANCE = "ADVANCE"  # move the candidate forward
    HOLD = "HOLD"  # not yet — revisit later
    DECLINE = "DECLINE"  # do not move forward (a human judgement, never "the AI rejected")
