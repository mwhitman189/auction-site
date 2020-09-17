from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Count

from .forms import NewListingForm, NewBidForm
from .models import User, AuctionListing, Bid, WatchList


def index(request):
    listings = AuctionListing.objects.all()

    return render(request, "auctions/index.html", {"listings": listings})


def listing(request, listing_id):
    listing = AuctionListing.objects.get(id=listing_id)

    # Check for existing bids. If none are present, set the current bid to
    # the listing starting_bid
    if Bid.objects.filter(listing=listing_id, is_active=True).exists():
        bid_object = Bid.objects.get(listing=listing_id, is_active=True)
        current_bid = bid_object.amount
    else:
        current_bid = listing.starting_bid

    if request.method == "POST":
        form = NewBidForm(request.POST)

        if form.is_valid():
            # If the current existing bid is greater than the input amount, return an error
            if current_bid > form.cleaned_data["amount"]:
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "current_bid": current_bid,
                    "form": form,
                    "error": "Bid must be higher than current bid"
                })
            else:
                current_bid = form.cleaned_data["amount"]
                # Deactivate old bids
                bid_object.is_active = False
                bid_object.save()

                bid = form.save(commit=False)
                bid.listing = listing
                bid.bidder = request.user
                bid.save()

                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "current_bid": bid.amount,
                    "form": NewBidForm()
                })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "current_bid": current_bid,
                "form": form
            })

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "current_bid": current_bid,
        "form": NewBidForm()
    })


def new_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)

        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()

            return HttpResponseRedirect(reverse("auctions:listing", args={listing.id}))

        else:
            return render(request, "auctions/new_listing.html", {"form": form})

    else:
        return render(request, "auctions/new_listing.html", {"form": NewListingForm()})


def new_watchlist_item(request, listing_id):
    user = request.user
    listing = AuctionListing.objects.get(id=listing_id)

    if user.watchlist:
        watchlist = WatchList(user=request.user, listing=listing)
        watchlist.save()
    else:
        watchlist = WatchList.objects.get(user=user.id)

    return HttpResponseRedirect(reverse("auctions:listing", args={listing_id}))


def categories(request):
    categories = AuctionListing.objects.values(
        'category').annotate(item_count=Count('category'))
    return render(request, "auctions/categories.html", {"categories": categories})


def category(request, category):
    category_items = AuctionListing.objects.filter(category=category)
    return render(request, "auctions/category.html", {"category": category, "category_items": category_items})


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")
