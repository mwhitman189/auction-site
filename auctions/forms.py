from django import forms
from django.db.models import Count
from .models import AuctionListing

BOOKS = 'BKS'
BUSINESS_N_INDUSTRIAL = 'BNI'
CLOTHING_SHOES_N_ACCESSORIES = 'CSE'
COLLECTIBLES = 'COL'
CONSUMER_ELECTRONICS = 'CEL'
CRAFTS = 'CFT'
HOME_N_GARDEN = 'HNG'
MOTORS = 'MTR'
PET_SUPPLIES = 'PTS'
SPORTING_GOODS = 'SPT'
SPORTS_MEM = 'SPM'
TOYS_N_HOBBIES = 'TNH'
ANTIQUES = 'ATQ'
COMPUTERS_N_NETWORKING = 'CNN'

categories = [
    ("", "--Category--"),
    ("BKS", "Books"),
    ("BNI", "Business & Industrial"),
    ("CSE", "Clothing, Shoes & Accessories"),
    ("COL", "Collectibles"),
    ("CEL", "Consumer Electronics"),
    ("CFT", "Crafts"),
    ("HNG", "Home & Garden"),
    ("MTR", "Motors"),
    ("PTS", "Pet Supplies"),
    ("SPT", "Sporting Goods"),
    ("SPM", "Sports Mem, Cards & Fan Shop"),
    ("TNH", "Toys & Hobbies"),
    ("ATQ", "Antiques"),
    ("CNN", "Computers/Tablets & Networking"),
]


class NewListingForm(forms.Form):
    title = forms.CharField(max_length=64)
    description = forms.CharField(widget=forms.Textarea, max_length=400)
    starting_bid = forms.DecimalField(min_value=0.10)
    img_url = forms.URLField(
        label='The URL of an image of your item', required=False)
    category = forms.ChoiceField(choices=categories)
