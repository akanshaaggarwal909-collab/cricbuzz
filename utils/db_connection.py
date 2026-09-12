"""
utils/db_connection.py
Centralized, database-agnostic connection handling.
Supports SQLite (default, zero-setup), MySQL, and PostgreSQL.
"""
import sqlite3
import pandas as pd
from contextlib import contextmanager

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_TYPE, DB_CONFIG


def _get_raw_connection():
    """Return a raw DB-API connection for the configured DB_TYPE."""
    if DB_TYPE == "sqlite":
        conn = sqlite3.connect(DB_CONFIG["sqlite"]["path"], check_same_thread=False)
        conn.execute("PRAGMA foreign_keys = ON;")
        return conn

    elif DB_TYPE == "mysql":
        import mysql.connector
        cfg = DB_CONFIG["mysql"]
        return mysql.connector.connect(
            host=cfg["host"], port=cfg["port"], user=cfg["user"],
            password=cfg["password"], database=cfg["database"]
        )

    elif DB_TYPE == "postgresql":
        import psycopg2
        cfg = DB_CONFIG["postgresql"]
        return psycopg2.connect(
            host=cfg["host"], port=cfg["port"], user=cfg["user"],
            password=cfg["password"], dbname=cfg["database"]
        )

    else:
        raise ValueError(f"Unsupported DB_TYPE: {DB_TYPE}")


@contextmanager
def get_connection():
    """Context manager that yields a connection and always closes it."""
    conn = _get_raw_connection()
    try:
        yield conn
    finally:
        conn.close()


def run_query(sql: str, params: tuple = ()) -> pd.DataFrame:
    """Run a SELECT query and return results as a pandas DataFrame."""
    with get_connection() as conn:
        return pd.read_sql_query(sql, conn, params=params)


def execute(sql: str, params: tuple = ()) -> int:
    """Run an INSERT / UPDATE / DELETE statement. Returns affected row count."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()
        affected = cur.rowcount
        cur.close()
        return affected


def init_db(schema_path: str = "sql/schema.sql", seed_path: str = "sql/sample_data.sql"):
    """Initialize the database from the schema (and optionally seed sample data)."""
    with get_connection() as conn:
        with open(schema_path) as f:
            conn.executescript(f.read()) if DB_TYPE == "sqlite" else _run_multi(conn, f.read())
        if seed_path and os.path.exists(seed_path):
            with open(seed_path) as f:
                conn.executescript(f.read()) if DB_TYPE == "sqlite" else _run_multi(conn, f.read())
        conn.commit()


def _run_multi(conn, script: str):
    """Fallback for DB drivers without executescript (MySQL/Postgres)."""
    cur = conn.cursor()
    for statement in script.split(";"):
        statement = statement.strip()
        if statement:
            cur.execute(statement)
    cur.close()
