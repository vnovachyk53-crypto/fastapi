from typing import Optional, List
from datetime import datetime
from car import Car, CarCreate, CarUpdate
from schemas import CarBase
import uuid
from typing import List
from fastapi import FastAPI, HTTPException


app = FastAPI()

cars_db: List[Car] = []


@app.post("/cars", response_model=Car)
def create_car(car_data: CarCreate):
    new_car = Car(
        car_id=str(len(cars_db) + 1),
        **car_data.model_dump()
    )
    cars_db.append(new_car)
    return new_car


@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/cars")
def get_cars():
    return cars_db

@app.post("/cars/", response_model=Car)
def create_car(car: CarCreate):
    car_id = str(uuid.uuid4())

    # Створюємо об'єкт Pydantic
    new_car = Car(
        car_id=car_id,
        brand_model=car.brand_model,
        manufacturer_name=car.manufacturer_name,
        vin=car.vin,
        body_type=car.body_type,
        engine_volume_or_power=car.engine_volume_or_power,
        price=car.price,
        expert_rating=None,
        is_available=car.is_available,
        short_description=car.short_description,
        year_of_manufacture=car.year_of_manufacture,
        date_added=car.date_added or str(datetime.now()),
        additional_options=car.additional_options
    )
    cars_db.append(new_car)
    return new_car


@app.get("/cars/", response_model=List[Car])
def read_cars(
        brand: Optional[str] = None,
        fuel_type: Optional[str] = None,
        min_year: Optional[int] = None,
        page: int = 1,
        items_per_page: int = 10
):
    filtered_cars = cars_db
    if brand:
        filtered_cars = [c for c in filtered_cars if c.brand_model == brand]
    if fuel_type:
        filtered_cars = [
            c for c in filtered_cars
            if c.additional_options and fuel_type in c.additional_options
        ]
    if min_year:
        filtered_cars = [c for c in filtered_cars if c.year_of_manufacture >= min_year]

    start = (page - 1) * items_per_page
    end = start + items_per_page
    return filtered_cars[start:end]


@app.get("/cars/{car_id}", response_model=Car)
def read_car(car_id: str):
    for car in cars_db:
        if car.car_id == car_id:
            return car
    raise HTTPException(status_code=404, detail="Car not found")


@app.put("/cars/{car_id}", response_model=Car)
def update_car(car_id: str, car_update: CarUpdate):
    for i, existing_car in enumerate(cars_db):
        if existing_car.car_id == car_id:
            # Оновлюємо лише передані поля
            update_data = car_update.model_dump(exclude_unset=True)
            updated_car_data = existing_car.model_dump()
            updated_car_data.update(update_data)

            cars_db[i] = Car(**updated_car_data)
            return cars_db[i]

    raise HTTPException(status_code=404, detail="Car not found")


@app.delete("/cars/{car_id}")
def delete_car(car_id: str):
    for i, existing_car in enumerate(cars_db):
        if existing_car.car_id == car_id:
            del cars_db[i]
            return {"detail": "Car deleted"}
    raise HTTPException(status_code=404, detail="Car not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
