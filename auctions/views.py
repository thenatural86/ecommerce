from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import User, Listing, Watchlist


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })

# view details about a particular listing


@login_required
def listing(request, listing_id):
    item = Listing.objects.get(id=listing_id)
    added = Watchlist.objects.filter(
        listingid=listing_id, user=request.user.username)
    print("listing view", item)
    return render(request, "auctions/listing.html", {
        "item": item,
        "added": added
    })

# add/remove items to/from watchlist
# take in request and listing id


def watch(request, listing_id):
    watch = Watchlist()
    watch.user = request.user.username
    watch.listingid = listing_id
    watch.save()
    watching = Watchlist.objects.filter(
        id=listing_id, user=request.user.username)
    return HttpResponseRedirect(reverse("index"))


def remove_watch(request, listing_id):
    watch = Watchlist.objects.filter(
        listingid=listing_id, user=request.user.username)
    if watch:
        watch.delete()
    item = Listing.objects.get(id=listing_id)
    added = Watchlist.objects.filter(
        listingid=listing_id, user=request.user.username)
    print("REMOVE WATCH", item)
    return render(request, "auctions/listing.html", {
        "item": item,
        "added": added
    })


def watchlist(request, user):
    watchlist = Watchlist.objects.filter(user=user)
    items = []
    for item in watchlist:
        items.append(Listing.objects.filter(id=item.listingid))
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist,
        "items": items

    })


def create_listing(request):
    # if post request
    if request.method == "POST":
        # create a Listing object and save to var named item
        item = Listing()
        # pull data from form filled out by user and use as values for object
        item.title = request.POST["title"]
        item.description = request.POST["description"]
        item.price = request.POST["price"]
        item.image = request.POST["image"]
        item.category = request.POST["category"]
        # save to db
        item.save()
        # save all listing to items
        items = Listing.objects.all()
        # print()
        return render(request, "auctions/index.html", {
            "listings": items
        })
    return render(request, "auctions/create_listing.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
