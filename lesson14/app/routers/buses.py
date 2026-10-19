from fastapi import APIRouter, status
from app.database import Conn
from app.schemas.buses import BusCreate, BusResponse
from app.services import buses as service

router = APIRouter(prefix="/buses", tags=["Автобуси"])

@router.get("", response_model=list[BusResponse])
def list_buses(conn: Conn):
    return service.list_buses(conn)

@router.get("/{bus_id}", response_model=BusResponse)
def get_bus(bus_id: int, conn: Conn):
    return service.get_bus(conn, bus_id)

@router.post("", response_model=BusResponse, status_code=status.HTTP_201_CREATED)
def create_bus(data: BusCreate, conn: Conn):
    return service.create_bus(conn, data)