import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from mysql.connector import Error as MySQLError
from mysql.connector import IntegrityError, PoolError
from fastapi.staticfiles import StaticFiles
from app.config import get_settings
from app.database import create_pool
from app.routers import categories, expenses, stats

logger = logging.getLogger("expense_tracker")

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = create_pool(get_settings())
    yield

app = FastAPI(title="Expense Tracker API", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categories.router)
app.include_router(expenses.router)
app.include_router(stats.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.exception_handler(PoolError)
def pool_error_handler(request: Request, exc: PoolError):
    """Усі з'єднання пулу зайняті: просимо повторити пізніше."""
    logger.error("Pool exhausted: %s", exc)
    return JSONResponse({"detail": "Service busy, try again later"}, status_code=503)

@app.exception_handler(MySQLError)
def mysql_error_handler(request: Request, exc: MySQLError):
    """Помилки бази перетворюємо на зрозумілі відповіді БЕЗ тексту SQL і імен таблиць[cite: 23]."""
    code = getattr(exc, "errno", None) or 0
    if isinstance(exc, IntegrityError) and code == 1062:  # дублікат UNIQUE[cite: 23]
        return JSONResponse({"detail": "Such record already exists"}, status_code=409)
    if code == 1451:  # RESTRICT: категорія містить витрати[cite: 23]
        return JSONResponse(
            {"detail": "Record is in use and cannot be deleted"}, status_code=409
        )
    logger.error("MySQL error %s", code)  # подробиці лише в лог[cite: 23]
    return JSONResponse({"detail": "Internal server error"}, status_code=500)

@app.get("/")
def root():
    return {"message": "Expense Tracker API"}