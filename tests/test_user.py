import pytest

from models import Film, User


def test_user_can_set_film_status_and_rate_film() -> None:
    user = User("Анна")
    film = Film("Фильм", "Режиссер", ["драма"])

    user.set_status(film, "смотрю")
    rating = user.rate_film(film, 9)

    assert user.statuses[film.name] == "смотрю"
    assert rating.user is user


def test_user_rejects_unknown_status() -> None:
    user = User("Анна")
    film = Film("Фильм", "Режиссер", [])

    with pytest.raises(ValueError):
        user.set_status(film, "неизвестен")
