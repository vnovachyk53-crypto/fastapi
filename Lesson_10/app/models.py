from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150))
    release_year: Mapped[int] = mapped_column(Integer)
    genre: Mapped[str] = mapped_column(String(50))
    producer: Mapped[str | None] = mapped_column(String(100), default=None)
    duration: Mapped[int] = mapped_column(Integer)
    actors: Mapped[str] = mapped_column(Text)