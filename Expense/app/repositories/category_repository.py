from app.database import Connection
from app.database_helper import execute, fetch_all, fetch_one

UPDATABLE = {"name": "name = %(name)s"}


def create(conn: Connection, data: dict) -> dict:
    new_id, _ = execute(conn, "INSERT INTO categories (name) values(%(name)s)", data)
    return get_by_id(conn, new_id)


def get_by_id(conn: Connection, category_id: int) -> dict | None:
    return fetch_one(
        conn, "SELECT id, name FROM categories WHERE id=%(id)s", {"id": category_id}
    )


def get_all(conn: Connection) -> list[dict]:
    return fetch_all(conn, "SELECT id, name FROM categories ORDER BY id")


def update(conn: Connection, category_id: int, changes: dict) -> dict | None:
    unknown = set(changes) - set(UPDATABLE)
    if unknown or not changes:
        raise ValueError("Недозоволені поля або не задані")

    set_sql = ", ".join(UPDATABLE[field] for field in UPDATABLE if field in changes)
    params = {field: changes[field] for field in UPDATABLE if field in changes}
    execute(
        conn,
        "UPDATE categories SET " + set_sql + "  WHERE ID =%(id)s",
        {**params, "id": category_id},
    )
    return get_by_id(conn, category_id)


def delete(conn: Connection, category_id: int) -> bool:
    _, deleted = execute(
        conn, "DELETE FROM categories WHERE id = %(id)s", {"id": category_id}
    )
    return deleted > 0
