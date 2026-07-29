import { describe, expect, it } from "vitest";

import { DECISION_ORDER, decisionPresentation } from "./decision-presentation";

// The human decision uses neutral, non-punitive language — never "reject"/"AI rejected".
describe("decision presentation", () => {
  it("offers exactly Advance / Hold / Decline as human actions", () => {
    expect(DECISION_ORDER).toEqual(["ADVANCE", "HOLD", "DECLINE"]);
    expect(DECISION_ORDER.map((d) => decisionPresentation(d).verb)).toEqual([
      "Advance",
      "Hold",
      "Decline",
    ]);
  });

  it("recorded-state labels are neutral (Declined, never 'Rejected')", () => {
    expect(decisionPresentation("ADVANCE").label).toBe("Advanced");
    expect(decisionPresentation("HOLD").label).toBe("On hold");
    expect(decisionPresentation("DECLINE").label).toBe("Declined");
    for (const d of DECISION_ORDER) {
      expect(decisionPresentation(d).label.toLowerCase()).not.toContain("reject");
    }
  });

  it("Decline is not styled as an error/destructive badge (a considered judgement)", () => {
    expect(decisionPresentation("DECLINE").badge).toBe("neutral");
    expect(decisionPresentation("ADVANCE").badge).toBe("success");
    expect(decisionPresentation("HOLD").badge).toBe("warning");
  });
});
