from typing import Annotated
from fastapi import APIRouter, Query, status
from app.database import Conn
from app.schemas.drivers import DriverCreate, DriverResponse, DriverUpdate
from app.services import drivers as service

router = APIRouter(prefix="/drivers", tags=["Водії"])

@router.get("", response_model=list[DriverResponse])
def list_drivers(
    conn: Conn,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    return service.list_drivers(conn, limit, offset)

@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(driver_id: int, conn: Conn):
    return service.get_driver(conn, driver_id)

@router.post("", response_model=DriverResponse, status_code=status.HTTP_201_CREATED)
def create_driver(data: DriverCreate, conn: Conn):
    return service.create_driver(conn, data)

@router.put("/{driver_id}", response_model=DriverResponse)
def update_driver(driver_id: int, data: DriverUpdate, conn: Conn):
    return service.update_driver(conn, driver_id, data)

@router.delete("/{driver_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_driver(driver_id: int, conn: Conn):
    service.delete_driver(conn, driver_id)