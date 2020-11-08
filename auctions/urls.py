from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create_listing, name="create_listing"),
    path("listing/<int:listing_id>", views.listing, name="listing"),
    path("watch/<int:listing_id>", views.watch, name="watch"),
    path("remove/<int:listing_id>", views.remove_watch, name="remove"),
    path("watchlist/<str:user>", views.watchlist, name="watchlist"),
    path("close_bid/<int:listing_id>", views.close_bid, name="close_bid"),
    path("comment/<int:listing_id>", views.comment, name="comment"),
    path("categories", views.categories, name="categories"),
    path("goto_category/<str:category>",
         views.goto_category, name="goto_category")
]
