from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app import models  # noqa: F401 — реєструє ORM-моделі в Base.metadata
from app.database import Base, engine
from app.routers import auth, books

Base.metadata.create_all(engine)

app = FastAPI(title="Book Store")

app.include_router(auth.router)
app.include_router(books.router)


@app.get("/api/health")
def health():
    return {"message": "Сервер працює"}


# Фронтенд розміщений у shop/frontend. Монтуємо його останнім,
# щоб він не перехоплював API-маршрути.
FRONTEND_DIR = Path(__file__).resolve().parent / "frontend"
app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")
