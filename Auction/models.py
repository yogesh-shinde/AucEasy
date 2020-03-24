from django.db import models
from Product.models import ProductInformation
from User.models import User

# Create your models here.


class AuctionDetails(models.Model):
    auctiondetails_id = models.AutoField(primary_key=True)
    auctiondetails_date = models.DateTimeField()
    productinformation = models.ForeignKey(
        ProductInformation, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.productinformation.productinformation_name}'


class CurrentAuction(models.Model):
    currentauction_id = models.AutoField(primary_key=True)
    auctiondetails = models.OneToOneField(AuctionDetails, models.DO_NOTHING)

    def __str__(self):
        return f'{self.auctiondetails.productinformation.productinformation_name}'


class Bidder(models.Model):
    bidder_id = models.AutoField(primary_key=True)
    bidder_type = models.CharField(max_length=36)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.bidder_id}'

    

class AutoBid(models.Model):
    autobid_id = models.AutoField(primary_key=True)
    starting_price = models.FloatField()
    increment_price_by = models.FloatField()
    ending_price = models.FloatField()
    bidder = models.ForeignKey(Bidder, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.autobid_id}'


class CurrentBid(models.Model):
    currentbid_id = models.AutoField(primary_key=True)
    currentbid_time = models.TimeField()
    currentbid_amount = models.FloatField()
    # currentbid_bidderprice = models.FloatField()
    currentauction = models.ForeignKey(
        CurrentAuction, on_delete=models.CASCADE)
    bidder = models.ForeignKey(Bidder, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.currentbid_id}'
