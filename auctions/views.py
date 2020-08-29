from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime
from .models import User, Listing
from .forms import ListingForm, BidForm

def validate_bid(bid, highest_bid):
    if bid < highest_bid:
        raise ValidationError( 
        _('%(bid)s is under the minimal amount'),params = {'bid':bid}, 
        )

def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings":listings
    } )


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    if request.method == "POST":
        form = ListingForm( request.POST, request.FILES)
        user = request.user

        if form.is_valid():
            listing = form.instance
            listing.listedBy = user 
            listing.save()

            return render(request, "auctions/index.html", {
                "listings": Listing.objects.all()
            })

    else:
        form = ListingForm()
    
    return render(request, "auctions/create.html",{
        "form":form
    })

def listing_page(request,listing_id):
    listing = Listing.objects.get(pk=listing_id)
    # define highest bid
    if len(listing.bids.all()) > 0:
            highest_bid = int(max(listing.bids.values_list('bid'))[0])
            highest_bidder = max(listing.bids.all()).bidder
    else:
        highest_bid = listing.startingBid
        highest_bidder = "First bid is yet to be made."

    if request.method == "POST":
        #get all post information
        form = BidForm(request.POST)
        bidAmount = int(request.POST["bid"])
        bidder = request.user
        # check if the new bid is Valid
        if bidAmount > highest_bid:
            # if its bigger save it and present the page
            bid = form.instance
            bid.bidder = bidder
            bid.listing = listing
            bid.bid = bidAmount
            bid.save()
            return render( request, "auctions/listing.html", {
        "form":BidForm(), "listing":listing, "highest_bid_amount": bidAmount,
        "highest_bidder": bidder, 
        })
        else:
            # return message that input is not good
            # i need also to manage that bid is changed on the main page
            
            return render(request, "auctions/listing.html", {
                "form": BidForm(), "listing": listing, "highest_bid_amount": highest_bid,
                "highest_bidder": None, "error": f"Value error: Your bid ({bidAmount}$) is not high enough.\nMinimal bid is: {highest_bid+1}$"
            })
    else:
        return render( request, "auctions/listing.html", {
        "form":BidForm(), "listing":listing, "highest_bid_amount": highest_bid,
        "highest_bidder": highest_bidder,
        })