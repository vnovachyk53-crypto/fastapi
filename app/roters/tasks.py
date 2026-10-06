from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db

router = APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.get("/{task_id}", response_model=schemas.TaskResponse)
def get_task(task_id: int, db: Session = Depends(get_db)):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задачу не знайдено"
        )
    return task


@router.patch("/{task_id}", response_model=schemas.TaskResponse)
def update_task(
        task_id: int,
        task_update: schemas.TaskUpdate,
        db: Session = Depends(get_db)
):
    query = db.query(models.Task).filter(models.Task.id == task_id)
    task = query.first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задачу не знайдено"
        )

    update_data = task_update.model_dump(exclude_unset=True)
    query.filter(models.Task.id == task_id).update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(task)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    query = db.query(models.Task).filter(models.Task.id == task_id)
    task = query.first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Задачу не знайдено"
        )

    query.delete(synchronize_session=False)
    db.commit()

    return None