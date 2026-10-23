"""Application entry point and collection/JSON operations."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from models import Film, Rating, User

DEFAULT_DATA_DIR = Path(__file__).resolve().parent / "data"


def get_film_rating(film_ratings: list[int]) -> float:
    """Return the average of integer ratings."""
    if not film_ratings:
        return 0.0
    return sum(film_ratings) / len(film_ratings)


def find_film(films: list[Film], name: str) -> Film:
    """Find a film by name."""
    for film in films:
        if film.name == name:
            return film
    raise LookupError(f"Произведение не найдено: {name}")


def films_to_dict(films: list[Film]) -> list[dict[str, Any]]:
    """Convert film objects to JSON-compatible dictionaries."""
    return [
        {
            "name": film.name,
            "director": film.director,
            "genres": film.genres,
            "ratings": [
                {"user": rating.user.name, "value": rating.value}
                for rating in film.ratings
            ],
        }
        for film in films
    ]


def save_films(films: list[Film], path: Path | str) -> None:
    """Save films and their ratings to a JSON file."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(films_to_dict(films), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_films(path: Path | str, users: dict[str, User] | None = None) -> list[Film]:
    """Load films from JSON and reconnect ratings with user objects."""
    source = Path(path)
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Не удалось загрузить данные из {source}") from exc

    users_by_name = users if users is not None else {}
    films: list[Film] = []
    for item in data:
        film = Film(item["name"], item["director"], item["genres"])
        for item_rating in item.get("ratings", []):
            user = users_by_name.setdefault(
                item_rating["user"], User(item_rating["user"])
            )
            film.add_rating(Rating(user, film, item_rating["value"]))
        films.append(film)
    return films


def users_to_dict(users: list[User]) -> list[dict[str, Any]]:
    """Convert user objects to JSON-compatible dictionaries."""
    return [{"name": user.name, "statuses": user.statuses} for user in users]


def save_users(users: list[User], path: Path | str) -> None:
    """Save users and their statuses to a JSON file."""
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(
        json.dumps(users_to_dict(users), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_users(path: Path | str) -> list[User]:
    """Load users from JSON."""
    source = Path(path)
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"Не удалось загрузить данные из {source}") from exc
    users: list[User] = []
    for item in data:
        user = User(item["name"])
        user.statuses = dict(item.get("statuses", {}))
        users.append(user)
    return users


def create_initial_data(
    data_dir: Path | str = DEFAULT_DATA_DIR,
) -> tuple[list[Film], list[User]]:
    """Create the initial object collections used by the application."""
    alice = User("Анна")
    bob = User("Иван")
    spirited_away = Film(
        "Унесенные призраками",
        "Хаяо Миядзаки",
        ["фэнтези", "приключения", "драма"],
    )
    alice.set_status(spirited_away, "просмотрено")
    alice.rate_film(spirited_away, 10)
    bob.rate_film(spirited_away, 8)
    films = [spirited_away]
    users = [alice, bob]
    directory = Path(data_dir)
    save_films(films, directory / "films.json")
    save_users(users, directory / "users.json")
    return films, users


if __name__ == "__main__":
    films, _ = create_initial_data()
    for film in films:
        print(f"Название фильма: {film.name}")
        print(f"Режиссер фильма: {film.director}")
        print(f"Жанры: {film.genres}")
        print(f"Средняя оценка: {film.average_rating()}")
