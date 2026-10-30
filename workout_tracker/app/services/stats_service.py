"""Aggregate queries; all user-specific reports are scoped by owner_id."""

from sqlalchemy import case, desc, func, select
from sqlalchemy.orm import Session

from app.models import User, Workout
from app.schemas_stats import GroupBy, Metric


# Allowlist: user input selects a known SQLAlchemy expression, never an attribute name.
MONTH_EXPR = func.date_format(Workout.done_on, "%Y-%m")
GROUP_COLUMNS = {
    GroupBy.kind: Workout.kind,
    GroupBy.month: MONTH_EXPR,
}

# The dictionary contains ready-to-use expressions, not function names from the request.
METRICS = {
    Metric.count: func.count(Workout.id),
    Metric.sum_duration: func.coalesce(func.sum(Workout.duration_min), 0),
    Metric.sum_distance: func.coalesce(func.sum(Workout.distance_km), 0),
    Metric.avg_duration: func.avg(Workout.duration_min),
}


def summary(db: Session, owner_id: int):
    stmt = (
        select(
            func.count(Workout.id).label("total_workouts"),
            func.coalesce(func.sum(Workout.duration_min), 0).label("total_duration_min"),
            func.coalesce(func.sum(Workout.distance_km), 0).label("total_distance_km"),
            func.avg(Workout.duration_min).label("avg_duration_min"),
            func.min(Workout.distance_km).label("min_distance_km"),
            func.max(Workout.distance_km).label("max_distance_km"),
        )
        .where(Workout.owner_id == owner_id)
    )
    return db.execute(stmt).one()


def by_kind(db: Session, owner_id: int):
    stmt = (
        select(
            Workout.kind.label("kind"),
            func.count(Workout.id).label("workouts_count"),
            func.coalesce(func.sum(Workout.duration_min), 0).label("total_duration_min"),
            func.coalesce(func.sum(Workout.distance_km), 0).label("total_distance_km"),
        )
        .where(Workout.owner_id == owner_id)
        .group_by(Workout.kind)
        .order_by(Workout.kind)
    )
    return db.execute(stmt).all()


def by_month(db: Session, owner_id: int):
    # Keep the same SQL expression in SELECT and GROUP BY (MySQL ONLY_FULL_GROUP_BY).
    month_expr = func.date_format(Workout.done_on, "%Y-%m")
    stmt = (
        select(
            month_expr.label("month"),
            func.count(Workout.id).label("workouts_count"),
            func.coalesce(func.sum(Workout.distance_km), 0).label("total_distance_km"),
        )
        .where(Workout.owner_id == owner_id)
        .group_by(month_expr)
        .order_by(month_expr)
    )
    return db.execute(stmt).all()


def top_users(db: Session, min_workouts: int):
    """Global leaderboard: intentionally spans owners to compare users.

    The assignment defines this endpoint without owner_id and asks for users
    ranked by their workout counts. All personal statistics remain owner-scoped.
    """
    workouts_count = func.count(Workout.id)
    stmt = (
        select(
            User.id.label("user_id"),
            User.name.label("name"),
            workouts_count.label("workouts_count"),
        )
        .join(Workout, Workout.owner_id == User.id)
        .group_by(User.id, User.name)
        .having(workouts_count >= min_workouts)
        .order_by(desc("workouts_count"), User.id)
    )
    return db.execute(stmt).all()


def done_ratio(db: Session, owner_id: int):
    long_count = func.count(
        case((Workout.duration_min >= 60, Workout.id))
    )
    stmt = (
        select(
            long_count.label("long_workouts"),
            func.count(Workout.id).label("total_workouts"),
        )
        .where(Workout.owner_id == owner_id)
    )
    return db.execute(stmt).one()


def grouped(db: Session, owner_id: int, group_by: GroupBy, metric: Metric):
    group_col = GROUP_COLUMNS[group_by]
    stmt = (
        select(
            group_col.label("group"),
            METRICS[metric].label("value"),
        )
        .where(Workout.owner_id == owner_id)
        .group_by(group_col)
        .order_by(group_col)
    )
    return db.execute(stmt).all()


def running_total(db: Session, owner_id: int):
    cumulative_km = func.sum(Workout.distance_km).over(
        order_by=(Workout.done_on, Workout.id),
        rows=(None, 0),
    )
    stmt = (
        select(
            Workout.id.label("workout_id"),
            func.date_format(Workout.done_on, "%Y-%m-%d").label("done_on"),
            Workout.distance_km.label("distance_km"),
            cumulative_km.label("running_total_km"),
        )
        .where(Workout.owner_id == owner_id)
        .order_by(Workout.done_on, Workout.id)
    )
    return db.execute(stmt).all()


def rank_by_kind(db: Session, owner_id: int):
    total_duration = func.coalesce(func.sum(Workout.duration_min), 0)
    stmt = (
        select(
            Workout.kind.label("kind"),
            total_duration.label("total_duration_min"),
            func.rank()
            .over(order_by=total_duration.desc())
            .label("rank"),
        )
        .where(Workout.owner_id == owner_id)
        .group_by(Workout.kind)
        .order_by("rank", Workout.kind)
    )
    return db.execute(stmt).all()
