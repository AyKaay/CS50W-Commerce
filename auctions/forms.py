from django import forms 
from .models import AuctionListings, Bid, User, Comment
from django.contrib.auth import get_user_model

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password_confirm = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'password_confirm']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password != password_confirm:
            raise forms.ValidationError("Passwords do not match")

# To create a new listing.
class AuctionListingForm(forms.ModelForm):
    time_date_end = forms.DateTimeField(widget=forms.TextInput(attrs={
        'id': 'default-datepicker',
        'type': 'text',
        'placeholder': 'Select date'
    }))
    class Meta:
        model = AuctionListings
        fields = ['title', 'image', 'time_date_end', 'description', 'category',
                  'starting_bid', 'bid_amount', 'buy_price']

    def save(self, commit=True):
        auction_listing = super().save(commit=False)
        if commit:
            auction_listing.save()
            Bid.objects.create(
                auction_listing=auction_listing,
                bidder=auction_listing.seller,  # Assuming the seller is the initial bidder
                starting_bid=self.cleaned_data['starting_bid'],
                bid_amount=self.cleaned_data['bid_amount'],
                buy_price=self.cleaned_data['buy_price']
            )
        return auction_listing

# Add initial bidding value while creating a listing    
class BidForm(forms.ModelForm):
    starting_bid = forms.FloatField(required=True)
    bid_amount = forms.FloatField(required=True)
    buy_price = forms.FloatField(required=True)

    class Meta:
        model = Bid
        fields = ['starting_bid', 'bid_amount', 'buy_price']

# To bid price in listing_page. Nevermind the current classes name    
class CurrentHighestBidForm(forms.ModelForm):
    current_highest_bid = forms.FloatField(label="Place your bid")
    class Meta:
        model = Bid
        fields = ['current_highest_bid']
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment_text']