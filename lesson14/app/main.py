from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from mysql.connector import errors

from app.config import get_settings
from app.database import create_pool, Conn, fetch_all, fetch_one
from app.exceptions import ConflictError, NotFoundError
from app.routers import companies, buses, routes, drivers, assignments

logger = logging.getLogger("uvicorn.error")


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.pool = create_pool(get_settings())
    yield


app = FastAPI(title="Bus Fleet API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(companies.router)
app.include_router(buses.router)
app.include_router(routes.router)
app.include_router(drivers.router)
app.include_router(assignments.router)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def root():
    return FileResponse("static/index.html")


@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(ConflictError)
async def conflict_handler(request: Request, exc: ConflictError):
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(errors.IntegrityError)
async def integrity_handler(request: Request, exc: errors.IntegrityError):
    logger.warning("Database integrity error on %s %s: %s", request.method, request.url.path, exc)
    return JSONResponse(
        status_code=409,
        content={
            "detail": "Порушено цілісність даних",
            "database_error": str(exc),
            "errno": getattr(exc, "errno", None),
            "sqlstate": getattr(exc, "sqlstate", None),
        },
    )


@app.exception_handler(errors.Error)
async def database_error_handler(request: Request, exc: errors.Error):
    logger.exception("MySQL error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Помилка бази даних",
            "database_error": str(exc),
            "errno": getattr(exc, "errno", None),
            "sqlstate": getattr(exc, "sqlstate", None),
        },
    )


@app.exception_handler(Exception)
async def unexpected_error_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s", request.method, request.url.path)
    return JSONResponse(
        status_code=500,
        content={"detail": "Внутрішня помилка сервера", "error": str(exc)},
    )


@app.get("/diagnostics/database", tags=["Службові"])
def diagnose_database(conn: Conn):
    """Read-only checks for tables and columns used by the API."""
    current = fetch_one(conn, "SELECT DATABASE() AS database_name")
    checks = {
        "companies": "SELECT id, name, phone FROM companies LIMIT 0",
        "buses": (
            "SELECT b.id, b.plate_number, b.model, b.seats, b.company_id, "
            "c.name AS company_name FROM buses b "
            "JOIN companies c ON c.id = b.company_id LIMIT 0"
        ),
        "routes": "SELECT id, number, title, distance_km FROM routes LIMIT 0",
        "drivers": (
            "SELECT d.id, d.full_name, d.phone, d.license_number, d.company_id, "
            "c.name AS company_name FROM drivers d "
            "JOIN companies c ON c.id = d.company_id LIMIT 0"
        ),
        "driver_routes": (
            "SELECT r.id AS route_id, r.number, r.title, r.distance_km "
            "FROM driver_routes dr JOIN routes r ON r.id = dr.route_id "
            "JOIN drivers d ON d.id = dr.driver_id LIMIT 0"
        ),
    }
    results = {}
    for table, sql in checks.items():
        try:
            fetch_all(conn, sql)
            results[table] = {"ok": True}
        except errors.Error as exc:
            results[table] = {
                "ok": False,
                "error": str(exc),
                "errno": getattr(exc, "errno", None),
                "sqlstate": getattr(exc, "sqlstate", None),
            }
    return {
        "database": current["database_name"] if current else None,
        "checks": results,
        "all_ok": all(item["ok"] for item in results.values()),
    }


@app.get("/health", tags=["Службові"])
def health():
    return {"status": "ok"}
