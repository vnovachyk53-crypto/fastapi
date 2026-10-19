from app.database import Connection, execute, fetch_all, fetch_one

SELECT_WITH_COMPANY = """
    SELECT b.id, b.plate_number, b.model, b.seats, b.company_id, c.name AS company_name
    FROM buses AS b
    JOIN companies AS c ON c.id = b.company_id
"""

def get_all(conn: Connection):
    return fetch_all(conn, SELECT_WITH_COMPANY + " ORDER BY b.plate_number")

def get_by_id(conn: Connection, bus_id: int):
    return fetch_one(conn, SELECT_WITH_COMPANY + " WHERE b.id = %s", (bus_id,))

def create(conn: Connection, plate_number: str, model: str, seats: int, company_id: int) -> int:
    new_id, _ = execute(
        conn,
        "INSERT INTO buses (plate_number, model, seats, company_id) VALUES (%s, %s, %s, %s)",
        (plate_number.strip(), model.strip(), seats, company_id)
    )
    return new_id