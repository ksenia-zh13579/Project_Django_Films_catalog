"""SQLite data access for the film catalogue web interface."""

from __future__ import annotations

import sqlite3

from db.database import fetch_all, get_connection


FILMS_QUERY = """
SELECT
    f.id,
    f.name,
    f.director,
    COALESCE(GROUP_CONCAT(DISTINCT g.name), '') AS genres,
    COUNT(DISTINCT r.id) AS rating_count,
    COALESCE(ROUND(AVG(r.value), 2), 0) AS average_rating
FROM films AS f
LEFT JOIN film_genres AS fg ON fg.film_id = f.id
LEFT JOIN genres AS g ON g.id = fg.genre_id
LEFT JOIN ratings AS r ON r.film_id = f.id
GROUP BY f.id, f.name, f.director
ORDER BY f.name
"""


def _with_genres(row: sqlite3.Row) -> dict[str, object]:
    """Convert a database row into a template-friendly film context."""
    film = dict(row)
    film["genres"] = (
        [genre for genre in str(row["genres"]).split(",") if genre]
        if row["genres"]
        else []
    )
    return film


def get_films() -> list[dict[str, object]]:
    """Return films with genres and aggregate ratings from SQLite."""
    return [_with_genres(row) for row in fetch_all(FILMS_QUERY)]


def get_film_by_index(index: int) -> dict[str, object]:
    """Return a film with its ratings by displayed catalogue index."""
    films = get_films()
    try:
        film = films[index]
    except IndexError as exc:
        raise LookupError("Произведение не найдено") from exc
    ratings_query = """
    SELECT u.name AS user_name, r.value
    FROM ratings AS r
    JOIN users AS u ON u.id = r.user_id
    WHERE r.film_id = ?
    ORDER BY u.name
    """
    result = dict(film)
    result["ratings"] = [
        dict(row) for row in fetch_all(ratings_query, (film["id"],))
    ]
    return result


def get_users() -> list[dict[str, object]]:
    """Return users and their statuses from SQLite."""
    users_query = "SELECT id, name FROM users ORDER BY name"
    status_query = """
    SELECT f.name AS film_name, s.status
    FROM statuses AS s
    JOIN films AS f ON f.id = s.film_id
    WHERE s.user_id = ?
    ORDER BY f.name
    """
    users: list[dict[str, object]] = []
    with get_connection() as conn:
        for row in conn.execute(users_query):
            user = dict(row)
            user["statuses"] = {
                status["film_name"]: status["status"]
                for status in conn.execute(status_query, (row["id"],))
            }
            users.append(user)
    return users
