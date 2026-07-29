// Handwritten DTOs mirroring the backend (app/modules/campaigns/schemas.py).
// These describe wire shapes only — the backend remains the source of truth for
// lifecycle rules and validation; the UI never re-implements them.

export type CampaignStatus = "draft" | "active" | "concluded";

export interface Competency {
  name: string;
  description?: string | null;
}

export interface RoleProfile {
  competencies: Competency[];
  bar: string;
}

export interface CreateCampaignRequest {
  role_title: string;
  role_profile: RoleProfile;
}

/** Full detail — GET /campaigns/{id}, plus create/activate responses. */
export interface Campaign {
  id: string;
  role_title: string;
  role_profile: RoleProfile;
  status: CampaignStatus;
  created_at: string;
}

/** A row in the list — deliberately lighter than the detail (no role_profile). */
export interface CampaignSummary {
  id: string;
  role_title: string;
  status: CampaignStatus;
  created_at: string;
}

export interface CampaignListResponse {
  items: CampaignSummary[];
  total: number;
  limit: number;
  offset: number;
}
