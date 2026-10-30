"""Маршрути для тренувань."""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Workout
from app.schemas import WorkoutCreate, WorkoutOut

router = APIRouter(prefix="/workouts", tags=["workouts"])


@router.post("", response_model=WorkoutOut, status_code=status.HTTP_201_CREATED)
def create_workout(payload: WorkoutCreate, db: Session = Depends(get_db)):
    # Перевіряємо, що користувач існує.
    owner = db.scalar(select(User.id).where(User.id == payload.owner_id))
    if owner is None:
        raise HTTPException(status_code=404, detail="Користувача не знайдено")

    workout = Workout(
        owner_id=payload.owner_id,
        title=payload.title,
        kind=payload.kind.value,
        duration_min=payload.duration_min,
        distance_km=payload.distance_km,
        done_on=payload.done_on,
    )
    db.add(workout)
    db.commit()
    db.refresh(workout)
    return workout


@router.get("", response_model=list[WorkoutOut])
def list_workouts(
    owner_id: int = Query(..., gt=0),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0, le=100_000),
    db: Session = Depends(get_db),
):
    stmt = (
        select(Workout)
        .where(Workout.owner_id == owner_id)
        .order_by(Workout.done_on.desc(), Workout.id.desc())
        .limit(limit)
        .offset(offset)
    )
    return db.scalars(stmt).all()
