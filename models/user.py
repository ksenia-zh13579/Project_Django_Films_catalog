"""User domain model."""

from __future__ import annotations

from typing import TYPE_CHECKING

from .rating import Rating

if TYPE_CHECKING:
    from .film import Film

VALID_STATUSES = {"хочу посмотреть", "смотрю", "просмотрено", "брошено"}


class User:
    """A catalogue user who can track and rate films."""

    def __init__(self, name: str) -> None:
        if not name.strip():
            raise ValueError("Имя пользователя не может быть пустым")
        self.name = name
        self.statuses: dict[str, str] = {}

    def set_status(self, film: Film, status: str) -> None:
        """Set the user's status for a film."""
        if status not in VALID_STATUSES:
            raise ValueError(f"Неизвестный статус: {status}")
        self.statuses[film.name] = status

    def rate_film(self, film: Film, value: int) -> Rating:
        """Rate a film and return the created rating."""
        rating = Rating(self, film, value)
        film.add_rating(rating)
        return rating

    def __str__(self) -> str:
        return self.name
