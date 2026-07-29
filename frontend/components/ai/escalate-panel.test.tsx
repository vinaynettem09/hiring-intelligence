import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { EscalatePanel } from "./escalate-panel";
import { makeEvaluationDetail } from "./test-fixtures";

describe("EscalatePanel — uncertainty as a feature, not candidate failure", () => {
  it("frames ESCALATE as human review needed, explicitly not a weak-candidate judgement", () => {
    render(
      <EscalatePanel
        detail={makeEvaluationDetail({
          recommendation: "ESCALATE",
          escalation_reason: "INSUFFICIENT_EVIDENCE",
          confidence: 0.2,
        })}
      />,
    );
    expect(screen.getByText(/more human review is needed/i)).toBeInTheDocument();
    expect(
      screen.getByText(/not a judgement that the candidate is weak/i),
    ).toBeInTheDocument();
  });

  it("surfaces the concrete evidence gaps", () => {
    render(
      <EscalatePanel
        detail={makeEvaluationDetail({
          recommendation: "ESCALATE",
          escalation_reason: "INSUFFICIENT_EVIDENCE",
          evidence_coverage: {
            competencies_total: 3,
            competencies_assessed: 1,
            tasks_total: 3,
            tasks_with_evidence: 1,
          },
        })}
      />,
    );
    expect(screen.getByText(/2 of 3 competencies could not be grounded/i)).toBeInTheDocument();
  });
});
