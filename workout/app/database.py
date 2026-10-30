"""Підключення до MySQL та створення сесій."""

import os
from collections.abc import Generator

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

load_dotenv()


class Base(DeclarativeBase):
    pass


# URL.create коректно обробляє пароль, навіть якщо в ньому є спеціальні символи.
DATABASE_URL = URL.create(
    "mysql+pymysql",
    username=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    host=os.getenv("DB_HOST", "127.0.0.1"),
    port=int(os.getenv("DB_PORT", "3306")),
    database=os.getenv("DB_NAME", "workout_tracker"),
    query={"charset": "utf8mb4"},
)

engine = create_engine(
    DATABASE_URL,
    echo=False,
    hide_parameters=True,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
