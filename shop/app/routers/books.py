"""Публічне читання каталогу та захищені CRUD-операції."""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from app.dependencies import CurrentUser
from app.services import book_service

router = APIRouter(prefix="/books", tags=["books"])


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    author: str = Field(min_length=1, max_length=100)
    genre: str = Field(min_length=1, max_length=80)


class BookUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=150)
    author: str | None = Field(default=None, min_length=1, max_length=100)
    genre: str | None = Field(default=None, min_length=1, max_length=80)


@router.get("")
def list_books():
    """Каталог доступний усім, навіть без входу."""
    return book_service.list_books()


@router.get("/{book_id}")
def get_book(book_id: int):
    book = book_service.get_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return book


@router.post("", status_code=status.HTTP_201_CREATED)
def post_book(book_data: BookCreate, user: CurrentUser):
    return book_service.create_book(**book_data.model_dump())


@router.put("/{book_id}")
def edit_book(book_id: int, book_data: BookUpdate, user: CurrentUser):
    changes = book_data.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status_code=400, detail="Немає даних для оновлення")
    if any(value is None for value in changes.values()):
        raise HTTPException(status_code=422, detail="Поля не можуть бути порожніми")
    book = book_service.update_book(book_id, changes)
    if book is None:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return book


@router.delete("/{book_id}")
def del_book(book_id: int, user: CurrentUser):
    book = book_service.delete_book(book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Книгу не знайдено")
    return {"message": "Книгу успішно видалено", "book": book}
