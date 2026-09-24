from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.database import engine
from app.models import Base
from app.routers import movies


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Movie Manager API", lifespan=lifespan)

app.include_router(movies.router)


@app.get("/health")
async def health():
    return {"ok": True}