"""Work-sample DTOs. The write side is a single business operation — *define the whole
work sample* — rather than granular question CRUD. The read side adds derived coverage
so the recruiter can see whether every competency actually has a task."""

from pydantic import BaseModel, Field

from app.modules.worksample.enums import TaskType


class WorkSampleTaskInput(BaseModel):
    prompt: str = Field(min_length=1, max_length=4000)
    instructions: str | None = Field(default=None, max_length=4000)
    evidence_intent: str = Field(min_length=1, max_length=2000)
    task_type: TaskType = TaskType.TEXT_RESPONSE
    competencies: list[str] = Field(min_length=1, max_length=20)
    expected_effort_minutes: int | None = Field(default=None, ge=1, le=480)


class DefineWorkSampleRequest(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    introduction: str | None = Field(default=None, max_length=4000)
    tasks: list[WorkSampleTaskInput] = Field(max_length=50)


class WorkSampleTaskResponse(BaseModel):
    id: str
    prompt: str
    instructions: str | None
    evidence_intent: str
    task_type: TaskType
    competencies: list[str]
    display_order: int
    expected_effort_minutes: int | None


class CompetencyCoverage(BaseModel):
    """Which campaign competencies a task actually covers — real product intelligence."""

    total: int
    covered: list[str]
    uncovered: list[str]


class WorkSampleResponse(BaseModel):
    exists: bool  # false until first defined
    editable: bool  # true only while the campaign is a draft
    campaign_id: str
    role_title: str
    title: str
    introduction: str | None
    tasks: list[WorkSampleTaskResponse]
    estimated_minutes: int  # summed from tasks
    coverage: CompetencyCoverage
