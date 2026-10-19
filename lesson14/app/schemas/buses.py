from pydantic import BaseModel, Field

class BusCreate(BaseModel):
    plate_number: str = Field(min_length=4, max_length=15)
    model: str = Field(min_length=2, max_length=80)
    seats: int = Field(ge=10, le=120)
    company_id: int = Field(gt=0)

class BusResponse(BaseModel):
    id: int
    plate_number: str
    model: str
    seats: int
    company_id: int
    company_name: str