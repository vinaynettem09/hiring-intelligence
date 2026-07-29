import { describe, expect, it } from "vitest";

import {
  CONFIDENCE_EXPLANATION,
  confidenceLevel,
  confidencePresentation,
  escalationReasonCopy,
  recommendationPresentation,
  recommendationShortLabel,
} from "./presentation";
import type { Recommendation } from "@/types/evaluation";

// These protect the product's deliberately-designed vocabulary: humane recommendation
// language, confidence as a LEVEL (never a probability/percentage), and the boundary copy.

describe("recommendation presentation", () => {
  const cases: Array<[Recommendation, string, string]> = [
    ["STRONG_PROCEED", "Strong evidence to proceed", "positive"],
    ["PROCEED", "Evidence supports proceeding", "positive"],
    ["MIXED", "Mixed evidence", "moderate"],
    ["DO_NOT_PROCEED", "Evidence does not support proceeding", "negative"],
    ["ESCALATE", "Human review needed", "review"],
  ];

  it.each(cases)("%s → humane label + tone (never raw enum)", (rec, label, tone) => {
    const p = recommendationPresentation(rec);
    expect(p.label).toBe(label);
    expect(p.tone).toBe(tone);
    expect(p.label).not.toContain(rec); // never leaks the enum token
  });

  it("ESCALATE reads as human review, never candidate failure", () => {
    expect(recommendationPresentation("ESCALATE").label.toLowerCase()).toContain("human review");
    expect(recommendationShortLabel("ESCALATE")).toBe("Human review");
  });

  it("DO_NOT_PROCEED is never punitive 'reject' language", () => {
    const all = [
      recommendationPresentation("DO_NOT_PROCEED").label,
      recommendationPresentation("DO_NOT_PROCEED").detail,
      recommendationShortLabel("DO_NOT_PROCEED"),
    ].join(" ");
    expect(all.toLowerCase()).not.toContain("reject");
  });
});

describe("evidence confidence", () => {
  it("maps values to Low/Moderate/High LEVELS", () => {
    expect(confidenceLevel(1.0)).toBe("high");
    expect(confidenceLevel(0.7)).toBe("high");
    expect(confidenceLevel(0.5)).toBe("moderate");
    expect(confidenceLevel(0.4)).toBe("moderate");
    expect(confidenceLevel(0.2)).toBe("low");
  });

  it("labels say 'evidence confidence' and NEVER a percentage/probability", () => {
    for (const v of [0, 0.2, 0.5, 0.7, 1.0]) {
      const label = confidencePresentation(v).label;
      expect(label).toContain("evidence confidence");
      expect(label).not.toContain("%");
      expect(label.toLowerCase()).not.toContain("probability");
      expect(label).not.toContain("100");
    }
  });

  it("explanation states it is NOT a probability of success", () => {
    expect(CONFIDENCE_EXPLANATION.toLowerCase()).toContain("not a probability");
    expect(CONFIDENCE_EXPLANATION.toLowerCase()).toContain("succeed");
  });
});

describe("escalation reason copy", () => {
  it("insufficient evidence is about evidence, not the candidate", () => {
    const copy = escalationReasonCopy("INSUFFICIENT_EVIDENCE")!;
    expect(copy.toLowerCase()).toContain("evidence");
    expect(copy.toLowerCase()).not.toContain("weak candidate");
  });

  it("returns null when there is no escalation", () => {
    expect(escalationReasonCopy(null)).toBeNull();
  });
});
