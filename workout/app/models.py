"""ORM-моделі таблиць users та workouts."""

from datetime import date
from decimal import Decimal

from sqlalchemy import (
    CheckConstraint,
    Date,
    ForeignKey,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email", name="uq_users_email"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)


class Workout(Base):
    __tablename__ = "workouts"
    __table_args__ = (
        CheckConstraint("duration_min > 0", name="ck_workouts_duration_positive"),
        CheckConstraint("distance_km >= 0", name="ck_workouts_distance_nonnegative"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", name="fk_workouts_owner", ondelete="RESTRICT"),
        nullable=False,
        index=True,
    )
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    kind: Mapped[str] = mapped_column(String(30), nullable=False)
    duration_min: Mapped[int] = mapped_column(Integer, nullable=False)
    distance_km: Mapped[Decimal] = mapped_column(
        Numeric(6, 2), nullable=False, default=Decimal("0.00")
    )
    done_on: Mapped[date] = mapped_column(Date, nullable=False, index=True)
