import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";

import { AIRecommendationCard } from "./ai-recommendation-card";
import { makeEvaluationDetail } from "./test-fixtures";

describe("AIRecommendationCard — advisory, never a decision or a score", () => {
  it("shows the humane recommendation label, marked as AI-assisted", () => {
    render(<AIRecommendationCard detail={makeEvaluationDetail({ recommendation: "PROCEED" })} />);
    expect(screen.getByText("Evidence supports proceeding")).toBeInTheDocument();
    expect(screen.getByText(/AI-assisted assessment/i)).toBeInTheDocument();
  });

  it("states the human-decides boundary and never claims to be the decision", () => {
    render(<AIRecommendationCard detail={makeEvaluationDetail()} />);
    expect(screen.getByText(/final decisions remain with your hiring team/i)).toBeInTheDocument();
    const body = document.body.textContent ?? "";
    expect(body.toLowerCase()).not.toContain("ai decision");
    expect(body.toLowerCase()).not.toContain("hire");
    expect(body.toLowerCase()).not.toContain("reject");
  });

  it("renders confidence as a LEVEL and never as a percentage/probability", () => {
    render(<AIRecommendationCard detail={makeEvaluationDetail({ confidence: 1.0 })} />);
    expect(screen.getByText(/High evidence confidence/i)).toBeInTheDocument();
    const body = document.body.textContent ?? "";
    expect(body).not.toContain("%");
    expect(body).not.toContain("100");
    expect(body.toLowerCase()).not.toContain("probability of success");
  });

  it("keeps recommendation and confidence as distinct signals", () => {
    // A negative call can still carry HIGH confidence (orthogonal).
    render(
      <AIRecommendationCard
        detail={makeEvaluationDetail({ recommendation: "DO_NOT_PROCEED", confidence: 0.95 })}
      />,
    );
    expect(screen.getByText("Evidence does not support proceeding")).toBeInTheDocument();
    expect(screen.getByText(/High evidence confidence/i)).toBeInTheDocument();
  });

  it("only reveals the raw reliability score inside the explanation, on request", async () => {
    const user = userEvent.setup();
    render(<AIRecommendationCard detail={makeEvaluationDetail({ confidence: 0.5 })} />);
    expect(document.body.textContent).not.toContain("0.50");
    await user.click(screen.getByRole("button", { name: /what does this mean/i }));
    expect(screen.getByText(/reliability score/i)).toBeInTheDocument();
    expect(screen.getByText(/0.50/)).toBeInTheDocument(); // a score out of 1.0, not a %
  });
});
