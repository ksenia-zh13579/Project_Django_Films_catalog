from django.urls import path

from . import views

app_name = "films"

urlpatterns = [
    path("", views.film_list, name="list"),
    path("<int:film_index>/", views.film_detail, name="detail"),
]
