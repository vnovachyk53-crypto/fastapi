"""
models.py — моделі ORM: кожен клас описує таблицю в базі даних.
"""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    """Таблиця users: користувачі застосунку."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)  # логін, унікальний
    # Зберігаємо НЕ пароль, а його хеш (Argon2). 255 символів — з запасом.
    password_hash: Mapped[str] = mapped_column(String(255))
