"""Бізнес-логіка каталогу книг. Дані зберігаються в пам'яті процесу."""

_BOOKS: list[dict] = [
    {"id": 1, "title": "Кобзар", "author": "Т. Шевченко", "genre": "Поезія"},
    {"id": 2, "title": "Лісова пісня", "author": "Леся Українка", "genre": "Драма"},
    {"id": 3, "title": "Тіні забутих предків", "author": "М. Коцюбинський", "genre": "Повість"},
]


def list_books() -> list[dict]:
    return _BOOKS


def get_book(book_id: int) -> dict | None:
    return next((book for book in _BOOKS if book["id"] == book_id), None)


def create_book(title: str, author: str, genre: str) -> dict:
    new_id = max((book["id"] for book in _BOOKS), default=0) + 1
    book = {"id": new_id, "title": title, "author": author, "genre": genre}
    _BOOKS.append(book)
    return book


def update_book(book_id: int, changes: dict) -> dict | None:
    book = get_book(book_id)
    if book is None:
        return None
    book.update(changes)
    return book


def delete_book(book_id: int) -> dict | None:
    book = get_book(book_id)
    if book is None:
        return None
    _BOOKS.remove(book)
    return book
