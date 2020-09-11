from django import forms
from django.db.models import Count
from .models import AuctionListing

# categories = AuctionListing._meta.get_field('category').choices


class NewListingForm(forms.ModelForm):
    class Meta:
        model = AuctionListing
        fields = ['name', 'category', 'starting_bid',
                  'buyout_price', 'details', 'img', 'expiration']
