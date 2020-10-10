from django.contrib import messages
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime
from .models import User, Listing, Bid, Comment,Category
from .forms import ListingForm, BidForm, CommentForm
from django.contrib.auth.decorators import login_required

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
        form = ListingForm( request.POST)
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
            highest_bid = int(max(listing.bids.all()).bid)
            highest_bidder = max(listing.bids.all()).bidder
    else:
        highest_bid = listing.startingBid
        highest_bidder = None

    if request.method == "POST":
        #get all post information
        form = BidForm(request.POST)
        bidAmount = int(request.POST.get("bid", False))
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
        "form":BidForm(),"comment_form":CommentForm(), "listing":listing, "highest_bid_amount": bidAmount,
        "highest_bidder": bidder, 
        })
        else:
            messages.error(request, f'Bid not high enough. Bid must be at least{highest_bid+1}')
            return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))
    else:
        return render( request, "auctions/listing.html", {
        "form":BidForm(), "comment_form":CommentForm(),"listing":listing, "highest_bid_amount": highest_bid,
        "highest_bidder": highest_bidder, 
        })

def deactivate_listing(request, listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk = listing_id)
        listing.active = False
        listing.save()
        return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))

@login_required
def watchlist_view(request):
    user = request.user
    if request.method == "POST":
        listing_id = request.POST.get("listing_id", False)
        listing = Listing.objects.get(pk=listing_id)
        add = request.POST["add"]
        if add == "True":
            user.watchlist.add(listing)
            user.save()
        elif add == "False":
            user.watchlist.remove(listing)
            user.save()
        watchlist = user.watchlist.all()
        return HttpResponseRedirect(reverse("listing_page", args=(listing.id,)))
    if request.user.is_anonymous:
        watchlist = None
    else:
        watchlist = user.watchlist.all()
    return render(request, "auctions/watchlist.html", {
        "watchlist":watchlist
    })

@login_required
def comment_view(request,listing_id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=listing_id)
        comment_text = request.POST.get("text",False)
        user = request.user
        comment= Comment( text=comment_text, user=user, listing=listing )
        comment.save()
        return HttpResponseRedirect(reverse("listing_page", args=(listing_id,)))

def categories_view(request):
    categories = Category.values
    return render(request, 'auctions/categories.html', {
        "categories":categories,
    })
def category_view(request, category_name):
    listings = Listing.objects.all()
    category_listings = []
    for listing in listings:
        if listing.category == category_name:
            category_listings.append(listing)
    
    return render(request, 'auctions/category.html', {
        "listings": listings, "category_listings": category_listings, "category_name":category_name,
    })