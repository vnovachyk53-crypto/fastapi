from app.database import Connection, execute, fetch_all, fetch_one

def exists(conn: Connection, driver_id: int, route_id: int) -> bool:
    row = fetch_one(conn, "SELECT 1 AS ok FROM driver_routes WHERE driver_id = %s AND route_id = %s", (driver_id, route_id))
    return row is not None

def create(conn: Connection, driver_id: int, route_id: int) -> None:
    execute(conn, "INSERT INTO driver_routes (driver_id, route_id) VALUES (%s, %s)", (driver_id, route_id))

def delete(conn: Connection, driver_id: int, route_id: int) -> bool:
    _, affected = execute(conn, "DELETE FROM driver_routes WHERE driver_id = %s AND route_id = %s", (driver_id, route_id))
    return affected > 0

def get_by_driver(conn: Connection, driver_id: int):
    return fetch_all(conn, """
        SELECT r.id AS route_id, r.number, r.title, r.distance_km
        FROM driver_routes AS dr
        JOIN routes AS r ON r.id = dr.route_id
        WHERE dr.driver_id = %s
        ORDER BY r.number
    """, (driver_id,))