from pydantic import BaseModel, Field

class DriverCreate(BaseModel):
    full_name: str = Field(min_length=3, max_length=120)
    phone: str = Field(min_length=7, max_length=20)
    license_number: str = Field(min_length=5, max_length=20)
    company_id: int = Field(gt=0)

class DriverUpdate(BaseModel):
    full_name: str = Field(min_length=3, max_length=120)
    phone: str = Field(min_length=7, max_length=20)
    license_number: str = Field(min_length=5, max_length=20)
    company_id: int = Field(gt=0)

class DriverResponse(BaseModel):
    id: int
    full_name: str
    phone: str
    license_number: str
    company_id: int
    company_name: str