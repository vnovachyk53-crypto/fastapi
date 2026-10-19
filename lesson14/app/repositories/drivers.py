from app.database import Connection, execute, fetch_all, fetch_one

SELECT_WITH_COMPANY = """
    SELECT d.id, d.full_name, d.phone, d.license_number, d.company_id, c.name AS company_name
    FROM drivers AS d
    JOIN companies AS c ON c.id = d.company_id
"""

def get_all(conn: Connection, limit: int, offset: int):
    return fetch_all(conn, SELECT_WITH_COMPANY + " ORDER BY d.full_name LIMIT %s OFFSET %s", (limit, offset))

def get_by_id(conn: Connection, driver_id: int):
    return fetch_one(conn, SELECT_WITH_COMPANY + " WHERE d.id = %s", (driver_id,))

def create(conn: Connection, full_name: str, phone: str, license_number: str, company_id: int) -> int:
    new_id, _ = execute(
        conn,
        "INSERT INTO drivers (full_name, phone, license_number, company_id) VALUES (%s, %s, %s, %s)",
        (full_name.strip(), phone.strip(), license_number.strip(), company_id)
    )
    return new_id

def update(conn: Connection, driver_id: int, full_name: str, phone: str, license_number: str, company_id: int) -> None:
    execute(
        conn,
        "UPDATE drivers SET full_name = %s, phone = %s, license_number = %s, company_id = %s WHERE id = %s",
        (full_name.strip(), phone.strip(), license_number.strip(), company_id, driver_id)
    )

def delete(conn: Connection, driver_id: int) -> bool:
    _, affected = execute(conn, "DELETE FROM drivers WHERE id = %s", (driver_id,))
    return affected > 0