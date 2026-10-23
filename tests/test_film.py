import json

from main import find_film, load_films, save_films
from models import Film, User


def test_film_interacts_with_user_rating() -> None:
    user = User("Анна")
    film = Film("Фильм", "Режиссер", ["драма"])

    user.rate_film(film, 9)

    assert film.average_rating() == 9
    assert str(film) == "Фильм (Режиссер)"


def test_film_rating_is_serialized_and_loaded(tmp_path) -> None:
    user = User("Анна")
    film = Film("Фильм", "Режиссер", ["драма"])
    user.rate_film(film, 9)
    path = tmp_path / "films.json"

    save_films([film], path)
    loaded = load_films(path, {user.name: user})

    assert find_film(loaded, "Фильм").ratings[0].value == 9
    assert json.loads(path.read_text(encoding="utf-8"))[0]["name"] == "Фильм"


def test_empty_rating_collection_has_zero_average() -> None:
    film = Film("Фильм", "Режиссер", [])

    assert film.average_rating() == 0.0
