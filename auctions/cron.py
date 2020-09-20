from .models import AuctionListing, Bid
from django.utils import timezone


def closeoutExpiredListings():
    now = timezone.now()
    exp_listings = AuctionListing.objects.filter(
        expiration__lt=now, is_active=True)
    for listing in exp_listings:
        if len(Bid.objects.filter(listing=listing.id, is_active=True)) > 0:
            bid = Bid.objects.get(listing=listing.id, is_active=True)
            bid.is_winner = True
            bid.is_active = False
            bid.save()

            listing.is_active = False
            listing.save()

    return exp_listings
