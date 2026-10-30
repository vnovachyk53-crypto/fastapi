"""Маршрути статистики."""

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import schemas_stats as schemas
from app.database import get_db
from app.services import stats_service

router = APIRouter(prefix="/stats", tags=["stats"])


@router.get("/summary", response_model=schemas.SummaryOut)
def get_summary(owner_id: int = Query(..., gt=0), db: Session = Depends(get_db)):
    return stats_service.summary(db, owner_id)


@router.get("/by-kind", response_model=list[schemas.KindStat])
def get_by_kind(owner_id: int = Query(..., gt=0), db: Session = Depends(get_db)):
    return stats_service.by_kind(db, owner_id)


@router.get("/by-month", response_model=list[schemas.MonthStat])
def get_by_month(owner_id: int = Query(..., gt=0), db: Session = Depends(get_db)):
    return stats_service.by_month(db, owner_id)


@router.get("/top-users", response_model=list[schemas.TopUserStat])
def get_top_users(
    min_workouts: int = Query(3, ge=1, le=100_000),
    db: Session = Depends(get_db),
):
    return stats_service.top_users(db, min_workouts)


@router.get("/done-ratio", response_model=schemas.DoneRatioOut)
def get_done_ratio(owner_id: int = Query(..., gt=0), db: Session = Depends(get_db)):
    return stats_service.done_ratio(db, owner_id)


@router.get("/group", response_model=list[schemas.GroupStat])
def get_grouped_stats(
    group_by: schemas.GroupBy = Query(...),
    metric: schemas.Metric = Query(...),
    owner_id: int = Query(..., gt=0),
    db: Session = Depends(get_db),
):
    return stats_service.grouped(db, owner_id, group_by, metric)


# Бонусні маршрути з віконними функціями SQL.
@router.get("/running-total", response_model=list[schemas.RunningTotalStat])
def get_running_total(owner_id: int = Query(..., gt=0), db: Session = Depends(get_db)):
    return stats_service.running_total(db, owner_id)


@router.get("/rank", response_model=list[schemas.RankStat])
def get_rank(owner_id: int = Query(..., gt=0), db: Session = Depends(get_db)):
    return stats_service.rank_by_kind(db, owner_id)
