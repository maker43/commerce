from django import forms
from .models import Listing, Bid

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        exclude = ["active","listedBy", "createdOn"]

class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = [ "bid", ]



        # bid should be presented on the page, starting bid is there and current bit should also be there 
        # cuurent bid is part of the bid class and maybe Bid should be child class off Listing ** that is an interesting concept
