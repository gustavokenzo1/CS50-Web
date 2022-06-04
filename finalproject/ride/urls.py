from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("register", views.register_view, name="register"),
    path("login", views.login_view, name="login"),
    path('rides', views.rides, name='rides'),
    path('rides/new', views.new_ride, name='new_ride'),
    path("get_rides", views.get_rides, name="get_rides"),
    path("rides/personal", views.personal_rides, name="personal_rides"),
    path('ride/delete/<int:ride_id>', views.delete_ride, name='delete_ride'),
    path('ride/<int:ride_id>', views.ride_details, name='ride_details'),
    path('ride/<int:ride_id>/message', views.message_ride, name='message_ride'),
]
