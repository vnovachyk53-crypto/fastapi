from typing import Optional, List
from pydantic import BaseModel

class Car(BaseModel):
    car_id: str
    brand_model: str
    manufacturer_name: str
    vin: str
    body_type: str
    engine_volume_or_power: float
    price: float
    expert_rating: Optional[float] = None
    is_available: bool
    short_description: str
    year_of_manufacture: int
    date_added: str
    additional_options: Optional[List[str]] = None

class CarCreate(BaseModel):
    brand_model: str
    manufacturer_name: str
    vin: str
    body_type: str
    engine_volume_or_power: float
    price: float
    is_available: bool
    short_description: str
    year_of_manufacture: int
    date_added: Optional[str] = None
    additional_options: Optional[List[str]] = None

class CarUpdate(BaseModel):
    brand_model: Optional[str] = None
    manufacturer_name: Optional[str] = None
    vin: Optional[str] = None
    body_type: Optional[str] = None
    engine_volume_or_power: Optional[float] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None
    short_description: Optional[str] = None
    year_of_manufacture: Optional[int] = None
    date_added: Optional[str] = None
    additional_options: Optional[List[str]] = None