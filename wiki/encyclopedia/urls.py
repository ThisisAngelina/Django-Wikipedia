from django.urls import path

from . import views


urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.read_entry, name="read_entry"),
    path("search", views.search, name="search"),
]
