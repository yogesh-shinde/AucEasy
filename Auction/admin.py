from django.contrib import admin
from Auction.models import *
# Register your models here.

admin.site.register(AuctionDetails)
admin.site.register(CurrentAuction)
admin.site.register(Bidder)
admin.site.register(AutoBid)
admin.site.register(CurrentBid)
