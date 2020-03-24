from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from Auction.models import *
from Auction.forms import *
from datetime import datetime, date, time
from datetime import timedelta
from django.utils import timezone
from django.core import validators
from Product.models import *
from django.contrib import messages
from Admin.admin_decorator import admin_login
from User.decorator import user_login
import copy

# Create your views here.


class Auction_Details(View):
    @admin_login
    def get(self, request):
        # print('Hello')
        aname = request.session.get('admin')
        objAuction = AuctionDetails.objects.all()
        return render(request, 'details_auction.html', {'admin': aname, 'objAuction': objAuction})


class AddAuction(View):
    objCurrent = AuctionDetails.objects.all()
    currentForm = CurrentAuctionForm()

    def get(self, request):
        aname = request.session.get('admin')
        return render(request, 'add_auction.html', {'admin': aname, 'objCurrent': self.objCurrent, 'currentForm': self.currentForm})

    def post(self, request):
        currentForm = CurrentAuctionForm(request.POST)
        try:
            if (currentForm.is_valid()):
                auction = currentForm.cleaned_data['auctiondetails']
                currentForm.save()
                messages.success(request, 'Your product is add successfully!')
                return redirect('/auction/current-auction/')
        except ObjectDoesNotExist:
            messages.error(request, 'The give input id wrong')
        except Exception:
            print(e)
        return redirect('/auction/add-auction/')


class Upcoming_Auction(View):
    now = datetime.now()
    objAuction = AuctionDetails.objects.filter(
        auctiondetails_date__gt=datetime.now())
    date = None
    if objAuction:
        date = objAuction[0].auctiondetails_date
        product = objAuction[0].productinformation
        images = product.productimages_set.all()

    def calculate_dates(self, date, now):
        if date:
            delta = datetime(now.year, date.month, date.day)
            days = (delta - now).days
            return days

    def get(self, request):
        name = request.session.get('admin')
        uname = request.session.get('uname')
        if name:
            return render(request, 'upcoming_auction.html', {'admin': name, 'objAuction': self.objAuction, 'date': self.calculate_dates(self.date, self.now)})
        elif uname:
            return render(request, 'User/upcoming_auction_user.html', {'user': uname, 'objAuction': self.objAuction, 'date': self.calculate_dates(self.date, self.now)})
        else:
            return render(request, 'User/upcoming_auction_guest.html', {'objAuction': self.objAuction, 'date': self.calculate_dates(self.date, self.now)})


class Current_Auction(View):
    objAuction = CurrentAuction.objects.all()
    bidList = []
    amount = []
    is_seller = []

    cform = CurrentBidForm

    def get(self, request, *arg):
        self.bidList.clear()
        self.amount.clear()
        form = self.cform()

        for obj in self.objAuction:
            if obj.auctiondetails.productinformation.user.user_id == request.session.get('uid'):
                self.is_seller.append(True)
            else:
                self.is_seller.append(False)
        self.is_seller_copy = copy.copy(self.is_seller)

        for obj in self.objAuction:
            currentbid = obj.currentbid_set.all().last()
            if currentbid:
                bidder = currentbid.bidder
                amount = bidder.currentbid_set.all().last()
                self.amount.append(amount.currentbid_amount)
                self.bidList.append(bidder)
            else:
                self.amount.append(None)
                self.bidList.append(None)
        data = zip(self.objAuction, self.bidList,
                   self.amount, self.is_seller_copy)
        # print(self.bidList)
        del self.is_seller[:]

        aname = request.session.get('admin')
        uname = request.session.get('uname')
        if aname:
            return render(request, 'current_auction.html', {'admin': aname, 'data': data, 'form': form})
        elif uname:
            return render(request, 'User/current_auction_user.html', {'user': uname, 'data': data, 'form': form})
        else:
            return render(request, 'User/current_auction_guest.html', {'data': data, 'form': form})


class Product_Details(View):
    @admin_login
    def get(self, request, id):
        auctionobj = AuctionDetails.objects.get(auctiondetails_id=id)
        return render(request, 'details_product.html', {'product': auctionobj})


class AddToAuctionView(View):
    Form = AuctionDetailsForm
    template_name = 'add_to_auction.html'

    def get(self, request, *args, **kwargs):
        pid = kwargs.get('pid')
        form = self.Form()
        prod = ProductInformation.objects.get(productinformation_id=pid)
        aname = request.session.get('admin')
        return render(request, self.template_name, context={'admin': aname, 'form': form, 'prod': prod})

    def post(self, request, *args, **kwrags):
        pid = kwrags.get('pid')
        form = self.Form(request.POST)
        prod = ProductInformation.objects.get(productinformation_id=pid)
        try:

            if form.is_valid():
                auctiondate = form.cleaned_data.get('auctiondate')
                today = date.today()
                if auctiondate <= today:
                    messages.warning(request, "Please enter upcoming date!")
                    return render(request, self.template_name, context={'form': form, 'prod': prod})
                else:
                    auction = AuctionDetails()
                    auction.productinformation = prod
                    auction.auctiondetails_date = auctiondate
                    auction.save()
                    messages.success(
                        request, "Product added to auctiondetails!")
                return redirect('/auction/add-auction/')
            return render(request, self.template_name, context={'form': form, 'prod': prod})
        except ObjectDoesNotExist:
            messages.error(request, 'The give input id wrong')
        except Exception:
            print(e)


class Current_Bid(View):
    @user_login
    def post(self, request, *args, **kwargs):
        id = kwargs.get('cid')
        # base_price=ProductInformation.objects.get()
        objCurrent = CurrentAuction.objects.get(currentauction_id=id)
        base_price = objCurrent.auctiondetails.productinformation.productinformation_baseprice
        print(base_price)
        lastbid = objCurrent.currentbid_set.all().last()
        print(lastbid)
        lastbid_amount = lastbid.currentbid_amount
        currentForm = CurrentBidForm(request.POST)
        if currentForm.is_valid():
            today = datetime.now()
            current_time = today.strftime('%H:%M:%S')
            amount = currentForm.cleaned_data.get('bid_amount')
            if amount > lastbid_amount:
                uid = request.session.get('uid')
                uname = request.session.get('uname')

                bidd = None
                try:
                    user = User.objects.filter(
                        user_id=uid, user_username__exact=uname).last()
                    print(user)
                    bidd = user.bidder_set.all().last()
                except Bidder.DoesNotExist:
                    bidd = Bidder()
                    bidd.bidder_type = 'manaual'
                    user = User.objects.get(user_id=uid, user_username=uname)
                    print(user)
                    bidd.user = user
                    bidd.save()

                finally:
                    objBid = CurrentBid()
                    objBid.currentbid_time = current_time
                    objBid.currentbid_amount = amount
                    objBid.bidder = bidd
                    objBid.currentauction = objCurrent
                    objBid.save()
                    return redirect('/auction/current-auction/')
        messages.error(
            request, "Please enter amount greater than last bid amount")
        return redirect('/auction/current-auction/')
