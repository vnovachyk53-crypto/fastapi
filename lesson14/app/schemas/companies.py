from pydantic import BaseModel, Field

class CompanyCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    phone: str = Field(min_length=7, max_length=20)

class CompanyResponse(BaseModel):
    id: int
    name: str
    phone: str