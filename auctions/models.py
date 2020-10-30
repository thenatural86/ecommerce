from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.IntegerField()
    image = models.TextField()
    category = models.CharField(max_length=64)


class Bid(models.Model):
    user = models.CharField(max_length=64)
    title = models.CharField(max_length=64)
    bid = models.IntegerField()


class Comment(models.Model):
    user = models.CharField(max_length=64)
    comment = models.TextField()
    listingid = models.IntegerField()


class Watchlist(models.Model):
    user = models.CharField(max_length=64)
    listingid = models.IntegerField()
