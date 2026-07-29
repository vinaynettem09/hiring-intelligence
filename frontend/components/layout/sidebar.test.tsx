import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import type { MeResponse } from "@/types/identity";

import { Sidebar } from "./sidebar";

const nav = vi.hoisted(() => ({ pathname: "/review-queue" }));
vi.mock("next/navigation", () => ({ usePathname: () => nav.pathname }));

const identity: MeResponse = {
  id: "u1",
  email: "recruiter@acme.com",
  role: "recruiter",
  organization: { id: "o1", name: "Acme" },
};

function renderSidebar(over: Partial<React.ComponentProps<typeof Sidebar>> = {}) {
  const onLogout = vi.fn();
  const onToggleCollapse = vi.fn();
  render(
    <Sidebar
      identity={identity}
      onLogout={onLogout}
      collapsed={false}
      onToggleCollapse={onToggleCollapse}
      {...over}
    />,
  );
  return { onLogout, onToggleCollapse };
}

describe("Sidebar — the recruiter shell rail", () => {
  it("shows only the real destinations and marks the active one", () => {
    nav.pathname = "/review-queue";
    renderSidebar();
    for (const label of ["Dashboard", "Review", "Campaigns"]) {
      expect(screen.getByRole("link", { name: label })).toBeInTheDocument();
    }
    // No invented destinations.
    expect(screen.queryByRole("link", { name: /settings|analytics|reports|billing/i })).toBeNull();
    expect(screen.getByRole("link", { name: "Review" })).toHaveAttribute("aria-current", "page");
  });

  it("keeps account + logout reachable", () => {
    renderSidebar();
    expect(screen.getByText("Acme")).toBeInTheDocument();
    expect(screen.getByText("recruiter@acme.com")).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /log out/i })).toBeInTheDocument();
  });

  it("toggles collapse via an accessible control", async () => {
    const user = userEvent.setup();
    const { onToggleCollapse } = renderSidebar({ collapsed: true });
    // Collapsed: labels remain accessible names even though visually sr-only.
    expect(screen.getByRole("link", { name: "Campaigns" })).toBeInTheDocument();
    await user.click(screen.getByRole("button", { name: /expand sidebar/i }));
    expect(onToggleCollapse).toHaveBeenCalledTimes(1);
  });
});
