from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.read_entry, name="read_entry"),
    path("search/", views.search, name="search"),
    path("create/", views.create_entry, name="create_entry"),
    path("random", views.read_random, name="read_random")
]
