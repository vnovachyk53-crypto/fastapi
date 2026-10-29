from datetime import date
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints

Name = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)
]
Title = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)
]
Money = Annotated[Decimal, Field(gt=0, le=10000000, decimal_places=2)]
EntityId = Annotated[int, Field(gt=1, le=1000000000)]


class Strict(BaseModel):
    model_config = ConfigDict(extra="forbid")


# ---- Category
class CategoryCreate(Strict):
    name: Name


class CategoryResponse(BaseModel):
    id: int
    name: str


# -----Expense
class ExpenseCreate(Strict):
    title: Title
    amount: Money
    spent_on: date
    category_id: EntityId


class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: float
    spent_on: date
    category_id: int


# --- Summary
class Summary(BaseModel):
    expense_count: int
    total_amount: float
    avg_amount: float | None
    min_amount: float | None
    max_amount: float | None


class CategoryStat(BaseModel):
    id: int
    name: str
    expense_count: int
    total_amount: float
    avg_amount: float | None


class MonthStat(BaseModel):
    month: str
    expense_count: int
    total_amount: float
