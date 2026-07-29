import { render } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { axe } from "vitest-axe";

import { AIRecommendationCard } from "./ai-recommendation-card";
import { makeEvaluationDetail } from "./test-fixtures";
import { QueueItemCard } from "@/components/review/queue-item-card";
import type { ReviewQueueItem } from "@/types/review";

// Automated axe pass on two high-value surfaces. NOT a claim of full WCAG compliance —
// a fast guard against obvious violations (labels, roles, name/role/value).
const AXE_OPTS = { rules: { region: { enabled: false } } };

const queueItem: ReviewQueueItem = {
  candidate_evaluation_id: "ce-1",
  candidate_name: "Ada Lovelace",
  candidate_email: "ada@x.com",
  campaign_id: "camp-1",
  role_title: "Data Engineer",
  stage: "NEEDS_REVIEW",
  needs_attention: true,
  recommendation: "ESCALATE",
  confidence: 0.2,
  run_number: 1,
  decision: null,
  last_activity_at: "2026-07-29T10:00:00Z",
};

describe("accessibility (axe)", () => {
  it("AIRecommendationCard has no obvious violations", async () => {
    const { container } = render(
      <AIRecommendationCard detail={makeEvaluationDetail({ recommendation: "MIXED", confidence: 0.5 })} />,
    );
    const results = await axe(container, AXE_OPTS);
    expect(results.violations).toEqual([]);
  });

  it("QueueItemCard has no obvious violations", async () => {
    const { container } = render(<QueueItemCard item={queueItem} />);
    const results = await axe(container, AXE_OPTS);
    expect(results.violations).toEqual([]);
  });
});
