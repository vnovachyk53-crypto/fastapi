from sqlalchemy.orm import Session
from app.models import Task
from app.schemas import TaskCreate, TaskUpdate


def create_task(session: Session, project_id: int, payload: TaskCreate) -> Task:
    task = Task(**payload.model_dump(), project_id=project_id)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


def get_task(session: Session, task_id: int) -> Task | None:
    return session.get(Task, task_id)


def update_task(session: Session, task: Task, payload: TaskUpdate) -> Task:
    changes = payload.model_dump(exclude_unset=True)
    for field, value in changes.items():
        setattr(task, field, value)
    session.commit()
    session.refresh(task)
    return task


def delete_task(session: Session, task) -> None:
    session.delete(task)
    session.commit()
