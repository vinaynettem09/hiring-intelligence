// Mirrors app/modules/dashboard/schemas.py — a purpose-built read model. All fields
// are real, derived from existing data (no AI/velocity/confidence).

import type { CampaignStatus } from "@/types/campaign";

export interface DashboardMetrics {
  total_campaigns: number;
  active_campaigns: number;
  draft_campaigns: number;
  total_candidates: number;
  candidates_missing_resume: number;
}

export interface DashboardAttention {
  draft_campaigns: number;
  active_campaigns_without_candidates: number;
  candidates_missing_resume: number;
}

export interface DashboardCampaign {
  id: string;
  role_title: string;
  status: CampaignStatus;
  created_at: string;
}

export interface DashboardCandidate {
  evaluation_id: string;
  name: string;
  email: string;
  campaign_id: string;
  campaign_role_title: string;
  created_at: string;
}

export interface DashboardResponse {
  metrics: DashboardMetrics;
  attention: DashboardAttention;
  recent_campaigns: DashboardCampaign[];
  recent_candidates: DashboardCandidate[];
}
