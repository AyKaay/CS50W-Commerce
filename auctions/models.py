from django.contrib.auth.models import AbstractUser
from django.db import models

# Model No.1
class User(AbstractUser):
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username

# Model No.2
class AuctionListings(models.Model):
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=64, blank=False, null=False)
    bid_amount = models.FloatField(blank=False)
    #bid_time = models.DateTimeField(default="timezone.now")
    buy_price = models.FloatField(blank=False)
    category = models.CharField(max_length=24, null=True)
    current_highest_bid = models.FloatField(blank=True, null=True) # THIS
    description = models.TextField(blank=False, null=False)
    image = models.FileField(upload_to="uploads/")
    listing_is_open = models.BooleanField(default=True)
    terms_and_condition = models.TextField(blank=True)
    time_date_end = models.DateTimeField(blank=False, null=False)
    starting_bid = models.FloatField(blank=False)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    last_bidder = models.CharField(max_length=64, blank=True, default="Tav"),
    def __str__(self):
        return self.title
    
# Model No.3
class Bid(models.Model):    
    id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=64, blank=False, null=False, default="untitled")  # Populated from AuctionListings.title
    auction_listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    starting_bid = models.FloatField(blank=False, null=False)
    bid_amount = models.FloatField(blank=False, null=False)
    buy_price = models.FloatField(blank=False, null=False)
    bid_time = models.DateTimeField(auto_now_add=True)
    #current_highest_bid = models.FloatField(blank=True, null=True)
    def __str__(self):
        return self.title

# Model No.4
class Comment(models.Model):
    id = models.BigAutoField(primary_key=True)
    auction_listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.TextField(blank=True)
    comment_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title

# Model No.5   
class Watchlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    auction_listing = models.ForeignKey(AuctionListings, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title