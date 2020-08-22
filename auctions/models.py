from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField(max_length=400)
    startingBid = models.IntegerField()
    image = models.ImageField(upload_to = 'images')

    class Category(models.TextChoices):
        sports = "Sports"
        fashion = "Fashion"
        electronics = "Electronics"
        toys = "Toys"
        clothing = "Clothing"
        other = "Other"
    category = models.CharField(max_length=15, choices=Category.choices, default="Other")
    def __str__(self):
        return f"{self.title}"