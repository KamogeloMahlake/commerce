from typing import List
from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Comment, User, Listing, Bid

Categories =  (('Auto', 'Auto'), ('Toys', 'Toys'), ('Electronics', 'Electronics'), ('Fashion', 'Fashion'), ('Home', 'Home'))

class CreateListingForm(forms.Form):
    title = forms.CharField(
        label="Title",
        widget=forms.TextInput(attrs={"class": "form-control-md form-group"}),
    )
    description = forms.CharField(
        label="Description",
        widget=forms.Textarea(
            attrs={
                "class": "form-control-md",
                "rows": "4",
                "cols": "40"
            }),
    )
    starting_bid = forms.FloatField(
        label="Starting Bid",
        widget=forms.NumberInput(
            attrs={
                "class": "form-control-md form-group",
                "value": "1.00",
                "min": "1.00",
                "max": "100000000.00",
            }
        ),
    )
    image_url = forms.URLField(
        label="Image URL(optional)",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control-md form-group"}),
    )

    category = forms.ChoiceField(
        choices= Categories,
        widget=forms.Select(attrs={'class': 'form-control-md'}),
        required=False
        
    )

class CommentForm(forms.Form):
    comment = forms.CharField(
        label="",
        widget=forms.Textarea(
            attrs={"class": "form-control form-group", "placeholder": "Add Comment"}
        ),
    )

class BidForm(forms.Form):
    amount = forms.FloatField(
        label="Enter Bid", 
        widget=forms.NumberInput(
            attrs={
                "class": "form-control-md form-group",
                "style": "margin: 2rem 0.05rem 0 0"
            }
    ))

@login_required
def my_listings(request):
    return render(request, "auctions/index.html", {
        'listings': Listing.objects.filter(user=request.user),
        'title': f"Listings: {request.user.username}"
    })
@login_required
def bid(request, id):
    listing = Listing.objects.get(pk=id)
    form = BidForm(request.POST)

    if form.is_valid():
        amount = float(form.cleaned_data['amount'])

        if listing.current_bid and amount > listing.current_bid:
            bid = Bid.objects.filter(listing=listing)[0]
            bid.user = request.user
            bid.bid = amount
            listing.current_bid = bid.bid
            bid.save()
        
        elif amount > listing.starting_bid:
            bid = Bid(user=request.user, bid=amount, listing=listing)
            listing.current_bid = amount
            bid.save()

        listing.save()

    return HttpResponseRedirect(reverse('listing', kwargs={"id": id}))

@login_required
def close_listing(request, id):
    listing = Listing.objects.get(pk=id)

    if listing.user == request.user and listing.active:
       bid  = Bid.objects.filter(listing=listing)[0]
       listing.active = False 
       
       if bid:
           listing.winner = bid.user
       
       listing.save()
    
    return HttpResponseRedirect(reverse('index'))

def index(request):
    listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {"listings": listings, "title": "Active Listings"})


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required(login_url="auctions/login.html")
def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)

        if form.is_valid():

            try:
                listing = Listing(user=request.user, **form.cleaned_data)
                listing.save()

            except IntegrityError:
                return render(request, "auctions/index.html")
            return HttpResponseRedirect(reverse("index"))

    return render(request, "auctions/create.html", {"form": CreateListingForm()})


def listing_page(request, id):
    listing = Listing.objects.get(pk=id)
    comments = Comment.objects.filter(listing=listing)
    winner = "" if listing.active else f"The auction is closed!"
    watchlist = True if request.user.is_authenticated and listing in request.user.watchlist.all() else False
    if winner and listing.winner == request.user:
        winner += " You are the winner!"
    elif winner and listing.winner != request.user and listing.user != request.user:
        winner += f"The winner is {listing.winner}"

    return render(
        request,
        "auctions/listing.html",
        {"listing": listing, "comment": CommentForm(), "comments": comments, "bid": BidForm(), "watchlist": watchlist, "winner": winner}
    )


@login_required(login_url="auctions/login.html")
def watchlist(request):
    return render(
        request, "auctions/watchlist.html", {"watchlist": request.user.watchlist.all()}
    )


@login_required()
def add_watchlist(request, id):
    listing = Listing.objects.get(pk=id)

    if listing and listing not in request.user.watchlist.all():
        request.user.watchlist.add(listing)

    return HttpResponseRedirect(reverse("watchlist"))


@login_required
def remove_watchlist(request, id):
    listing = Listing.objects.get(pk=id)

    if listing:
        request.user.watchlist.remove(listing)
    return HttpResponseRedirect(reverse("watchlist"))


def categories(request):
    return render(request, "auctions/categories.html", {"categories": [x for x, _ in Categories]})

def category(request, title):
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(category=title),
        "title": f"Category: {title}"
    })

@login_required(login_url="auction/login.html")
def add_comment(request, id):
    if request.method == "POST":
        form = CommentForm(request.POST)

        if form.is_valid():
            comment = form.cleaned_data["comment"]

            c = Comment(
                user=request.user, text=comment, listing=Listing.objects.get(pk=id)
            )
            c.save()

        return HttpResponseRedirect(reverse("listing", kwargs={"id": id}))
    return HttpResponseRedirect(reverse("index"))
