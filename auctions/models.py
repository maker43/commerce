from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=40)
    description = models.TextField(max_length=400)
    startingBid = models.IntegerField()
    image = models.ImageField(upload_to = 'images')
    listedBy = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    createdOn = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

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

class Bids(models.Model):

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    seller = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    bidder = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True)
    bid = models.IntegerField()
    

    # Bids need to be related to the Listing and to the User, so table should have User ralated to the bid by 
    # having the biggest bid and user that has posted that Listing
    #                  ##BID
    #             ## Seller## Listing (starting bid)
    #             ## Buyer ## Highest Bidder ## 
    #             #  