import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import type { ReviewQueueItem } from "@/types/review";

import { QueueItemCard } from "./queue-item-card";

function item(over: Partial<ReviewQueueItem> = {}): ReviewQueueItem {
  return {
    candidate_evaluation_id: "ce-1",
    candidate_name: "Ada Lovelace",
    candidate_email: "ada@x.com",
    campaign_id: "camp-1",
    role_title: "Data Engineer",
    stage: "EVALUATED",
    needs_attention: false,
    recommendation: "PROCEED",
    confidence: 0.9,
    run_number: 1,
    decision: null,
    last_activity_at: "2026-07-29T10:00:00Z",
    ...over,
  };
}

describe("QueueItemCard — situation understandable without opening it", () => {
  it("leads with the stage; AI recommendation/confidence are secondary", () => {
    render(<QueueItemCard item={item()} />);
    expect(screen.getByText("Ada Lovelace")).toBeInTheDocument();
    expect(screen.getByText("Evaluated")).toBeInTheDocument();
    // recommendation + evidence confidence, shown as supporting detail (never a %)
    expect(screen.getByText(/Proceed · High evidence confidence/i)).toBeInTheDocument();
    expect(document.body.textContent).not.toContain("%");
  });

  it("gives each stage exactly one contextual action + href", () => {
    const { rerender } = render(<QueueItemCard item={item({ stage: "EVALUATED" })} />);
    expect(screen.getByRole("link", { name: /view evaluation/i })).toHaveAttribute(
      "href",
      "/campaigns/camp-1/candidates/ce-1",
    );
    rerender(
      <QueueItemCard item={item({ stage: "NEEDS_REVIEW", recommendation: "ESCALATE", confidence: 0.2 })} />,
    );
    expect(screen.getByText("Human review needed")).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /review evidence/i })).toBeInTheDocument();
  });

  it("shows the human decision as a resolved-outcome badge when one exists", () => {
    render(<QueueItemCard item={item({ decision: "ADVANCE" })} />);
    expect(screen.getByText(/Decided: Advanced/i)).toBeInTheDocument();
  });
});
