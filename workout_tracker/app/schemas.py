"""Pydantic v2 input and output schemas."""

from datetime import date
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class WorkoutKind(str, Enum):
    run = "run"
    gym = "gym"
    yoga = "yoga"
    swim = "swim"


class InputSchema(BaseModel):
    model_config = ConfigDict(extra="forbid")


class UserCreate(InputSchema):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr


class WorkoutCreate(InputSchema):
    owner_id: int = Field(gt=0)
    title: str = Field(min_length=1, max_length=100)
    kind: WorkoutKind
    duration_min: int = Field(gt=0)
    distance_km: Decimal = Field(ge=0, max_digits=6, decimal_places=2)
    done_on: date


class WorkoutOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    owner_id: int
    title: str
    kind: WorkoutKind
    duration_min: int
    distance_km: float
    done_on: date
