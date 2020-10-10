from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.timezone import now


class User(AbstractUser):
    pass
class Category(models.TextChoices):
    books         = "Books"
    sports        = "Sports"
    fashion       = "Fashion"
    electronics   = "Electronics"
    toys          = "Toys"
    clothing      = "Clothing"
    other         = "Other"

class Listing(models.Model):
    id            = models.AutoField(primary_key=True)
    title         = models.CharField(max_length=40)
    description   = models.TextField(max_length=400)
    startingBid   = models.IntegerField()
    listedBy      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="user_listings" , null=True)
    createdOn     = models.DateTimeField( auto_now_add=True )
    image         = models.CharField(max_length= 250, blank=True)
    active        = models.BooleanField(default=True)
    watchers      = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="watchlist")
    category      = models.CharField(max_length=15, choices=Category.choices, default="Other")
    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    id            = models.AutoField(primary_key=True)
    listing       = models.ForeignKey(Listing, on_delete=models.CASCADE,related_name="bids")
    bidder        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, related_name="user_bids")
    bid           = models.IntegerField()
    def __gt__(self, other):
        return self.bid > other.bid
    def __str__(self):
        return f"{self.bid}"
    
class Comment(models.Model):
    text          = models.TextField(max_length=450)
    listing       = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listing_comments")
    user          = models.ForeignKey(User, on_delete=models.CASCADE, related_name= "user_comments")
    time          = models.DateTimeField( auto_now_add=True)
