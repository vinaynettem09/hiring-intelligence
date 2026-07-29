import { describe, expect, it } from "vitest";

import type { ReviewQueueItem } from "@/types/review";

import { activityLabel, queueHref, queuePresentation } from "./queue-presentation";

function item(over: Partial<ReviewQueueItem> = {}): ReviewQueueItem {
  return {
    candidate_evaluation_id: "ce-1",
    candidate_name: "Ada Lovelace",
    candidate_email: "ada@x.com",
    campaign_id: "camp-1",
    role_title: "Data Engineer",
    stage: "READY_FOR_EVALUATION",
    needs_attention: true,
    recommendation: null,
    confidence: null,
    run_number: null,
    decision: null,
    last_activity_at: new Date().toISOString(),
    ...over,
  };
}

describe("queue stage → operational language", () => {
  it("READY reads as 'Awaiting evaluation' (not 'candidate hasn't started')", () => {
    expect(queuePresentation(item({ stage: "READY_FOR_EVALUATION" })).stageLabel).toBe(
      "Awaiting evaluation",
    );
  });

  it("NEEDS_REVIEW distinguishes ESCALATE (human review) from MIXED", () => {
    const escalate = queuePresentation(
      item({ stage: "NEEDS_REVIEW", recommendation: "ESCALATE" }),
    );
    const mixed = queuePresentation(item({ stage: "NEEDS_REVIEW", recommendation: "MIXED" }));
    expect(escalate.stageLabel).toBe("Human review needed");
    expect(mixed.stageLabel).toBe("Review mixed evidence");
  });

  it("waiting-on-candidate and completed are visually quiet", () => {
    expect(queuePresentation(item({ stage: "AWAITING_CANDIDATE" })).quiet).toBe(true);
    expect(queuePresentation(item({ stage: "EVALUATED" })).quiet).toBe(true);
    expect(queuePresentation(item({ stage: "READY_FOR_EVALUATION" })).quiet).toBe(false);
  });
});

describe("queue actions route correctly", () => {
  it("evaluation stages open the workspace; waiting stages open the roster", () => {
    expect(queueHref(item({ stage: "EVALUATED" }))).toBe(
      "/campaigns/camp-1/candidates/ce-1",
    );
    expect(queueHref(item({ stage: "READY_FOR_EVALUATION" }))).toBe(
      "/campaigns/camp-1/candidates/ce-1",
    );
    expect(queueHref(item({ stage: "AWAITING_CANDIDATE" }))).toBe(
      "/campaigns/camp-1/candidates",
    );
  });
});

describe("activity label is meaningful per stage", () => {
  it("uses a stage-appropriate verb, not a bare timestamp", () => {
    expect(activityLabel(item({ stage: "READY_FOR_EVALUATION" }))).toMatch(/^Submitted /);
    expect(activityLabel(item({ stage: "EVALUATED" }))).toMatch(/^Evaluated /);
    expect(activityLabel(item({ stage: "AWAITING_CANDIDATE" }))).toMatch(/^Invited /);
    expect(activityLabel(item({ stage: "AWAITING_INVITATION" }))).toMatch(/^Added /);
  });
});
