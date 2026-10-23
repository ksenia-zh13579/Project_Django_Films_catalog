from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from films.services import get_films, get_users


def home(request: HttpRequest) -> HttpResponse:
    """Display a catalogue overview."""
    films = get_films()
    return render(
        request,
        "homepage/home.html",
        {"films": films, "film_count": len(films)},
    )


def user_list(request: HttpRequest) -> HttpResponse:
    """Display users and their statuses."""
    users = get_users()
    return render(request, "homepage/user_list.html", {"users": users})


def about(request: HttpRequest) -> HttpResponse:
    """Display a short description of the catalogue."""
    return render(request, "homepage/about.html")
