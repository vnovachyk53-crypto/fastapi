from pydantic import BaseModel, Field

class AssignmentCreate(BaseModel):
    driver_id: int = Field(gt=0)
    route_id: int = Field(gt=0)

class AssignmentResponse(BaseModel):
    driver_id: int
    route_id: int

class DriverRouteResponse(BaseModel):
    route_id: int
    number: str
    title: str
    distance_km: int