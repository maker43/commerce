from django import forms
from .models import Listing, Bid, Comment

class ListingForm(forms.ModelForm):
    class Meta:
        model   = Listing
        exclude = ["active","listedBy", "createdOn", "watchers"]

class BidForm(forms.ModelForm):
    class Meta:
        model  = Bid
        fields = [ "bid", ]

class CommentForm(forms.ModelForm):
    class Meta:
        model  = Comment
        fields = ["text"]
        labels = {
            "text":'',
        }
