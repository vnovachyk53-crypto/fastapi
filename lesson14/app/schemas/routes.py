from pydantic import BaseModel, Field

class RouteCreate(BaseModel):
    number: str = Field(min_length=1, max_length=10)
    title: str = Field(min_length=3, max_length=120)
    distance_km: int = Field(ge=1, le=5000)

class RouteResponse(BaseModel):
    id: int
    number: str
    title: str
    distance_km: int