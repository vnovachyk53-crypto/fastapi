from pydantic import BaseModel
from typing import List, Optional

class CarBase(BaseModel):
    brand_model: str
    manufacturer_name: str
    vin: str
    body_type: str
    engine_volume_or_power: float
    price: float
    is_available: bool
    short_description: str
    year_of_manufacture: int
    date_added: str
    additional_options: Optional[List[str]] = []

class CarCreate(CarBase):
    pass

class CarUpdate(CarBase):
    pass