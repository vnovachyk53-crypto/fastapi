from typing import Any

from .database import Connection


# -----------------
def fetch_all(
    conn: Connection, sql: str, params: tuple | dict = ()
) -> list[dict[str, Any]]:
    with conn.cursor(dictionary=True) as cur:
        cur.execute(sql, params)
        return cur.fetchall()


def fetch_one(
    conn: Connection, sql: str, params: tuple | dict = ()
) -> dict[str, Any] | None:
    with conn.cursor(dictionary=True) as cur:
        cur.execute(sql, params)
        return cur.fetchone()


def execute(conn: Connection, sql: str, params: tuple | dict = ()) -> tuple[int, int]:
    """Повертає (lastrowid, rowcount). Commit робить сервіс."""
    with conn.cursor() as cur:
        cur.execute(sql, params)
        return cur.lastrowid, cur.rowcount
