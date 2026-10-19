from fastapi import APIRouter, status
from app.database import Conn
from app.schemas.companies import CompanyCreate, CompanyResponse
from app.services import companies as service

router = APIRouter(prefix="/companies", tags=["Перевізники"])

@router.get("", response_model=list[CompanyResponse])
def list_companies(conn: Conn):
    return service.list_companies(conn)

@router.get("/{company_id}", response_model=CompanyResponse)
def get_company(company_id: int, conn: Conn):
    return service.get_company(conn, company_id)

@router.post("", response_model=CompanyResponse, status_code=status.HTTP_201_CREATED)
def create_company(data: CompanyCreate, conn: Conn):
    return service.create_company(conn, data)