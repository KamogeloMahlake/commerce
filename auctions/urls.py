from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create"),
    path("listings/<int:id>", views.listing_page, name="listing"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("categories/<str:title>", views.category, name="category"),
    path("add/<int:id>", views.add_watchlist, name="add"),
    path("remove/<int:id>", views.remove_watchlist, name="remove"),
    path("comment/<int:id>", views.add_comment, name="comment"),
    path("bid/<int:id>", views.bid, name="bid"),
    path("close/<int:id>", views.close_listing, name="close"),
    path("mylistings", views.my_listings, name="mylistings")
]
