from django.db import models
from Auction.models import *

# Create your models here.

class SuccessReport(models.Model):
    successreport_id=models.AutoField(primary_key=True)
    auctiondetails=models.ForeignKey(AuctionDetails,on_delete=models.CASCADE)
    currentbid=models.ForeignKey(CurrentBid,models.DO_NOTHING)

    def __str__(self):
        return self.successreport_id

class CancelReport(models.Model):
    cancelreport_id=models.AutoField(primary_key=True)
    cancelreport_date=models.DateTimeField()
    cancelreport_reason=models.TextField()
    auctiondetails=models.ForeignKey(AuctionDetails,on_delete=models.CASCADE)

    def __str__(self):
        return self.cancelreport_id

class AuctionQuery(models.Model):
    auctionquery_id=models.AutoField(primary_key=True)
    user_query=models.TextField()
    successreport=models.ForeignKey(SuccessReport,on_delete=models.CASCADE)

    def __str__(self):
        return self.auctionquery_id