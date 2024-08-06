from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Max
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse

from .forms import UserRegistrationForm, AuctionListingForm, BidForm, CurrentHighestBidForm, CommentForm
from .models import AuctionListings, Bid, Watchlist, Comment

User = get_user_model()

def index(request):
    listing_preview = AuctionListings.objects.all().order_by("-time_date_end")[:8]
    return render(request, "auctions/index.html", {"listing_preview": listing_preview})

def search_category(request):
    if request.method == "POST":
        search_query = request.POST.get('search_query', '')
        search_result = AuctionListings.objects.filter(category__icontains = search_query)
        return render(request, 'auctions/search_category.html', {
            "search_result": search_result, "search_query": search_query
            })  
    else:
        return redirect('index')
        
@login_required
def listing_page(request, id):
    auction_listing = get_object_or_404(AuctionListings, pk=id)
    comments = Comment.objects.filter(auction_listing=auction_listing).order_by('-comment_time')
    
    if request.method == 'POST':
        # For placing new bid
        # Update the current highest bid in the auction listing
        if 'place_bid' in request.POST:
            current_price = 0
            current_price = auction_listing.current_highest_bid
            new_price = current_price + auction_listing.bid_amount
            auction_listing.current_highest_bid = new_price
            
            # Set the latest bidder
            last_bidder = ""
            if current_price == 0:
                auction_listing.last_bidder = auction_listing.seller
            else:
                auction_listing.last_bidder = request.user
            auction_listing.save()
            return redirect('listing_page', id=auction_listing.id)
        
        # For making new comment
        if 'add_comment' in request.POST:        
            comment_form = CommentForm(request.POST) 
            if comment_form.is_valid():
                new_form = comment_form.save(commit=False)
                new_form.auction_listing = auction_listing
                new_form.user = request.user
                new_form.save()
                return redirect('listing_page', id=auction_listing.id)
            else:
                messages.error(request, "Invalid input.")
    else:
        comment_form = CommentForm()
    
    return render(request, 'auctions/listing_page.html', {
        'listing': auction_listing,
        'comment_form': comment_form, # Pass the comment form
        'comments': comments, # Pass the comment
    })
  
@login_required
def create_listing(request):
    if request.method == 'POST':
        form = AuctionListingForm(request.POST, request.FILES)
        bid_form = BidForm(request.POST)
        if form.is_valid():
            auction_listing = form.save(commit=False)
            auction_listing.seller = request.user  # Set the seller to the current user
            auction_listing.save()
            
            return redirect('index')
    else:
        form = AuctionListingForm()
    
    return render(request, 'auctions/create_listing.html', {'form': form,})

# the second page of creating list (adding bid value), not to be confused with bidding higher
# def place_bids(request, listing_id):
    auction_listing = get_object_or_404(AuctionListings, pk=listing_id)
    
    if request.method == 'POST':
        bid_form = BidForm(request.POST)
        if bid_form.is_valid():
            new_bid = bid_form.save(commit=False)
            new_bid.auction_listing = auction_listing
            new_bid.bidder = request.user
            new_bid.save()
            return redirect('index')
    else:
        bid_form = BidForm()
        
    return render(request, 'auctions/place_bids.html', {'bid_form': bid_form, 'listing': auction_listing})

@login_required
def listing_is_open(request, id):
    auction_listing = get_object_or_404(AuctionListings, pk=id)
    
    if request.method == 'POST':
        if request.user == auction_listing.seller:
            if auction_listing.listing_is_open == True: 
                auction_listing.listing_is_open = False
            else:
                auction_listing.listing_is_open = True
            auction_listing.save()
            return redirect('listing_page', id=auction_listing.id)
    else:
        return render(request, 'auctions/listing_page.html', {'listing':auction_listing})

@login_required
def add_to_watchlist(request, id):
    listing = get_object_or_404(AuctionListings, pk=id)
    Watchlist.objects.create(user=request.user, auction_listing=listing)
    
    return redirect('view_watchlist')

@login_required
def remove_from_watchlist(request, id):
    listing = get_object_or_404(AuctionListings, pk=id)
    Watchlist.objects.filter(user=request.user, auction_listing=listing).delete()
    return redirect('view_watchlist')

@login_required
def view_watchlist(request):
    watchlist_items = Watchlist.objects.filter(user=request.user)
    
    return render(request, 'auctions/watchlist.html', {'watchlist_items': watchlist_items})
    
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

#@login_required
#def listing_comment(request, id):
    auction_listing = get_object_or_404(AuctionListings, pk=id)
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_form = comment_form.save(commit=False)
            new_form.auction_listing = auction_listing
            new_form.bidder = request.user
            new_form.save()
            return redirect('listing_page', id=auction_listing.id)
    else:
        bid_form = CommentForm()
        
    return render(request, 'auctions/listing_page.html', {'comment_form': comment_form, 'listing': auction_listing})
        
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

