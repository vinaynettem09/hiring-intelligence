// Mirrors app/modules/worksample/schemas.py.

export type TaskType = "text_response";

export interface WorkSampleTask {
  id: string;
  prompt: string;
  instructions: string | null;
  evidence_intent: string;
  task_type: TaskType;
  competencies: string[];
  display_order: number;
  expected_effort_minutes: number | null;
}

export interface CompetencyCoverage {
  total: number;
  covered: string[];
  uncovered: string[];
}

export interface WorkSample {
  exists: boolean;
  editable: boolean; // true only while the campaign is a draft
  campaign_id: string;
  role_title: string;
  title: string;
  introduction: string | null;
  tasks: WorkSampleTask[];
  estimated_minutes: number;
  coverage: CompetencyCoverage;
}

export interface TaskInput {
  prompt: string;
  instructions?: string | null;
  evidence_intent: string;
  task_type?: TaskType;
  competencies: string[];
  expected_effort_minutes?: number | null;
}

export interface DefineWorkSampleRequest {
  title: string;
  introduction?: string | null;
  tasks: TaskInput[];
}
