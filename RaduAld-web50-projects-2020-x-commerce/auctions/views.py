from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.db.models.signals import post_delete
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Watchlist, Bid, Comment, Category


def index(request):
    listings = Listing.objects.filter(active=True).all()
    bids = []
    for item in listings:
        bids.append(Bid.objects.filter(listing_name=item).last())
    return render(request, "auctions/index.html", {
        "listings": listings,
        "bids": bids,
        "title": "Active Listings",
    })

@login_required
def watchlist_page(request):
    user = request.user
    listis = Watchlist.objects.get(user=user)
    listings = listis.watchlist.all()
    return render(request, "auctions/index.html", {
        "listings": listings,
        "title": "Watchlist",
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
        return render(request, "auctions/login.html" )

@login_required
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
            watchlist = Watchlist(user=user)
            watchlist.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_listing(request):
    categories = Category.objects.all()
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        bid = request.POST["bid"]
        image_url = request.POST["image_url"]
        user = request.user
        categories = request.POST["selected_categories"]
        listing = Listing(title=title.capitalize(), description=description, image_url=image_url, user=user, active=True)
        listing.save()
        listing_id = listing.id
        b = Bid(bid=bid, user=user, listing_name=listing)
        b.save()
        return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))
    return render(request, "auctions/create_listing.html", {
        "categories": categories,
    })


def listing(request, listing_id):
    try:
        l = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        return render(request, "auctions/ersuc.html", {
            "message": "Page not found."
        })
    try:
        comments = Comment.objects.filter(listing_name=l).all()
    except:
        comments = None
    user = request.user
    if user == l.user:
        close = True
    else:
        close = False
    highest_bid = Bid.objects.filter(listing_name=l).order_by("bid").last()
    try: 
        Watchlist.objects.get(user=user, watchlist=l)
        wl = True
    except:
        wl = False
    bids_number = Bid.objects.filter(listing_name=l).count()
    bids_number -= 1
    if request.method == "POST":
        button = request.POST["but"]
        try:
            bid = request.POST["bid"]
            if bid != "":
                bid = int(bid)
                if bid <= highest_bid.bid:
                    return render(request, "auctions/listing.html", {
                            "alert": "Please enter a valid bid, higher than the highest bid!",
                            "listing": l,
                            "wl": wl,
                            "close": close,
                            "closed": False,
                            "comments": comments,
                            "highest_bid": highest_bid,
                            "bids_number": bids_number,
                        })
                b = Bid(bid=bid, user=user, listing_name=l)
                b.save()
                highest_bid = b      
                bids_number = Bid.objects.filter(listing_name=l).count()
                bids_number -= 1
                return render(request, "auctions/listing.html", {
                            "alert": "Bid Placed!",
                            "listing": l,
                            "wl": wl,
                            "close": close,
                            "closed": False,
                            "comments": comments,
                            "highest_bid": highest_bid,
                            "bids_number": bids_number,
                        })
            else: 
                if button == "Add to Watchlist":
                    watchlist = Watchlist.objects.get(user=user)
                    watchlist.watchlist.add(l)
                    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))
                if button == "Remove from Watchlist":
                    watchlist = Watchlist.objects.get(user=user)
                    watchlist.watchlist.remove(l)
                    return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))
                if button == "Close Listing":
                    l.active = False
                    l.save()
                    return HttpResponseRedirect(reverse("closed_listing_page", kwargs={"listing_id": listing_id}))
        except:
            text = request.POST["comment"]
            comment = Comment(text=text, user=user, listing_name=l)
            comment.save()
            return HttpResponseRedirect(reverse("listing", kwargs={"listing_id": listing_id}))
    return render(request, "auctions/listing.html", {
        "listing": l,
        "wl": wl,
        "close": close,
        "comments": comments,
        "highest_bid": highest_bid,
        "bids_number": bids_number,
    })


def closed_listings(request):
    closed_listings = Listing.objects.filter(active=False).all()
    return render(request, "auctions/index.html", {
        "listings": closed_listings,
        "title": "Closed Listings",
    })


def closed_listing(request, listing_id):
    try:
        l = Listing.objects.get(id=listing_id)
    except Listing.DoesNotExist:
        return render(request, "auctions/ersuc.html", {
            "message": "Page not found."
        })
    try:
        comments = Comment.objects.filter(listing_name=l).all()
    except:
        comments = None
    user = request.user
    highest_bid = Bid.objects.filter(listing_name=l).order_by("bid").last()
    return render(request, "auctions/listing.html", {
        "listing": l,
        "user": user,
        "comments": comments,
        "highest_bid": highest_bid,
    })


def categories(request):
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories": categories,
    })


def category_page(request, category_id):
    c = Category.objects.get(id=category_id)
    lists = []
    listings = Listing.objects.filter(active=True).all()
    for listing in listings:
        for category in listing.categories.all():
            if category.id == category_id:
                lists.append(listing)
    if lists == []:
        lists = None
    bids = []
    for item in listings:
        bids.append(Bid.objects.filter(listing_name=item).last())
    return render(request, "auctions/index.html", {
        "title": c.categ,
        "listings": lists,
        "bids": bids,
    })
