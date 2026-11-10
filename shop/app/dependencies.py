"""
dependencies.py — спільні залежності FastAPI (Depends).

Головна: get_current_user — відповідає на питання «хто робить цей запит?».
Захистити маршрут = додати в нього параметр `user: CurrentUser`.
"""

from typing import Annotated  # Annotated — тип + додаткова інформація (Cookie, Depends)

from fastapi import (
    Cookie,  # Cookie — дістає значення cookie із запиту
    Depends,  # Depends — оголошення залежності
    HTTPException  # HTTPException — відповідь з кодом помилки
)

from app import session_store  # сховище сесій
from app.config import settings  # налаштування (ім'я cookie тощо)
from app.database import (
    DbSession  # сеанс БД (скорочення Annotated[Session, Depends(get_db)])
)
from app.models import User  # модель користувача (для типу результату)
from app.services import user_service  # пошук користувача в базі


def get_current_user(
    db: DbSession,
    # FastAPI сам візьме cookie з іменем session_id (ім'я параметра = ім'я cookie,
    # див. settings.cookie_name). Якщо cookie немає — буде None.
    session_id: Annotated[str | None, Cookie()] = None
) -> User:
    """Повертає поточного користувача або піднімає 401."""
    user_id = session_store.get_user_id(session_id)
    user = user_service.get_by_id(db, user_id) if user_id else None
    if user is None:
        # 401 = «не автентифіковано»: немає чинної сесії.
        raise HTTPException(status_code=401, detail="Не автентифіковано")
    return user


# Скорочення: у маршруті пишемо `user: CurrentUser` — і маршрут захищено.
CurrentUser = Annotated[User, Depends(get_current_user)]

# Підказка: параметр get_current_user має називатися session_id, бо таке ім'я cookie.
assert settings.cookie_name == "session_id"
