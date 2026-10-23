import pytest

from models import Film, Rating, User


def test_rating_has_related_user_and_film() -> None:
    user = User("Анна")
    film = Film("Фильм", "Режиссер", [])
    rating = Rating(user, film, 10)

    assert rating.user is user
    assert rating.film is film
    assert str(rating) == "Анна: 10/10 для «Фильм»"


def test_rating_value_must_be_between_one_and_ten() -> None:
    user = User("Анна")
    film = Film("Фильм", "Режиссер", [])

    with pytest.raises(ValueError):
        Rating(user, film, 11)
