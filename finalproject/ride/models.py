from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Ride(models.Model):
    derparture = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    schedule = models.CharField(max_length=100)
    seats = models.IntegerField()
    driver = models.ForeignKey(User, on_delete=models.CASCADE)
    passengers = models.ManyToManyField(User, related_name='passengers')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.derparture} to {self.destination}'
