from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register_view, name="register"),
    path("login", views.login_view, name="login"),
    path('rides', views.rides, name='rides'),
    path('rides/new', views.new_ride, name='new_ride'),
    path("get_rides", views.get_rides, name="get_rides"),
]
