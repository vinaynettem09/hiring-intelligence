import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { MockEvaluationNotice } from "./mock-evaluation-notice";

describe("MockEvaluationNotice — mock must never masquerade as real", () => {
  it("warns loudly when the run came from the mock provider", () => {
    render(<MockEvaluationNotice provider="mock" />);
    expect(screen.getByText(/development only/i)).toBeInTheDocument();
    expect(screen.getByText(/not a real model assessment/i)).toBeInTheDocument();
  });

  it("renders nothing for a real provider (provider not marketed in primary UX)", () => {
    const { container } = render(<MockEvaluationNotice provider="gemini" />);
    expect(container).toBeEmptyDOMElement();
  });
});
