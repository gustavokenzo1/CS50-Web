from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:language>", views.language, name="language"),
    path("search", views.search, name="search"),
    path("new_page", views.new_page, name="new_page"),
    path("error", views.error, name="error"),
    path("edit/<str:language>", views.edit, name="edit"),
    path("random", views.random_page, name="random"),
]
