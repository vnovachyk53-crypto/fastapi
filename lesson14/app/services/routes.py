from app.database import Connection
from app.exceptions import NotFoundError
from app.repositories import routes as repo
from app.schemas.routes import RouteCreate

def list_routes(conn: Connection):
    return repo.get_all(conn)

def get_route(conn: Connection, route_id: int):
    route = repo.get_by_id(conn, route_id)
    if route is None:
        raise NotFoundError("Маршрут не знайдено")
    return route

def create_route(conn: Connection, data: RouteCreate):
    new_id = repo.create(conn, data.number, data.title, data.distance_km)
    conn.commit()
    return get_route(conn, new_id)