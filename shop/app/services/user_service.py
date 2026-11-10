"""
services/user_service.py — бізнес-логіка роботи з користувачами.

Сервіс не знає про HTTP (cookie, коди відповідей): він лише працює з базою.
Так логіку легко перевіряти й повторно використовувати.
"""

from sqlalchemy import select  # select — побудова SQL-запиту SELECT
from sqlalchemy.orm import Session  # Session — тип сеансу БД (для анотацій)

from app.models import User  # модель таблиці users
from app.security import (
    hash_password,  # хешування пароля при реєстрації
    verify_password,  # перевірка пароля при вході
)


def get_by_username(db: Session, username: str) -> User | None:
    """Знайти користувача за логіном (або None)."""
    return db.scalar(select(User).where(User.username == username))


def get_by_id(db: Session, user_id: int) -> User | None:
    """Знайти користувача за первинним ключем (або None)."""
    return db.get(User, user_id)


def create_user(db: Session, username: str, password: str) -> User:
    """Створити користувача; у базу потрапляє лише хеш пароля."""
    user = User(username=username, password_hash=hash_password(password))
    db.add(user)
    db.commit()  # commit — явно, бо код після yield у get_db виконується пізно
    return user


def authenticate(db: Session, username: str, password: str) -> User | None:
    """
    Перевірити логін і пароль. Повертає користувача або None.

    Навмисно НЕ розрізняємо «немає такого логіна» і «хибний пароль»:
    для зовнішнього світу це одна й та сама відмова (рекомендація OWASP).
    """
    user = get_by_username(db, username)
    if user is None or not verify_password(password, user.password_hash):
        return None
    return user
