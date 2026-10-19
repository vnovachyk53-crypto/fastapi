from app.database import Connection, execute, fetch_all, fetch_one

def get_all(conn: Connection):
    return fetch_all(conn, "SELECT id, number, title, distance_km FROM routes ORDER BY number")

def get_by_id(conn: Connection, route_id: int):
    return fetch_one(conn, "SELECT id, number, title, distance_km FROM routes WHERE id = %s", (route_id,))

def create(conn: Connection, number: str, title: str, distance_km: int) -> int:
    new_id, _ = execute(
        conn,
        "INSERT INTO routes (number, title, distance_km) VALUES (%s, %s, %s)",
        (number.strip(), title.strip(), distance_km)
    )
    return new_id