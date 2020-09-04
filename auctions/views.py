from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User,Bid,Comment,Listing,Watchlist

class ListingForm(forms.Form):
    user=User
    title = forms.CharField(max_length=64)
    description = forms.CharField(max_length=256)
    starting_bid = forms.IntegerField()
    image_url = forms.URLField(max_length=200)
    category = forms.CharField(max_length=64)

def close_listing(listing_param):
    listings_obtained = Listing.objects.get(pk=listing_param[0].pk)
    listings_obtained.active = False
    listings_obtained.save()

def place_bid(bid, user, listing_param):
    listings_obtained = Listing.objects.get(pk=listing_param[0].pk)

    if bid > listings_obtained.price:
        new_bid = Bid()
        new_bid.user = user
        new_bid.amount = bid
        new_bid.listing = listings_obtained
        new_bid.save()

        listings_obtained.price = bid
        listings_obtained.save()
        return 0
    else:
        return 1

def add_comment(user, comment, listing_param):
    comment_obtained = Comment(user=user, listing=listing_param[0], comments=comment)
    comment_obtained.save()

def get_winning_bid(listing_param):
    bids_obtained = Bid.objects.all().filter(listing=listing_param[0])
    winning_bid = bids_obtained.last()
    return winning_bid

def watchlist_list(user, listing_param):
    try:
        watch_list=Watchlist.objects.get(user=user)
    except (UnboundLocalError, Watchlist.DoesNotExist):
        watch_list = Watchlist()
        watch_list.user = user
        watch_list.save()

    watchlist_listing = Watchlist.objects.filter(user=user, listing=listing_param[0])
    watched = bool(watchlist_listing)

    if watched:
        watch_list.listing.remove(Listing.objects.get(pk=listing_param[0].pk))
    else:
        watch_list.listing.add(Listing.objects.get(pk=listing_param[0].pk))



def index(request):
    active_listings = Listing.objects.all().filter(active=True)
    return render(request, "auctions/index.html",{
    "listings":active_listings
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

@login_required(login_url = "login")
def create(request):
    if request.method=="POST":
        listings_obtained = Listing()
        listings_obtained.user = User.objects.get(username=request.user)
        listings_obtained.title = request.POST["title"]
        listings_obtained.description = request.POST["description"]
        listings_obtained.starting_bid = request.POST["starting-bid"]
        listings_obtained.price = listings_obtained.starting_bid
        listings_obtained.image_url = request.POST["url"]
        listings_obtained.category = request.POST["category"]
        listings_obtained.active = True
        listings_obtained.save()
        return HttpResponseRedirect(reverse("index"))

    return render(request,"auctions/create.html")


def listing(request,listing_id):
        watched=False
        owner=False
        winning_bid=False
        user=request.user
        listings_obtained=Listing.objects.filter(pk=listing_id)
        comments = Comment.objects.filter(listing=listings_obtained[0])

        if request.user.is_authenticated:
            user=User.objects.get(username=request.user)

        try:
            owner = bool(Listing.objects.get(user=user, pk=listings_obtained[0].pk))
        except Listing.DoesNotExist:
            owner = False

        if request.method == "POST":
            if "close" in request.POST:
                close_listing(listings_obtained)
                return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))

            if "bid" in request.POST:
                if request.POST["bid"] == "":
                    messages.add_message(request, messages.ERROR, "Please place a bid",extra_tags="bid")
                    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))
                bid=int(request.POST["bid"])
                if place_bid(bid, user, listings_obtained) == 0:
                    messages.add_message(request, messages.SUCCESS, "Bid Placed!" ,extra_tags="bid")
                    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))
                else:
                    messages.add_message(request, messages.ERROR, "Please put a higher bid", extra_tags="bid")
                    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))

            if "comment" in request.POST:
                comment=request.POST["comment"]
                add_comment(user,comment,listings_obtained)
                return HttpResponseRedirect(reverse ("listing", kwargs={"listing_id": listing_id}))

            if "watch" in request.POST:
                watchlist_list(user, listings_obtained)
                return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))

        if not listings_obtained[0].active:
            winning_bid = get_winning_bid(listings_obtained)

        return render(request,"auctions/listing.html",{
            "listing": listings_obtained[0],
            "comments":comments,
            "user": user,
            "owner":owner,
            "winner":winning_bid

        },
    )



def watchlist_action(request, listing_id):

    user = request.user
    list = Listing.objects.filter(id = listing_id).first()
    w = Watchlist.objects.filter(user = user, listing = list).first()

    if w is None:
        wl = Watchlist.objects.create(user = user, listing = list)
        wl.save()
        return HttpResponseRedirect(reverse("watchlist"))

    w.delete()
    return HttpResponseRedirect(reverse("watchlist"))

@login_required(login_url="login")
def watchlist(request):
    user = request.user
    wl = Watchlist.objects.filter(user = user)


    return render(request, "auctions/watchlist.html",{
        "watchlist": wl
    })


def categories(request):
    l = []
    li = Listing.objects.all()

    for listing in li:
        if listing.category:
            if listing.category not in l:
                l.append(listing.category)

    return render(request, "auctions/categories.html", {"categories": l})

def category_list(request, category):
    listings = Listing.objects.all().filter(category=category)
    return render(request, "auctions/category_list.html",
        {"Listings": listings

        })
