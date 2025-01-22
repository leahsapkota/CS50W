from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create_listing", views.createListing, name="create_listing"),
    path("displayCategory", views.displayCategory, name="displayCategory"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("addWatchlist/<int:id>", views.addWatchlist, name="addWatchlist"),
    path("deleteWatchlist/<int:id>", views.deleteWatchlist, name="deleteWatchlist"),
    path("watchlist", views.showWatchlist, name="watchlist"),
    path("AddComment/<int:id>", views.AddComment, name="AddComment"),
    path("addBid/<int:id>", views.addBid, name="addBid"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("closeAuction/<int:id>", views.closeAuction, name = "closeAuction"),
]
