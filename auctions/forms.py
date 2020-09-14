from django import forms
from django.db.models import Count
from .models import AuctionListing, Bid


class NewListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['item', 'category', 'starting_bid',
                  'buyout_price', 'details', 'img', 'expiration']


class NewBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ['amount']
