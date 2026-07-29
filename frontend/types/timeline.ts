// Handwritten DTOs mirroring app/modules/timeline/schemas.py.
// A coherent, chronological audit trail assembled from authoritative records.

export type TimelineEventKind =
  | "INVITATION_SENT"
  | "INVITATION_OPENED"
  | "CONSENT_GRANTED"
  | "CONSENT_WITHDRAWN"
  | "WORK_SAMPLE_SUBMITTED"
  | "EVALUATION_GENERATED"
  | "DECISION_RECORDED";

export interface TimelineEntry {
  kind: TimelineEventKind;
  at: string;
  actor_type: string; // "recruiter" | "candidate" | "system"
  actor: string | null;
  summary: string;
}

export interface HiringTimelineResponse {
  candidate_evaluation_id: string;
  candidate_name: string;
  candidate_email: string;
  role_title: string;
  entries: TimelineEntry[]; // chronological, oldest first
}
