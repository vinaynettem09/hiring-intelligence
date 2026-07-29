import { AppShell } from "@/components/layout/app-shell";

// The single authenticated recruiter shell. Route group `(recruiter)` does not affect URLs
// (/dashboard, /campaigns/*, /review-queue stay as-is) but mounts AppShell — and its
// identity (/me) fetch + sidebar state — ONCE across all recruiter routes, instead of
// remounting when moving between Dashboard, Campaigns and Review Queue. Auth (`(auth)`) and
// candidate (`/invite`) remain separate trust/experience boundaries with their own shells.
export default function RecruiterLayout({ children }: { children: React.ReactNode }) {
  return <AppShell>{children}</AppShell>;
}
