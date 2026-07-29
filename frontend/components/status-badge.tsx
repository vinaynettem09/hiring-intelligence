import { Badge, type BadgeProps } from "@/components/ui/badge";
import type { CampaignStatus } from "@/types/campaign";

// Maps a campaign's lifecycle state to a badge tone. Visual only — the backend
// owns what each status means and when it may change.
const VARIANT: Record<CampaignStatus, NonNullable<BadgeProps["variant"]>> = {
  draft: "warning",
  active: "success",
  concluded: "neutral",
};

export function StatusBadge({ status }: { status: CampaignStatus }) {
  return <Badge variant={VARIANT[status]}>{status}</Badge>;
}
