"""Головний файл FastAPI."""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.database import Base, engine
from app import models  # noqa: F401 - реєструє моделі перед створенням таблиць
from app.routers import stats, users, workouts

app = FastAPI(
    title="Workout Tracker API",
    description="Облік тренувань та статистика на SQLAlchemy ORM і MySQL 8.",
    version="1.0.0",
)


@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)


app.include_router(users.router)
app.include_router(workouts.router)
app.include_router(stats.router)


@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok", "docs": "/docs"}


@app.exception_handler(IntegrityError)
async def handle_integrity_error(request: Request, exc: IntegrityError):
    # Не повертаємо клієнту текст помилки MySQL або SQL-запиту.
    return JSONResponse(
        status_code=409,
        content={"detail": "Порушено обмеження цілісності даних"},
    )


@app.exception_handler(SQLAlchemyError)
async def handle_database_error(request: Request, exc: SQLAlchemyError):
    # Внутрішні подробиці помилки залишаються на сервері.
    return JSONResponse(
        status_code=500,
        content={"detail": "Внутрішня помилка бази даних"},
    )
