from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", related_name="watchlist", blank=True)
    pass


class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator")
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(
        blank=True, null=True, max_digits=10, decimal_places=2
    )
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    active = models.BooleanField(default=True)
    winner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="winner", blank=True, null=True
    )
    date = models.DateField(auto_now_add=True)


class Bid(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bidder", blank=True, null=True
    )
    bid = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="listing", null=True, blank=True
    )


class Comment(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commentor", blank=True, null=True
    )
    text = models.TextField()
    listing = models.ForeignKey(
        Listing,
        on_delete=models.CASCADE,
        related_name="comment_listing",
        blank=True,
        null=True,
    )
