from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import *


def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
    })


def create_listing(request):
    if request.method == "POST":
        item = Listing()
        item.title = request.POST["title"]
        item.description = request.POST["description"]
        item.price = request.POST["price"]
        item.image = request.POST["image"]
        item.category = request.POST["category"]
        item.seller = request.user.username
        item.save()
        items = Listing.objects.all()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create_listing.html")


@login_required
def listing(request, listing_id):
    if request.method == "POST":
        item = Listing.objects.get(id=listing_id)
        added = Watchlist.objects.filter(
            id=listing_id, user=request.user.username)
        new_bid = int(request.POST["new_bid"])
        if item.price >= new_bid:
            return render(request, "auctions/listing.html", {
                "item": item,
                "added": added,
                "message": "Bid higher!",
                "msg_type": "danger"
            })
        else:
            item.price = new_bid
            item.active
            item.save()
            old_bid = Bid.objects.filter(listingid=listing_id)
            if old_bid:
                old_bid.delete()
            bid = Bid()
            bid.user = request.user.username
            bid.title = item.title
            bid.listingid = listing_id
            bid.bid = new_bid
            bid.save()
            return render(request, "auctions/listing.html", {
                "item": item,
                "added": added,
                "message": "Successful Bid!",
                "msg_type": "success"
            })
    else:
        comments = Comment.objects.filter(listingid=listing_id)
        item = Listing.objects.get(id=listing_id)
        added = Watchlist.objects.filter(
            listingid=listing_id, user=request.user.username)
    try:
        winner_obj = Winner.objects.get(listingid=listing_id)
        if winner_obj:
            return render(request, "auctions/listing.html", {
                "item": item,
                "added": added,
                "winner": winner_obj,
                "comments": comments,

            })
    except:
        return render(request, "auctions/listing.html", {
            "item": item,
            "added": added,
            "comments": comments,

        })


@login_required
def watch(request, listing_id):
    watch = Watchlist()
    watch.user = request.user.username
    watch.listingid = listing_id
    watch.save()
    item = Listing.objects.get(id=listing_id)
    added = Watchlist.objects.filter(
        listingid=listing_id, user=request.user.username)
    comments = Comment.objects.filter(listingid=listing_id)

    return render(request, "auctions/listing.html", {
        "item": item,
        "added": added,
        "comments": comments,

    })


@login_required
def remove_watch(request, listing_id):
    watch = Watchlist.objects.filter(
        listingid=listing_id, user=request.user.username)
    if watch:
        watch.delete()
    item = Listing.objects.get(id=listing_id)
    added = Watchlist.objects.filter(
        listingid=listing_id, user=request.user.username)
    comments = Comment.objects.filter(listingid=listing_id)

    return render(request, "auctions/listing.html", {
        "item": item,
        "added": added,
        "comments": comments,

    })

    # get the item whose bid is being closed on by getting its id which is the listing_id being passed into this view
    # get the bid that is to be closed via its listingid attr being equal to passed in listing_id
    # fill in winner_obj data via the request, bid_obj and listing_id
    # save this winner obj to db
    # make the listing no longer active.
    # delete listing, bid and watchlist objects


def close_bid(request, listing_id):
    winner_obj = Winner()
    item = Listing.objects.get(id=listing_id)
    bid_obj = Bid.objects.get(listingid=listing_id)
    winner_obj.winner = bid_obj.user
    winner_obj.win_price = bid_obj.bid
    winner_obj.seller = request.user.username
    winner_obj.title = bid_obj.title
    winner_obj.listingid = listing_id
    winner_obj.save()
    watch_obj = Watchlist.objects.filter(listingid=listing_id)
    message = "You won the auction! Well played."
    msg_type = "success"
    item.winner = winner_obj.winner
    item.active = False
    item.save()
    print(winner_obj.winner)
    watch_obj.delete()
    bid_obj.delete()
    return render(request, "auctions/listing.html", {
        "item": item,
        "winner": winner_obj
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


def comment(request, listing_id):
    comment_obj = Comment()
    comment_obj.comment = request.POST.get("comment")
    comment_obj.user = request.user.username
    comment_obj.listingid = listing_id
    comment_obj.save()
    comments = Comment.objects.filter(listingid=listing_id)
    item = Listing.objects.get(id=listing_id)
    added = Watchlist.objects.filter(
        listingid=listing_id, user=request.user.username)
    return render(request, "auctions/listing.html", {
        "comments": comments,
        "item": item,
        "added": added
    })


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
