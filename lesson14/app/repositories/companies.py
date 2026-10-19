from app.database import Connection, execute, fetch_all, fetch_one

def get_all(conn: Connection):
    return fetch_all(conn, "SELECT id, name, phone FROM companies ORDER BY name")

def get_by_id(conn: Connection, company_id: int):
    return fetch_one(conn, "SELECT id, name, phone FROM companies WHERE id = %s", (company_id,))

def create(conn: Connection, name: str, phone: str) -> int:
    new_id, _ = execute(conn, "INSERT INTO companies (name, phone) VALUES (%s, %s)", (name.strip(), phone.strip()))
    return new_id