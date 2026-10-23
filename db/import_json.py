"""Import the existing JSON catalogue into SQLite."""

from __future__ import annotations

import json
from pathlib import Path

from .database import get_connection, initialize_database

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"


def import_json_data() -> None:
    """Replace SQLite catalogue data with the JSON source data."""
    films_data = json.loads(
        (DATA_DIR / "films.json").read_text(encoding="utf-8")
    )
    users_data = json.loads(
        (DATA_DIR / "users.json").read_text(encoding="utf-8")
    )
    initialize_database()
    with get_connection() as conn:
        conn.executescript(
            """
            DELETE FROM statuses;
            DELETE FROM ratings;
            DELETE FROM film_genres;
            DELETE FROM genres;
            DELETE FROM films;
            DELETE FROM users;
            """
        )
        conn.executemany(
            "INSERT INTO films (name, director) VALUES (?, ?)",
            [(film["name"], film["director"]) for film in films_data],
        )
        conn.executemany(
            "INSERT INTO users (name) VALUES (?)",
            [(user["name"],) for user in users_data],
        )

        film_ids = {
            row["name"]: row["id"]
            for row in conn.execute("SELECT id, name FROM films")
        }
        user_ids = {
            row["name"]: row["id"]
            for row in conn.execute("SELECT id, name FROM users")
        }
        genres = {
            genre
            for film in films_data
            for genre in film.get("genres", [])
        }
        conn.executemany(
            "INSERT INTO genres (name) VALUES (?)",
            [(genre,) for genre in sorted(genres)],
        )
        genre_ids = {
            row["name"]: row["id"]
            for row in conn.execute("SELECT id, name FROM genres")
        }
        conn.executemany(
            "INSERT INTO film_genres (film_id, genre_id) VALUES (?, ?)",
            [
                (film_ids[film["name"]], genre_ids[genre])
                for film in films_data
                for genre in film.get("genres", [])
            ],
        )
        conn.executemany(
            "INSERT INTO ratings (film_id, user_id, value) VALUES (?, ?, ?)",
            [
                (film_ids[film["name"]], user_ids[rating["user"]], rating["value"])
                for film in films_data
                for rating in film.get("ratings", [])
            ],
        )
        conn.executemany(
            """
            INSERT INTO statuses (film_id, user_id, status)
            VALUES (?, ?, ?)
            """,
            [
                (film_ids[film_name], user_ids[user["name"]], status)
                for user in users_data
                for film_name, status in user.get("statuses", {}).items()
            ],
        )
        conn.commit()


if __name__ == "__main__":
    import_json_data()
    print("JSON-данные перенесены в SQLite.")
