from app.database import Connection
from app.exceptions import ConflictError, NotFoundError
from app.repositories import assignments as repo
from app.schemas.assignments import AssignmentCreate
from app.services import drivers as driver_service
from app.services import routes as route_service

def assign(conn: Connection, data: AssignmentCreate):
    driver_service.get_driver(conn, data.driver_id) # BR-A1
    route_service.get_route(conn, data.route_id)   # BR-A1
    if repo.exists(conn, data.driver_id, data.route_id):
        raise ConflictError("Водій уже має допуск до цього маршруту") # BR-A2
    repo.create(conn, data.driver_id, data.route_id)
    conn.commit()
    return {"driver_id": data.driver_id, "route_id": data.route_id}

def list_driver_routes(conn: Connection, driver_id: int):
    driver_service.get_driver(conn, driver_id)
    return repo.get_by_driver(conn, driver_id)

def unassign(conn: Connection, driver_id: int, route_id: int) -> None:
    if not repo.delete(conn, driver_id, route_id):
        raise NotFoundError("Допуск не знайдено") # BR-A3
    conn.commit()