"""Connection and query helpers for the catalogue SQLite database."""

from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any, Iterable

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATABASE_PATH = PROJECT_ROOT / "db" / "films_catalog.sqlite3"
SCHEMA_PATH = PROJECT_ROOT / "sql" / "schema.sql"


def get_connection() -> sqlite3.Connection:
    """Open a foreign-key-aware connection with named result columns."""
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def initialize_database() -> None:
    """Create all catalogue tables when they do not exist."""
    with get_connection() as conn:
        conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))


def fetch_all(
    query: str, parameters: Iterable[Any] = ()
) -> list[sqlite3.Row]:
    """Execute a read query and return rows with name-based access."""
    with get_connection() as conn:
        return conn.execute(query, tuple(parameters)).fetchall()
