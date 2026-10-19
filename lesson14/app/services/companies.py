from app.database import Connection
from app.exceptions import NotFoundError
from app.repositories import companies as repo
from app.schemas.companies import CompanyCreate

def list_companies(conn: Connection):
    return repo.get_all(conn)

def get_company(conn: Connection, company_id: int):
    company = repo.get_by_id(conn, company_id)
    if company is None:
        raise NotFoundError("Перевізника не знайдено")
    return company

def create_company(conn: Connection, data: CompanyCreate):
    new_id = repo.create(conn, data.name, data.phone)
    conn.commit()
    return get_company(conn, new_id)