from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Post(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="posts")
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.text}"


class Like(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE)
    post = models.ForeignKey(
        "Post", on_delete=models.CASCADE, related_name="likes")

    def __str__(self):
        return f"{self.user} - {self.post}"

class Follow(models.Model):
    user = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="following")
    follower = models.ForeignKey(
        "User", on_delete=models.CASCADE, related_name="followers")

    def __str__(self):
        return f"{self.user} - {self.follower}"

