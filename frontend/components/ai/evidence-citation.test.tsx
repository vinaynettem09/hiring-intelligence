import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it } from "vitest";

import type { SubmittedEvidenceItem } from "@/types/evaluation";

import { EvidenceCitation } from "./evidence-citation";
import { EvidenceProvider } from "./evidence-context";

const item: SubmittedEvidenceItem = {
  evidence_id: "ev-uuid-internal",
  task_id: "task-1",
  task_number: 2,
  task_prompt: "Deduplicate a large events table, keeping the latest row per user.",
  evidence_intent: "Set-based reasoning.",
  response_text: "I'd use ROW_NUMBER() partitioned by user_id.",
  captured_at: "2026-07-29T10:00:00Z",
};

describe("Claim → Citation → Source evidence", () => {
  it("labels the citation by task position, never the internal evidence UUID", () => {
    render(
      <EvidenceProvider items={[item]}>
        <EvidenceCitation citation={{ evidence_id: "ev-uuid-internal", task_id: "task-1" }} />
      </EvidenceProvider>,
    );
    const chip = screen.getByRole("button", { name: /view source evidence: task 2/i });
    expect(chip).toHaveTextContent("Task 2");
    expect(chip).not.toHaveTextContent("ev-uuid-internal");
  });

  it("opens the source evidence (task prompt + verbatim response) on click", async () => {
    const user = userEvent.setup();
    render(
      <EvidenceProvider items={[item]}>
        <EvidenceCitation citation={{ evidence_id: "ev-uuid-internal", task_id: "task-1" }} />
      </EvidenceProvider>,
    );
    await user.click(screen.getByRole("button", { name: /view source evidence: task 2/i }));
    expect(
      await screen.findByText(/Deduplicate a large events table/i),
    ).toBeInTheDocument();
    expect(screen.getByText(/ROW_NUMBER\(\) partitioned by user_id/i)).toBeInTheDocument();
  });
});
