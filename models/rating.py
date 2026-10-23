"""Rating domain model."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .film import Film
    from .user import User


class Rating:
    """A rating assigned by a user to a film."""

    def __init__(self, user: User, film: Film, value: int) -> None:
        if not 1 <= value <= 10:
            raise ValueError("Оценка должна быть целым числом от 1 до 10")
        self.user = user
        self.film = film
        self.value = value

    def __str__(self) -> str:
        return f"{self.user.name}: {self.value}/10 для «{self.film.name}»"
