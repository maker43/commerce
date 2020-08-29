from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils.timezone import now


from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

def validate_bid(bid, highest_bid):
    if bid < highest_bid:
        raise ValidationError( 
        _('%(bid)s is under the minimal amount'),params = {'bid':bid}, 
        )

class User(AbstractUser):
    pass
class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=40)
    description = models.TextField(max_length=400)
    startingBid = models.IntegerField()
    listedBy = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="user_listings" , null=True)
    createdOn = models.DateTimeField( auto_now_add=True )
    image = models.ImageField(upload_to = 'images')
    active = models.BooleanField(default=True)

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

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE,related_name="bids")
    bidder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, related_name="user_bids")
    bid = models.IntegerField(validators=[validate_bid])

    def __gt__(self, other):
        return self.bid > other.bid
    def __str__(self):
        return f"{self.bid}"
    def validate_bid(bid, highest_bid):
        if bid < highest_bid:
            raise ValidationError( 
            _('%(bid)s is under the minimal amount'),params = {'bid':bid}, 
            )
    
    # Bids need to be related to the Listing and to the User, so table should have User ralated to the bid by 
    # having the biggest bid and user that has posted that Listing
    #                  ##BID
    #             ## Seller## Listing (starting bid)
    #             ## Buyer ## Highest Bidder ## 
    #             #  
