// Mirrors app/modules/invitations/schemas.py.

/** Candidate-facing view — only what the candidate may see. No internal IDs. */
export interface CandidateInvitationView {
  candidate_name: string;
  organization_name: string;
  role_title: string;
  next_step: "consent";
  expires_at: string;
}

/** Recruiter-facing result of issuing an invitation (never contains the token). */
export interface InvitationSummary {
  id: string;
  candidate: { id: string; name: string; email: string };
  expires_at: string;
  created_at: string;
  replaced_previous: boolean;
}
