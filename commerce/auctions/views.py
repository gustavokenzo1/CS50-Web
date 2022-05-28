from cmath import log
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Auction, Bid, Comment, Watchlist


class CreateForm(forms.Form):
    title = forms.CharField(label="Title", max_length=100)
    description = forms.CharField(label="Description", max_length=500)
    starting_bid = forms.DecimalField(
        label="Starting Bid", max_digits=10, decimal_places=2)
    image = forms.CharField(label="Image", required=False)
    category = forms.ChoiceField(label="Category", choices=[("None", "None"),
                                                            ("Fashion", "Fashion"),
                                                            ("Toys", "Toys"),
                                                            ("Electronics",
                                                             "Electronics"),
                                                            ("Home", "Home"),
                                                            ("Other", "Other"), ])


class PlaceBidForm(forms.Form):
    bid = forms.DecimalField(
        label="Place Bid", max_digits=10, decimal_places=2)


class CreateCommentForm(forms.Form):
    comment = forms.CharField(label="Comment", max_length=500)


class SelectCategoryForm(forms.Form):
    category = forms.ChoiceField(label="Category", choices=[
        ("Select Category", "Select Category"),
        ("Fashion", "Fashion"),
        ("Toys", "Toys"),
        ("Electronics",
         "Electronics"),
        ("Home", "Home"),
        ("Other", "Other"), ],)


def index(request):
    if request.method == "POST":
        category = request.POST["category"]

        if category == "Select Category":
            auctions = Auction.objects.all()
        else:
            auctions = Auction.objects.filter(category=category)

        return render(request, "auctions/index.html", {
            "auctions": auctions,
            "categories": SelectCategoryForm()

        })

    return render(request, "auctions/index.html", {
        "auctions": Auction.objects.all(),
        "categories": SelectCategoryForm()
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


def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        starting_bid = request.POST["starting_bid"]
        image = request.POST["image"]
        category = request.POST["category"]
        user = request.user

        auction = Auction(title=title, description=description,
                          starting_bid=starting_bid, image=image,
                          category=category, user=user)
        auction.save()

        return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create.html", {
        "form": CreateForm()
    })


def item(request, item_id):
    listing = Auction.objects.get(id=item_id)
    user = request.user

    watchlist = []
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(
            user=request.user, auction=listing)

    context = {
        "listing": listing,
        "watchlist": watchlist,
        "placeBidForm": PlaceBidForm(),
        "createCommentForm": CreateCommentForm(),
    }

    if user == listing.user:
        context["edit"] = True

    if request.method == "POST":
        if request.POST["action"] == "End Auction":
            listing.is_active = False
            bids = Bid.objects.filter(auction=listing)

            for bid in bids:
                if bid.price == listing.current_price:
                    listing.winner = bid.user.username

            listing.save()
            context["winner"] = listing.winner

            return render(request, "auctions/item.html", context)

        elif request.POST["action"] == "Comment":
            comment = request.POST["comment"]

            comment = Comment(text=comment, auction=listing, user=user)
            comment.save()

            context["comments"] = Comment.objects.filter(auction=listing)
            return render(request, "auctions/item.html", context)

        else:
            bid = float(request.POST["bid"])
            auction = Auction.objects.get(id=item_id)

            if bid < auction.starting_bid:
                context["message"] = "Bid must be greater than starting bid."

                return render(request, "auctions/item.html", context)
            elif bid <= auction.current_price:
                context["message"] = "Bid must be greater than current price."

                return render(request, "auctions/item.html", context)
            else:
                newBid = Bid(price=bid, user=user, auction=auction)
                newBid.save()
                auction.current_price = newBid.price
                auction.save()

                listing = Auction.objects.get(id=item_id)
                context["listing"] = listing

                return render(request, "auctions/item.html", context)

    context["comments"] = Comment.objects.filter(auction=listing)

    return render(request, "auctions/item.html", context)


def watchlist(request):
    if request.method == "POST":
        item_id = 0

        try:
            item_id = request.POST["add_listing_id"]

            listing = Auction.objects.get(id=item_id)
            user = request.user

            watchlist = Watchlist(user=user, auction=listing)
            watchlist.save()
        except:
            item_id = request.POST["remove_listing_id"]

            listing = Auction.objects.get(id=item_id)
            user = request.user

            watchlist = Watchlist.objects.get(user=user, auction=listing)
            watchlist.delete()

        return render(request, "auctions/item.html", {
            "listing": listing,
            "watchlist": Watchlist.objects.filter(user=user, auction=listing),
        })

    auctions = Auction.objects.all()
    watchlist = Watchlist.objects.filter(user=request.user)

    listings = []
    for item in auctions:
        if item.id in [watchlist.auction.id for watchlist in watchlist]:
            listings.append(item)

    return render(request, "auctions/watchlist.html", {
        "auctions": listings
    })
