from django.contrib.auth.models import AbstractUser
from django.db import models

# One User can have multiple auctions, but one auction can only have one user
# One User can have multiple bids, but one bid can only have one user
# One User can have multiple comments, but one comment can only have one user
# One Auction can have multiple bids, but one bid can only have one auction
# One Auction can have multiple comments, but one comment can only have one auction

class User(AbstractUser):
    pass

class Auction(models.Model):
    category_choices = (
        ("Fashion", "Fashion"),
        ("Toys", "Toys"),
        ("Electronics", "Electronics"),
        ("Home", "Home"),
        ("Other", "Other"),
    )

    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.CharField(max_length=100, blank=True)
    category = models.CharField(max_length=100, choices=category_choices, blank=True)
    is_active = models.BooleanField(default=True)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    winner = models.CharField(max_length=100, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} - {self.description} - {self.user}"

class Bid(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.auction} - {self.price}"

class Comment(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.auction} - {self.text} - {self.user}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} - {self.auction}"