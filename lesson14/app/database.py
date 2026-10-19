from collections.abc import Iterator
from typing import Annotated, Any
from fastapi import Depends, Request
from mysql.connector import pooling
from mysql.connector.pooling import MySQLConnectionPool, PooledMySQLConnection
from app.config import Settings

Connection = PooledMySQLConnection

def create_pool(settings: Settings) -> MySQLConnectionPool:
    return pooling.MySQLConnectionPool(
        pool_name="fleet_pool",
        pool_size=settings.db_pool_size,
        host=settings.db_host,
        port=settings.db_port,
        user=settings.db_user,
        password=settings.db_password,
        database=settings.db_name,
        charset="utf8mb4",
        collation="utf8mb4_unicode_ci",
        autocommit=False,
        use_pure=True
    )

def get_conn(request: Request) -> Iterator[Connection]:
    conn = request.app.state.pool.get_connection()
    try:
        yield conn
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

Conn = Annotated[Connection, Depends(get_conn)]

def fetch_all(conn: Connection, sql: str, params: tuple = ()) -> list[dict[str, Any]]:
    with conn.cursor(dictionary=True) as cur:
        cur.execute(sql, params)
        return cur.fetchall()

def fetch_one(conn: Connection, sql: str, params: tuple = ()) -> dict[str, Any] | None:
    with conn.cursor(dictionary=True) as cur:
        cur.execute(sql, params)
        return cur.fetchone()

def execute(conn: Connection, sql: str, params: tuple = ()) -> tuple[int, int]:
    with conn.cursor() as cur:
        cur.execute(sql, params)
        return cur.lastrowid, cur.rowcount
