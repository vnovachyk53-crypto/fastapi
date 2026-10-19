from app.database import Connection
from app.exceptions import NotFoundError
from app.repositories import drivers as repo
from app.schemas.drivers import DriverCreate, DriverUpdate
from app.services import companies as company_service

def list_drivers(conn: Connection, limit: int, offset: int):
    return repo.get_all(conn, limit, offset)

def get_driver(conn: Connection, driver_id: int):
    driver = repo.get_by_id(conn, driver_id)
    if driver is None:
        raise NotFoundError("Водія не знайдено")
    return driver

def create_driver(conn: Connection, data: DriverCreate):
    company_service.get_company(conn, data.company_id) # BR-D1
    new_id = repo.create(conn, data.full_name, data.phone, data.license_number, data.company_id)
    conn.commit()
    return get_driver(conn, new_id)

def update_driver(conn: Connection, driver_id: int, data: DriverUpdate):
    get_driver(conn, driver_id)
    company_service.get_company(conn, data.company_id) # BR-D1
    repo.update(conn, driver_id, data.full_name, data.phone, data.license_number, data.company_id)
    conn.commit()
    return get_driver(conn, driver_id)

def delete_driver(conn: Connection, driver_id: int) -> None:
    if not repo.delete(conn, driver_id):
        raise NotFoundError("Водія не знайдено")
    conn.commit()