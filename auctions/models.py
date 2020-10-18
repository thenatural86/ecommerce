from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

# do these classes need id's?


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
