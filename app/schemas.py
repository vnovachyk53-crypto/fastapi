from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models import Priority


class TaskBase(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    description: str | None = None
    priority: Priority = Priority.medium
    due_date: date | None = None


class TaskCreate(TaskBase):
    pass


class TaskUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None
    priority: Priority | None = None
    due_date: date | None = None
    is_done: bool | None = None


class TaskResponse(TaskBase):
    id: int
    is_done: bool
    created_at: datetime
    project_id: int

    model_config = ConfigDict(from_attributes=True)


# ========================
class ProjectBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    description: str | None = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = None


class ProjectResponse(ProjectBase):
    id: int
    created_at: datetime
    tasks: list[TaskResponse] = []

    model_config = ConfigDict(from_attributes=True)
