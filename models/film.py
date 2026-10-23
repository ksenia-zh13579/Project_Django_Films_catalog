"""Film domain model."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .rating import Rating


class Film:
    """An animation film or series and its ratings."""

    def __init__(
        self,
        name: str,
        director: str,
        genres: list[str],
        ratings: list[Rating] | None = None,
    ) -> None:
        if not name.strip():
            raise ValueError("Название произведения не может быть пустым")
        if not director.strip():
            raise ValueError("Режиссер не может быть пустым")
        self.name = name
        self.director = director
        self.genres = list(genres)
        self.ratings = list(ratings or [])

    def add_rating(self, rating: Rating) -> None:
        """Add a rating belonging to this film."""
        if rating.film is not self:
            raise ValueError("Оценка относится к другому произведению")
        self.ratings.append(rating)

    def average_rating(self) -> float:
        """Return the average rating, or zero when there are no ratings."""
        if not self.ratings:
            return 0.0
        return sum(rating.value for rating in self.ratings) / len(self.ratings)

    def __str__(self) -> str:
        return f"{self.name} ({self.director})"
