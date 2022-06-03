from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Ride(models.Model):
    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    schedule = models.CharField(max_length=100)
    seats = models.IntegerField()
    price = models.IntegerField(default=0)
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    passengers = models.ManyToManyField(User, related_name='passengers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.departure} to {self.destination}'


class Message(models.Model):
    sender = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='receiver')
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender} to {self.receiver} in {self.ride}'
