// Candidate-facing DTOs (app/modules/responses/schemas.py) — no recruiter-only fields.

export interface CandidateTask {
  task_id: string;
  order: number;
  prompt: string;
  instructions: string | null;
  expected_effort_minutes: number | null;
  response_text: string;
}

export interface CandidateWorkSample {
  organization_name: string;
  role_title: string;
  title: string;
  introduction: string | null;
  estimated_minutes: number;
  tasks: CandidateTask[];
  submitted: boolean;
  submitted_at: string | null;
}

export interface SavedResponse {
  task_id: string;
  updated_at: string;
}

export interface SubmissionResult {
  organization_name: string;
  role_title: string;
  submitted_at: string;
  evidence_count: number;
}
