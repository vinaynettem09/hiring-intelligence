import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";

const router = vi.hoisted(() => ({ push: vi.fn(), replace: vi.fn() }));
vi.mock("next/navigation", () => ({ useRouter: () => router }));
vi.mock("@/lib/auth-store", () => ({ authStore: { getAccess: () => "token" } }));
vi.mock("@/services/campaign-service", () => ({
  CampaignService: { create: vi.fn().mockResolvedValue({ data: { id: "camp-1" } }) },
}));
// The app mounts <Toaster>; in isolation we stub sonner so toast side effects don't
// interfere with asserting the create → navigate flow.
vi.mock("sonner", () => ({ toast: { success: vi.fn(), error: vi.fn() } }));

import { CampaignService } from "@/services/campaign-service";

import NewCampaignPage from "./page";

const create = vi.mocked(CampaignService.create);
const NAME = "Competency (e.g. SQL)";

describe("New campaign — competency builder + validation", () => {
  beforeEach(() => {
    create.mockClear();
    router.push.mockClear();
  });

  it("adds and removes competency rows", async () => {
    const user = userEvent.setup();
    render(<NewCampaignPage />);
    expect(screen.getAllByPlaceholderText(NAME)).toHaveLength(1);
    // A single row can't be removed (nothing to remove to).
    expect(screen.queryByRole("button", { name: /remove competency/i })).toBeNull();

    await user.click(screen.getByRole("button", { name: "Add" }));
    expect(screen.getAllByPlaceholderText(NAME)).toHaveLength(2);

    await user.click(screen.getAllByRole("button", { name: /remove competency/i })[0]);
    expect(screen.getAllByPlaceholderText(NAME)).toHaveLength(1);
  });

  it("requires at least one named competency (backend still re-validates)", async () => {
    const user = userEvent.setup();
    render(<NewCampaignPage />);
    await user.type(screen.getByPlaceholderText(/Senior Data Engineer/i), "Data Engineer");
    await user.type(screen.getByPlaceholderText(/Ships correct/i), "Senior bar");
    await user.click(screen.getByRole("button", { name: /create campaign/i }));

    expect(await screen.findByText(/add at least one competency/i)).toBeInTheDocument();
    expect(create).not.toHaveBeenCalled(); // client guard held; nothing submitted
  });

  it("submits a valid campaign and navigates to it", async () => {
    const user = userEvent.setup();
    render(<NewCampaignPage />);
    await user.type(screen.getByPlaceholderText(/Senior Data Engineer/i), "Data Engineer");
    await user.type(screen.getByPlaceholderText(/Ships correct/i), "Senior bar");
    await user.type(screen.getByPlaceholderText(NAME), "SQL");
    await user.click(screen.getByRole("button", { name: /create campaign/i }));

    await waitFor(() => expect(create).toHaveBeenCalledTimes(1));
    expect(create.mock.calls[0][0]).toMatchObject({
      role_title: "Data Engineer",
      role_profile: { bar: "Senior bar", competencies: [{ name: "SQL" }] },
    });
    await waitFor(() => expect(router.push).toHaveBeenCalledWith("/campaigns/camp-1"));
  });
});
