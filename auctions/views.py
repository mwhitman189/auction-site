from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.encoding import force_text
from django.db.models import Count, CharField, When, Value, Case

from .forms import NewListingForm, NewBidForm
from .models import User, AuctionListing, Bid, WatchList, Comment


def index(request):
    listings = AuctionListing.objects.filter(is_active=True)

    return render(request, 'auctions/index.html', {'listings': listings})


def listing(request, listing_id):
    """
    Return a listing with the given id
    """
    listing = AuctionListing.objects.get(id=listing_id)
    is_on_watchlist = WatchList.objects.filter(listing=listing).exists()
    comments = Comment.objects.all()

    # Check for existing bids. If none are present, set the current bid to
    # the listing starting_bid
    if Bid.objects.filter(listing=listing_id, is_active=True).exists():
        bid_object = Bid.objects.get(listing=listing_id)
        current_bid = bid_object.amount

    else:
        current_bid = listing.starting_bid

    if request.method == 'POST':
        form = NewBidForm(request.POST)
        if not Bid.objects.filter(listing=listing_id, is_active=True).exists():
            bid_object = form.save(commit=False)
            bid_object.listing = listing
            bid_object.bidder = request.user

        if form.is_valid():
            # If the current existing bid is greater than the input amount, return an error
            if current_bid > form.cleaned_data['amount']:
                messages.error(
                    request, "Your bid must be higher than the current bid")
                return render(request, 'auctions/listing.html', {
                    'listing': listing,
                    'current_bid': current_bid,
                    'comments': comments,
                    'form': form
                })
            else:
                current_bid = form.cleaned_data['amount']
                # Deactivate old bids
                bid_object.is_active = False
                bid_object.save()

                bid = form.save(commit=False)
                bid.listing = listing
                bid.bidder = request.user
                bid.save()

                return render(request, 'auctions/listing.html', {
                    'listing': listing,
                    'bid': bid.amount,
                    'comments': comments,
                    'is_on_watchlist': is_on_watchlist,
                    'form': NewBidForm()
                })
        else:
            return render(request, 'auctions/listing.html', {
                'listing': listing,
                'bid': current_bid,
                'comments': comments,
                'is_on_watchlist': is_on_watchlist,
                'form': form
            })

    return render(request, 'auctions/listing.html', {
        'listing': listing,
        'bid': current_bid,
        'comments': comments,
        'is_on_watchlist': is_on_watchlist,
        'form': NewBidForm()
    })


def listing_closeout(request, listing_id):
    """
    Close out the auction if the user is the item seller
    """
    listing = AuctionListing.objects.get(id=listing_id)

    try:
        highest_bid = Bid.objects.get(listing=listing, is_active=True)
        if request.user.id == listing.seller.id:
            listing.is_active = False
            highest_bid.is_winner = True
            highest_bid.is_active = False

    except Bid.DoesNotExist:
        messages.error(request, "There are no bids on this item")
        return HttpResponseRedirect(reverse('auctions:listing', args={listing_id}))

    return False


def new_listing(request):
    """
    Return a form to create a new listing
    """
    if request.method == 'POST':
        form = NewListingForm(request.POST)

        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()

            return HttpResponseRedirect(reverse('auctions:listing', args={listing.id}))

        else:
            return render(request, 'auctions/new_listing.html', {'form': form})

    else:
        return render(request, 'auctions/new_listing.html', {'form': NewListingForm()})


def watchlist(request):
    """
    Return the user's watchlist
    """
    watchlist = WatchList.objects.filter(user=request.user)

    return render(request, 'auctions/watchlist.html', {'watchlist': watchlist})


def watchlist_toggle(request, listing_id):
    """
    Add listing to user's watchlist
    """
    user = request.user
    listing = AuctionListing.objects.get(id=listing_id)
    watchlist_item = WatchList.objects.filter(listing=listing)

    if watchlist_item.exists():
        watchlist_item.delete()
    else:
        watchlist_item = WatchList(user=user, listing=listing)
        watchlist_item.save()

    return HttpResponseRedirect(reverse('auctions:watchlist'))


def categories(request):
    """
    Return a list of item categories
    """
    category_counts = AuctionListing.objects.filter(is_active=True).values('category').annotate(
        count=Count('category')).order_by()

    choices = dict(AuctionListing._meta.get_field('category').flatchoices)

    for entry in category_counts:
        entry['category_abr'] = force_text(
            choices[entry['category']], strings_only=True)

    return render(request, 'auctions/categories.html', {'categories': category_counts})


def category(request, category):
    """
    Return a list of items for the given category
    """
    category_items = AuctionListing.objects.filter(
        category=category, is_active=True)

    return render(request, 'auctions/category.html', {'category': category, 'category_items': category_items})


def myItems(request):
    """
    Return a list of purchased items
    """
    purchased_items = Bid.objects.filter(is_winner=True)


def login_view(request):
    if request.method == 'POST':

        # Attempt to sign user in
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('auctions:index'))
        else:
            messages.error(request, "Invalid username and/or password")
            return render(request, 'auctions/login.html')
    else:
        return render(request, 'auctions/login.html')


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('auctions:index'))


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']

        # Ensure password matches confirmation
        password = request.POST['password']
        confirmation = request.POST['confirmation']
        if password != confirmation:
            messages.error(request, "Passwords must match")
            return render(request, 'auctions/register.html')

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.error(request, "That username is already taken")
            return render(request, 'auctions/register.html')
        login(request, user)
        return HttpResponseRedirect(reverse('auctions:index'))
    else:
        return render(request, 'auctions/register.html')
