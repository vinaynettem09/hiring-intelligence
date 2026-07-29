import { render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";

import { BreadcrumbProvider, Breadcrumbs, useBreadcrumbLabels } from "./breadcrumbs";

const nav = vi.hoisted(() => ({ pathname: "/" }));
vi.mock("next/navigation", () => ({ usePathname: () => nav.pathname }));

function Register({ map }: { map: Record<string, string> }) {
  useBreadcrumbLabels(map);
  return null;
}

describe("Breadcrumbs — deep-page sense of place", () => {
  it("renders nothing on top-level pages", () => {
    nav.pathname = "/dashboard";
    const { container } = render(
      <BreadcrumbProvider>
        <Breadcrumbs />
      </BreadcrumbProvider>,
    );
    expect(container).toBeEmptyDOMElement();
  });

  it("builds a labelled trail with the leaf marked aria-current", async () => {
    nav.pathname = "/campaigns/camp-1/candidates";
    render(
      <BreadcrumbProvider>
        <Register map={{ "camp-1": "Backend Engineer" }} />
        <Breadcrumbs />
      </BreadcrumbProvider>,
    );
    // Static segments + the page-supplied object label.
    expect(screen.getByRole("link", { name: "Campaigns" })).toHaveAttribute(
      "href",
      "/campaigns",
    );
    await waitFor(() =>
      expect(screen.getByRole("link", { name: "Backend Engineer" })).toBeInTheDocument(),
    );
    const leaf = screen.getByText("Candidates");
    expect(leaf).toHaveAttribute("aria-current", "page");
  });

  it("falls back to a positional label when no object label is supplied", () => {
    nav.pathname = "/campaigns/camp-1";
    render(
      <BreadcrumbProvider>
        <Breadcrumbs />
      </BreadcrumbProvider>,
    );
    // camp-1 with no registered label → "Campaign", and it's the current leaf.
    const leaf = screen.getByText("Campaign");
    expect(leaf).toHaveAttribute("aria-current", "page");
  });
});
