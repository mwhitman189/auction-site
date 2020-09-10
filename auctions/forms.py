from django import forms
from django.db.models import Count
from .models import AuctionListing

categories = AuctionListing._meta.get_field('category').choices


class NewListingForm(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField(widget=forms.Textarea, max_length=400)
    starting_bid = forms.DecimalField(min_value=0.10)
    img_url = forms.URLField(
        label='The URL of an image of your item', required=False)
    category = forms.ChoiceField(choices=categories)
