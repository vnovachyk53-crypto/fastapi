"""Pydantic response schemas for statistical endpoints."""

from enum import Enum

from pydantic import BaseModel, ConfigDict


class StatsRow(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class SummaryOut(StatsRow):
    total_workouts: int
    total_duration_min: int
    total_distance_km: float
    avg_duration_min: float | None
    min_distance_km: float | None
    max_distance_km: float | None


class KindStat(StatsRow):
    kind: str
    workouts_count: int
    total_duration_min: int
    total_distance_km: float


class MonthStat(StatsRow):
    month: str
    workouts_count: int
    total_distance_km: float


class TopUserStat(StatsRow):
    user_id: int
    name: str
    workouts_count: int


class DoneRatioOut(StatsRow):
    long_workouts: int
    total_workouts: int


class GroupBy(str, Enum):
    kind = "kind"
    month = "month"


class Metric(str, Enum):
    count = "count"
    sum_duration = "sum_duration"
    sum_distance = "sum_distance"
    avg_duration = "avg_duration"



class GroupStat(StatsRow):
    group: str
    value: int | float | None


class RunningTotalStat(StatsRow):
    workout_id: int
    done_on: str
    distance_km: float
    running_total_km: float


class RankStat(StatsRow):
    kind: str
    total_duration_min: int
    rank: int
