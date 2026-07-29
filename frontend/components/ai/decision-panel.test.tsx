import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";

import type { DecisionHistoryResponse } from "@/types/decision";

import { DecisionPanel } from "./decision-panel";

vi.mock("@/services/decision-service", () => ({
  DecisionService: { record: vi.fn().mockResolvedValue({ data: {} }) },
}));
import { DecisionService } from "@/services/decision-service";

const record = vi.mocked(DecisionService.record);

function renderPanel(over: Partial<React.ComponentProps<typeof DecisionPanel>> = {}) {
  const onRecorded = vi.fn();
  render(
    <DecisionPanel
      candidateEvaluationId="ce-1"
      informingEvaluationId="ev-1"
      informingRunNumber={2}
      history={null}
      onRecorded={onRecorded}
      {...over}
    />,
  );
  return { onRecorded };
}

describe("DecisionPanel — the accountable human decision", () => {
  beforeEach(() => record.mockClear());

  it("offers Advance / Hold / Decline and pre-selects NONE (AI never auto-decides)", () => {
    renderPanel();
    for (const verb of ["Advance", "Hold", "Decline"]) {
      const btn = screen.getByRole("button", { name: verb });
      expect(btn).toHaveAttribute("aria-pressed", "false");
    }
    // No decision is recorded just by viewing an AI recommendation.
    expect(record).not.toHaveBeenCalled();
  });

  it("references the informing AI run without letting it drive the decision", () => {
    renderPanel();
    expect(screen.getByText(/reference evaluation run 2/i)).toBeInTheDocument();
  });

  it("records the human's choice (rationale optional) and exposes return-to-work", async () => {
    const user = userEvent.setup();
    const { onRecorded } = renderPanel();

    await user.click(screen.getByRole("button", { name: "Decline" }));
    // Rationale is optional — record without typing one.
    await user.click(screen.getByRole("button", { name: /record decline/i }));

    await waitFor(() => expect(record).toHaveBeenCalledTimes(1));
    expect(record).toHaveBeenCalledWith("ce-1", {
      decision: "DECLINE",
      rationale: null,
      evaluation_id: "ev-1",
    });
    // The page (which owns the router + the "Review queue" return action) is notified.
    expect(onRecorded).toHaveBeenCalledTimes(1);
  });

  it("a decision can be recorded even with no AI evaluation to reference", async () => {
    const user = userEvent.setup();
    renderPanel({ informingEvaluationId: null, informingRunNumber: null });
    await user.click(screen.getByRole("button", { name: "Hold" }));
    await user.click(screen.getByRole("button", { name: /record hold/i }));
    await waitFor(() => expect(record).toHaveBeenCalledTimes(1));
    expect(record.mock.calls[0][1].evaluation_id).toBeNull();
  });

  it("shows the current decision + who/when when one exists (append-only history)", () => {
    const history: DecisionHistoryResponse = {
      candidate_evaluation_id: "ce-1",
      latest: {
        id: "d-2",
        decision: "ADVANCE",
        rationale: null,
        decided_by_email: "recruiter@acme.com",
        decided_at: "2026-07-29T10:00:00Z",
        informed_by_run_number: 2,
        created_at: "2026-07-29T10:00:00Z",
      },
      decisions: [
        {
          id: "d-2",
          decision: "ADVANCE",
          rationale: null,
          decided_by_email: "recruiter@acme.com",
          decided_at: "2026-07-29T10:00:00Z",
          informed_by_run_number: 2,
          created_at: "2026-07-29T10:00:00Z",
        },
      ],
    };
    renderPanel({ history });
    expect(screen.getByText("Advanced")).toBeInTheDocument();
    expect(screen.getByText(/recruiter@acme\.com/)).toBeInTheDocument();
  });
});
