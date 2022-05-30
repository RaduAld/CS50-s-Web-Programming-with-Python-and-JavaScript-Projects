from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("watchlist_page", views.watchlist_page, name="watchlist_page"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("closed_listings", views.closed_listings, name="closed_listings"),
    path("closed_listings/<int:listing_id>", views.closed_listing, name="closed_listing_page"),
    path("categories", views.categories, name="categories"),
    path("categories/<int:category_id>", views.category_page, name="category_page")
]
