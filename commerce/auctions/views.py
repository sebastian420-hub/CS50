from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Bid, Comment
from django import forms


class NewListingForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'placeholder': 'Enter the title', 'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}) )
    starting_bid = forms.DecimalField(label="Starting Bid", widget=forms.NumberInput(attrs={'placeholder': 'Enter the starting bid', 'class': 'form-control'}))
    image_url = forms.URLField(label="Image URL", required=False, widget=forms.URLInput(attrs={'placeholder': 'Enter the image URL', 'class': 'form-control'}))
    category = forms.CharField(label="Category", required=False, widget=forms.TextInput(attrs={'placeholder': 'Enter the category', 'class': 'form-control'}))

class NewBidForm(forms.Form):
    bid = forms.DecimalField(label="Bid", widget=forms.NumberInput(attrs={'placeholder': 'Enter your bid', 'class': 'form-control'}))

class NewCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control'})
        }

def index(request):
    listings = Listing.objects.filter(active=True)
    closed_listings = Listing.objects.filter(active=False)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "closed_listings": closed_listings,
        "boolean": True if listings.exists() else False,
        "closed_boolean": False if closed_listings == None else True,
        
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
            user.is_staff = False
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
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            image_url = form.cleaned_data["image_url"]
            category = form.cleaned_data["category"]
            user = request.user
            listing = Listing(title=title, description=description, starting_bid=starting_bid, image_url=image_url, category=category, user=user)
            listing.save()
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/create.html", {
                "form": form 
            })
    return render(request, "auctions/create.html", {
        "form": NewListingForm()
    })

def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    bids = Bid.objects.filter(listing=listing)
    current_bid = bids.order_by("-bid").first() 
    starting_bid = listing.starting_bid
    highest_bid = current_bid.bid if current_bid else starting_bid
    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(pk=listing_id),
        "bid_form": NewBidForm(),
        "bid_num": bids.count(),
        "highest_bid": highest_bid,
        "comment_form": NewCommentForm(),
        "comments": Comment.objects.filter(listing=listing)
        

    })


def bid(request, listing_id):
    if request.method == "POST":
      if request.user.is_authenticated:
          form = NewBidForm(request.POST)
          if form.is_valid():
            bid = form.cleaned_data["bid"]
            listing = Listing.objects.get(pk=listing_id)
            user = request.user
            if bid > listing.starting_bid:
                bid = Bid(listing=listing, user=user, bid=bid)
                bid.save()
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
            else:
                return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
          else:
            return render(request, "auctions/listing.html", {
                "listing": Listing.objects.get(pk=listing_id),
                "bid_form": form
            })
      else:
          return HttpResponseRedirect(reverse("login"))
    

def category(request, category):
    pass

def watchlist(request, username):
    pass

@login_required(login_url="login")
def comment(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    if request.method == "POST":
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.listing = listing
            comment.save()
            return HttpResponseRedirect(reverse("listing", args=(listing_id,)))
           


def closed(request):
    listing = Listing.objects.filter(active=False)
    return render(request, "auctions/closelisting.html", {
        "listings": listing
    })

def inactive(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    try:
        highest_bid = Bid.objects.filter(listing=listing).order_by("-bid").first()
        highest_bidder = highest_bid.user
        return render(request, "auctions/inactive_view.html", {
        "listing": listing,
        "highest_bid": highest_bid.bid,
        "message": f"Listing closed. Won by {highest_bidder}"
        })
    except AttributeError:
        return render(request, "auctions/inactive_view.html", {
        "listing": listing,
        "message": "No bids"
        })


def close(request, listing_id):
    try:
        listing = Listing.objects.get(pk=listing_id)
        listing.active = False
        listing.save()
        highest_bid = Bid.objects.filter(listing=listing).order_by("-bid").first()
        highest_bidder = highest_bid.user
        closed_listing = Listing.objects.filter(active=False)
        return render(request, "auctions/closelisting.html", {
        "listings": closed_listing,
        "message": f"Listing closed. Won by {highest_bidder}"
        })
    except AttributeError:
        listing = Listing.objects.get(pk=listing_id)
        listing.active = False
        listing.save()
        closed_listing = Listing.objects.filter(active=False)
        return render(request, "auctions/closelisting.html", {
        "listings": closed_listing,
        "message": "No bids"
        })
    

