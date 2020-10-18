from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=64)
    price = models.IntegerField()
    image = models.TextField()
    category = models.CharField(max_length=64)
