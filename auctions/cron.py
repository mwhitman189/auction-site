from .models import AuctionListing, Bid
import datetime


def closeoutExpiredListings():
    print("Working!")
    # now = datetime.datetime.now()
    # exp_listings = AuctionListing.objects.filter(
    #     expiration__lt=now, is_active=True)
    # print(now)
    # for listing in exp_listings:
    #     print(listing.id)
    #     bid = Bid.objects.get(listing=listing.id, is_active=True)
    #     bid.is_winner = True
    #     bid.is_active = False
    #     bid.save()

    #     listing.is_active = False
    #     listing.save()

    # return exp_listings
