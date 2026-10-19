from app.database import Connection
from app.exceptions import NotFoundError
from app.repositories import buses as repo
from app.schemas.buses import BusCreate
from app.services import companies as company_service

def list_buses(conn: Connection):
    return repo.get_all(conn)

def get_bus(conn: Connection, bus_id: int):
    bus = repo.get_by_id(conn, bus_id)
    if bus is None:
        raise NotFoundError("Автобус не знайдено")
    return bus

def create_bus(conn: Connection, data: BusCreate):
    company_service.get_company(conn, data.company_id) # BR-B1
    new_id = repo.create(conn, data.plate_number, data.model, data.seats, data.company_id)
    conn.commit()
    return get_bus(conn, new_id)