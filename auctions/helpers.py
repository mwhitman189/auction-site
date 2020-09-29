from django.utils.encoding import force_text
from .models import AuctionListing
from django.contrib import messages

# Get list of listing categories for converting DB value to string
choices = dict(AuctionListing._meta.get_field('category').flatchoices)


def getFullText(categories):
    """Get full text name of category / categories"""

    if type(categories) is str:
        category_full = force_text(choices[categories], strings_only=True)
        return category_full
    else:
        for entry in categories:
            entry['category_full'] = force_text(
                choices[entry['category']], strings_only=True)
        return categories
