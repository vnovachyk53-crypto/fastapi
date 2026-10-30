
from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy import select

from app.database import Base, SessionLocal, engine
from app.models import User, Workout

USERS = [
    {"name": "Анна Коваль", "email": "anna@example.com"},
    {"name": "Максим Бондар", "email": "maksym@example.com"},
    {"name": "Олена Мельник", "email": "olena@example.com"},
]

# 6 workouts per user; the date offsets span at least three calendar months.
WORKOUT_TEMPLATES = [
    ("Ранкова пробіжка", "run", 45, "5.20", 84),
    ("Силове тренування", "gym", 70, "0.00", 70),
    ("Йога", "yoga", 50, "0.00", 57),
    ("Плавання", "swim", 40, "1.50", 38),
    ("Вечірня пробіжка", "run", 65, "7.30", 19),
    ("Тренування в залі", "gym", 80, "0.00", 4),
]


def main() -> None:
    Base.metadata.create_all(bind=engine)
    today = date.today()

    with SessionLocal() as db:
        users_by_email: dict[str, User] = {}
        for user_data in USERS:
            user = db.scalar(select(User).where(User.email == user_data["email"]))
            if user is None:
                user = User(**user_data)
                db.add(user)
                db.flush()
            users_by_email[user.email] = user

        db.commit()

        for index, user_data in enumerate(USERS):
            user = users_by_email[user_data["email"]]
            existing = db.scalar(
                select(Workout.id).where(Workout.owner_id == user.id).limit(1)
            )
            if existing is not None:
                continue

            for title, kind, duration, distance, days_ago in WORKOUT_TEMPLATES:
                # Shift dates slightly for each user while keeping all samples recent.
                workout_date = today - timedelta(days=max(1, days_ago - index * 2))
                db.add(
                    Workout(
                        owner_id=user.id,
                        title=title,
                        kind=kind,
                        duration_min=duration,
                        distance_km=Decimal(distance),
                        done_on=workout_date,
                    )
                )

        db.commit()

    print("Seed завершено: 3 користувачі та до 18 тренувань додано.")


if __name__ == "__main__":
    main()
