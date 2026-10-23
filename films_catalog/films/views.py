from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import render

from .services import get_film_by_index, get_films


def film_list(request: HttpRequest) -> HttpResponse:
    """Display all films in the catalogue."""
    return render(request, "films/film_list.html", {"films": get_films()})


def film_detail(request: HttpRequest, film_index: int) -> HttpResponse:
    """Display details and ratings for one film."""
    try:
        film = get_film_by_index(film_index)
    except LookupError as exc:
        raise Http404(str(exc)) from exc
    return render(
        request,
        "films/film_detail.html",
        {"film": film, "film_index": film_index},
    )
