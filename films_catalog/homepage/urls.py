from django.urls import path

from . import views

app_name = "homepage"

urlpatterns = [
    path("", views.home, name="home"),
    path("users/", views.user_list, name="users"),
    path("about/", views.about, name="about"),
]
