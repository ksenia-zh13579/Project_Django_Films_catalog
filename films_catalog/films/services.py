"""Data access helpers for the film catalogue web interface."""

from pathlib import Path

from django.conf import settings

from main import load_films, load_users
from models import Film, User


def get_users() -> list[User]:
    """Load catalogue users from the shared JSON data."""
    return load_users(Path(settings.DATA_DIR) / "users.json")


def get_films(users: list[User] | None = None) -> list[Film]:
    """Load films and connect their ratings to shared user objects."""
    users_list = users if users is not None else get_users()
    users_by_name = {user.name: user for user in users_list}
    return load_films(Path(settings.DATA_DIR) / "films.json", users_by_name)


def get_film_by_index(index: int) -> Film:
    """Return a film by its displayed catalogue index."""
    films = get_films()
    try:
        return films[index]
    except IndexError as exc:
        raise LookupError("Произведение не найдено") from exc
