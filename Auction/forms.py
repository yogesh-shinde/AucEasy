from django import forms
from Auction.models import *


class AuctionDetailsForm(forms.Form):
    auctiondate = forms.DateField(widget=forms.DateInput(
        attrs={'type': 'date', 'format': '%YY-%MM-%DD'}))
    # class Meta:
    #     model=AuctionDetails
    #     fields=['auctiondate']
    #     #exclude=['productinformation']


class CurrentAuctionForm(forms.ModelForm):
    class Meta:
        model = CurrentAuction
        fields = '__all__'


class BidderForm(forms.ModelForm):
    class Meta:
        model = Bidder
        fields = '__all__'


class AutoBidForm(forms.ModelForm):
    class Meta:
        model = AutoBid
        fields = '__all__'


class CurrentBidForm(forms.Form):
    bid_amount = forms.FloatField()
