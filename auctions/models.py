from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator
from django.utils import timezone
from django.conf import settings


def return_exp_datetime():
    now = timezone.now()
    return now + timezone.timedelta(days=3)


class User(AbstractUser):
    avatar = models.URLField(blank=True, max_length=400)

    def __str__(self):
        return self.username


class Rating(models.Model):
    evaluator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="evaluator")
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="seller")
    rating = models.DecimalField(
        validators=[MaxValueValidator(5)], max_digits=2, decimal_places=1)

    def __str__(self):
        return f"{self.seller} ({self.rating})"


class AuctionListing(models.Model):
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

    CATEGORY_CHOICES = [
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

    item = models.CharField(max_length=64)
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES)
    starting_bid = models.DecimalField(max_digits=13, decimal_places=2)
    buyout_price = models.DecimalField(max_digits=13, decimal_places=2)
    details = models.TextField(max_length=400)
    img = models.URLField(blank=True, max_length=400)
    expiration = models.DateTimeField(default=return_exp_datetime)
    is_active = models.BooleanField(default=True)
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.item

    def is_valid_listing(self):
        return self.starting_bid < self.buyout_price and self.expiration > timezone.now() and (self.buyout_price and self.starting_bid) > 0


class WatchList(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE)

    def __str__(self):
        return self.listing.item


class Bid(models.Model):
    bidder = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=13, decimal_places=2)
    is_active = models.BooleanField(default=True)
    is_winner = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.bidder} - {self.amount} ({self.listing.id} {self.is_active})"

    def is_valid_bid(self):
        return self.amount > self.listing.starting_bid and not (self.is_winner and self.is_active)


class Comment(models.Model):
    commentor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    listing = models.ForeignKey(
        AuctionListing, on_delete=models.CASCADE)
    comment = models.TextField(max_length=150)
    votes = models.IntegerField()
    timestamp = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.commentor} on {self.listing} at {self.timestamp}"
