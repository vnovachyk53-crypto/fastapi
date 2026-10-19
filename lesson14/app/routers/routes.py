from fastapi import APIRouter, status
from app.database import Conn
from app.schemas.routes import RouteCreate, RouteResponse
from app.services import routes as service

router = APIRouter(prefix="/routes", tags=["Маршрути"])

@router.get("", response_model=list[RouteResponse])
def list_routes(conn: Conn):
    return service.list_routes(conn)

@router.post("", response_model=RouteResponse, status_code=status.HTTP_201_CREATED)
def create_route(data: RouteCreate, conn: Conn):
    return service.create_route(conn, data)