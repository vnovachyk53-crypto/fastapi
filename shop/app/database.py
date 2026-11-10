from typing import (
    Annotated
)

from fastapi import Depends
from sqlalchemy import (
    create_engine
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    sessionmaker
)

from app.config import settings

# Engine створюється ОДИН раз на весь застосунок.
# pool_pre_ping=True — перед використанням перевіряти, що з'єднання живе;
# pool_recycle=3600 — оновлювати з'єднання щогодини (MySQL закриває «старі»).
engine = create_engine(settings.database_url, pool_pre_ping=True, pool_recycle=3600)

# Фабрика сеансів: кожен виклик SessionLocal() дає новий сеанс роботи з БД.
SessionLocal = sessionmaker(engine)


class Base(DeclarativeBase):
    """Спільний базовий клас усіх моделей (таблиць)."""


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]
