from django.urls import path

from . import views

app_name = "auctions"

urlpatterns = [
    path("", views.index, name="index"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("categories", views.categories, name="categories"),
    path("category/<str:category>", views.category, name="category"),
    path("listing/new", views.new_listing, name="new_listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("watchlist/toggle/<int:listing_id>",
         views.watchlist_toggle, name="watchlist_toggle"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
