from fastapi import APIRouter, status
from app.database import Conn
from app.schemas.assignments import AssignmentCreate, AssignmentResponse, DriverRouteResponse
from app.services import assignments as service

router = APIRouter(tags=["Допуски"])

@router.post("/assignments", response_model=AssignmentResponse, status_code=status.HTTP_201_CREATED)
def assign(data: AssignmentCreate, conn: Conn):
    return service.assign(conn, data)

@router.get("/drivers/{driver_id}/routes", response_model=list[DriverRouteResponse])
def driver_routes(driver_id: int, conn: Conn):
    return service.list_driver_routes(conn, driver_id)

@router.delete("/assignments/{driver_id}/{route_id}", status_code=status.HTTP_204_NO_CONTENT)
def unassign(driver_id: int, route_id: int, conn: Conn):
    service.unassign(conn, driver_id, route_id)