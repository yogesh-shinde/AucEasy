from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import HttpResponse
import hashlib
from .forms import *
from .models import *
from Auction.forms import CurrentBidForm
from django.contrib import messages, auth
from django.core.mail import send_mail
from django.conf import settings
from Product.models import *
from Auction.models import AuctionDetails, CurrentAuction
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

# view for make password encrypted


def make_password(password):
    assert password
    hash1 = hashlib.md5(password.encode(encoding="utf-8")).hexdigest()
    return hash1

# show only user_base.html


class UserGuest(View):
    objAuction = CurrentAuction.objects.all()
    bidList = []
    amount = []
    cform = CurrentBidForm

    def get(self, request):
        self.bidList.clear()
        self.amount.clear()
        form = self.cform()
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
        data = zip(self.objAuction, self.bidList, self.amount)
        return render(request, 'User/home.html', {'data': data, 'form': form})


class Home(View):
    objAuction = CurrentAuction.objects.all()
    bidList = []
    amount = []
    cform = CurrentBidForm

    def get(self, request):
        uname = request.session.get('uname')
        self.bidList.clear()
        self.amount.clear()
        form = self.cform()
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
        data = zip(self.objAuction, self.bidList, self.amount)

        return render(request, 'User/user_home.html', {'user': uname, 'data': data, 'form': form})

# view for user registration


class UserRegister(View):
    def get(self, request):
        form = PostForm()
        return render(request, 'User/userreg.html', {'form': form})

    def post(self, request):
        form = PostForm(request.POST, request.FILES)
        if (form.is_valid()):
            user_password = form.cleaned_data['user_password']
            user_confirm_password = form.cleaned_data['user_confirm_password']

            if (user_password == user_confirm_password):
                user_password = make_password(user_password)
                user_confirm_password = make_password(user_confirm_password)
                user = User()
                user.user_name = form.cleaned_data['user_name']
                user.user_username = form.cleaned_data['user_username']
                user.user_password = user_password
                user.user_confirm_password = user_confirm_password
                user.user_email = form.cleaned_data['user_email']
                user.user_contact = form.cleaned_data['user_contact']
                user.gender = form.cleaned_data['gender']
                user.idproof_images = form.cleaned_data['idproof_images']
                user.country = form.cleaned_data['country']
                user.state = form.cleaned_data['state']
                user.city = form.cleaned_data['city']
                user.area = form.cleaned_data['area']
                user.save()
                for obj in form.cleaned_data['idproof']:
                    user.idproof.add(obj)
                user.save()
            return redirect('/user/user-login/')
        return render(request, 'User/userreg.html', {'form': form})

# view for user login


class UserLogin(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'User/UserLogin.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        try:
            if form.is_valid():
                username = form.cleaned_data.get('user_username')
                password = form.cleaned_data.get('user_confirm_password')
                password = make_password(password)
                user = User.objects.get(
                    user_username__exact=username, user_confirm_password__exact=password)
                if user is not None:
                    request.session['uname'] = user.user_username
                    request.session['uid'] = user.user_id
                    return redirect('/user/home/')
                else:
                    messages.error(
                        request, 'Please Enter Valid Username and Password')
                    return redirect('/user/user-login/')
        except ObjectDoesNotExist:
            messages.error(
                request, 'Please Enter Valid Username and Password!!')
        except Exception as e:
            messages.error(request, e)
        return redirect('/user/user-login/')

# view for email


def change_pass_email(request):
    if request.method == "POST":
        email = request.POST.get('email')
        # print(email,"***********")
        u = User.objects.get(user_email=email)
        send_mail(subject="test email from vikash", message=f"helooo there \n <a href= 'http://127.0.0.1:8000/user/email/{u.user_id}/ '> click here to change password</a>", recipient_list=["vikashjaka@gmail.com"],
                  from_email=settings.EMAIL_HOST_USER, fail_silently=True)
        # send_mail(subject, message, from_email, recipient_list, fail_silently=False, auth_user=None,
        # auth_password=None, connection=None, html_message=None)[source]¶
        return redirect("/user/user-login/")
    return render(request, "User/email.html")

# view for change password


def change_pass(request, id):
    if request.method == "POST":
        u = User.objects.get(user_id=id)
        u.user_confirm_password = make_password(request.POST.get("password"))
        u.save()
        return redirect("/user/user-login/")
    return render(request, "User/change_password.html", {"id": id})

# view for update user profile


class UserUpdate(View):
    def get(self, request):
        id = request.session.get('uid')
        pobj = User.objects.get(pk=id)
        uname = request.session.get('uname')
        pforms = UserProfile(instance=pobj)
        return render(request, 'user/updateprofile.html', {'pforms': pforms, 'user': uname})

    def post(self, request):
        id = request.session.get('uid')
        pobj = User.objects.get(pk=id)
        pforms = UserProfile(request.POST, request.FILES, instance=pobj)
        if pforms.is_valid():
            pforms.save()
            return redirect('/user/home/')
        # pforms = UserProfile(instance=pobj)
        return render(request, 'user/updateprofile.html', {'pforms': pforms})


class UserDisplayVerify(View):
    def get(self, request):
        uid = request.session.get('uid')
        # information=ProductInformation.objects.filter(user__user_id=uid)
        auctiondetails = ProductInformation.objects.filter(user__user_id=uid)
        # print(auctiondetails)
        uname = request.session.get('uname')
        return render(request, 'user/user_displayverify.html', {'information': auctiondetails, 'user': uname})


# class AboutUsUserLogin(View):
#     def get(self, request):
#         return render(request, 'AcuEasy/user_about_uslogin.html')


class AboutUsUserGuest(View):
    def get(self, request):
        if request.session.get('uname'):
            user = request.session.get('uname')
            return render(request, 'AcuEasy/user_aboutus.html', {'user': user})
        elif request.session.get('admin'):
            admin = request.session.get('admin')
            return render(request, 'AcuEasy/admin_aboutus.html', {'admin': admin})

        else:
            return render(request, 'AcuEasy/aboutus.html')


class ContactUs(View):
    def get(self, request):
        if request.session.get('uname'):
            user = request.session.get('uname')
            return render(request, 'AcuEasy/user_contactus.html', {'user': user})
        elif request.session.get('admin'):
            admin = request.session.get('admin')
            return render(request, 'AcuEasy/admin_contactus.html', {'admin': admin})

        else:
            return render(request, 'AcuEasy/contactus.html')


def logout_view(request):
    auth.logout(request)
    return redirect('/')
