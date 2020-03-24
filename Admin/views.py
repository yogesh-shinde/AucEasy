from django.shortcuts import render, redirect,HttpResponse, get_object_or_404
from django.views import View
from .models import AdminUser
from Admin.forms import *
from .admin_decorator import admin_login
from django.contrib import messages
from Product.models import *
from Product.views import *
from User.models import *
import hashlib
import requests   #pip install requests
import json
from django.core.exceptions import ObjectDoesNotExist
from Auction.models import *
from Auction.forms import *

# Create your views here.
# admin first page

def make_password(password):
    assert password
    hash1=hashlib.md5(password.encode(encoding="utf-8")).hexdigest()
    return hash1


# class ViewAdmin(View):
#     def get(self,request):
#         return render(request,'AcuEasy/admin_base.html')

class AdminDisplay(View):
    objAuction = CurrentAuction.objects.all()
    bidList = []
    amount = []
    cform = CurrentBidForm

    @admin_login
    def get(self, request):
        aname=request.session.get('admin')
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

        return render(request, 'admin_home.html', {'admin': aname,'data': data, 'form': form})

    # def get(self,request):
    #     aname=request.session.get('admin')
    # return render(request,'AcuEasy/admin_base2.html',{'admin':aname})


class AdminRegistration(View):
    def get(self,request):
        adminform=AdminUserForm()
        return render(request,'admin_register.html',{'adminform':adminform})

    def post(self,request):
        adminform=AdminUserForm(request.POST)
        if adminform.is_valid():
            password=adminform.cleaned_data['admin_password']
            confirmpassword=adminform.cleaned_data['admin_confirm_password']
            if (password==confirmpassword):
                password=make_password(password)
                confirmpassword=make_password(confirmpassword)
                admin=AdminUser()
                admin.admin_name=adminform.cleaned_data['admin_name']
                admin.admin_username=adminform.cleaned_data['admin_username']
                admin.admin_password=password
                admin.admin_confirm_password=confirmpassword
                admin.admin_email=adminform.cleaned_data['admin_email']
                admin.admin_contact=adminform.cleaned_data['admin_contact']
                admin.country=adminform.cleaned_data['country']
                admin.state=adminform.cleaned_data['state']
                admin.city=adminform.cleaned_data['city']
                admin.area=adminform.cleaned_data['area']
                admin.save()
                return redirect ('/admingui/admin-login/')
        else:
            return render(request,'admin_register.html',{'adminform':adminform})


class AdminLogin(View):
    def get(self,request):
        admin_loginform=AdminLoginForm()
        return render(request, 'admin_login.html',{'admin_loginform':admin_loginform})

    def post(self,request,*args,**kwargs):
        admin_loginform=AdminLoginForm(request.POST)
        try:
            if admin_loginform.is_valid():
                adminusername=admin_loginform.cleaned_data.get('admin_username')
                adminpassword=admin_loginform.cleaned_data.get('admin_confirm_password')
                adminpassword=make_password(adminpassword)
                admin=AdminUser.objects.get(admin_username=adminusername,admin_confirm_password=adminpassword)
                if admin is not None:
                    request.session['admin']=admin.admin_username
                    request.session['aid']=admin.admin_id
                    return redirect('/admingui/home/')
                else:
                    messages.error(request,'Please  enter valid username and password')
                    return redirect('/admingui/admin-login/')
        except  ObjectDoesNotExist:
                messages.error(request,'Please Enter Valid Username and Password!!')
        except Exception as e:
                messages.error(request,e)
        return redirect('/admingui/admin-login/')

class AdminUpdate(View):
    @admin_login
    def get(self,request):
        id=request.session.get('aid')
        admin=AdminUser.objects.get(pk=id)
        # admin=get_object_or_404(AdminUser,pk=id)
        adminform=AdminProfile(instance=admin)
        aname=request.session.get('admin')
        return render(request,'admin_update.html',{'adminform':adminform,'admin':aname})
    @admin_login
    def post(self,request):
        id=request.session.get('aid')
        admin=AdminUser.objects.get(pk=id)
        adminform=AdminProfile(request.POST,instance=admin)
        if adminform.is_valid():
            adminform.save()
            return redirect('/admingui/admin-login/')
        # adminform=AdminProfile(instance=admin)
        return render(request,'admin_update.html',{'adminform':adminform})


class PendingVerification(View):
    @admin_login
    def get(self,request):
        information=ProductInformation.objects.filter(product_verify=False)
        aname=request.session.get('admin')
        return render(request,'pending_verification.html',{'information':information,'admin':aname})

class VerifyProduct(View):
    @admin_login
    def get(self,request,*args,**kwargs):
        prod_id=kwargs.get('id')
        # print(prod_id)
        if prod_id:
            messages.success(request,'Product is verified!')
            obj=ProductInformation.objects.get(pk=prod_id)
            obj.product_verify = True
            obj.save()
            return redirect('/admingui/pending-verification/')


class CancelProduct(View):
    @admin_login
    def get(self,request,*args,**kwargs):
        prod_id=kwargs.get('id')
        if prod_id:
            messages.error(request,'Product is canceled!')
            obj=ProductInformation.objects.get(pk=prod_id)
            obj.delete()
            return redirect('/admingui/pending-verification/')

class ProductVerified(View):
    objproduct=ProductInformation.objects.filter(product_verify=True)
    @admin_login
    def get(self,request):
        aname=request.session.get('admin')
        return render(request,'product_verified.html',{'admin':aname,'objproduct':self.objproduct})


# Shilpa Mam Code
 
class AddProductCategory(View):
    def get(self,request):
        categoryform=ProductCategoryForm()
        aname=request.session.get('admin')
        return render (request,'add_category.html',{'admin':aname,'categoryform':categoryform})

    def post(self,request):
        categoryform=ProductCategoryForm(request.POST)
        if categoryform.is_valid():
            categoryform.save()
        return redirect('/admingui/add-subcategory/')

class AddProductSubcategory(View):
    def get(self,request):
        #categoryform=ProductCategory.objects.get(productcategory_id=id)
        subcategoryform=ProductSubcategoryForm()
        aname=request.session.get('admin')
        return render (request,'add_subcategory.html',{'admin':aname,'subcategoryform':subcategoryform})

    def post(self,request):
        #categoryform=ProductCategory.objects.get(productcategory_id=id)
        subcategoryform=ProductSubcategoryForm(request.POST)
        if subcategoryform.is_valid():
            subcategoryform.save()
        return redirect('/admingui/home/')

class AddCountry(View):
    def get(self,request):
        countryform=CountryForm()
        aname=request.session.get('admin')
        return render (request,'add_country.html',{'admin':aname,'countryform':countryform})

    def post(self,request):
        countryform=CountryForm(request.POST)
        if countryform.is_valid():
            countryform.save()
        return redirect(('/admingui/add-state/'))


class AddState(View):
    def get(self,request):
        stateform=StateForm()
        aname=request.session.get('admin')
        return render(request,'add_state.html',{'admin':aname,'stateform':stateform})

    def post(self,request):
       stateform=StateForm(request.POST)
       if stateform.is_valid():
            stateform.save()
       return redirect('/admingui/add-city/')

class AddCity(View):
    def get(self,request):
        cityform=CityForm()
        aname=request.session.get('admin')
        return render(request,'add_city.html',{'admin':aname,'cityform':cityform})

    def post(self,request):
       cityform=CityForm(request.POST)
       if cityform.is_valid():
            cityform.save()
       return redirect('/admingui/add-area/')

class AddArea(View):
    def get(self,request):
        areaform=AreaForm()
        aname=request.session.get('admin')
        return render(request,'add_area.html',{'admin':aname,'areaform':areaform})

    def post(self,request):
       areaform=AreaForm(request.POST)
       if areaform.is_valid():
            areaform.save()
       return redirect('/admingui/home/')



URL = 'https://www.sms4india.com/api/v1/sendCampaign'

# get request
def sendPostRequest(reqUrl, apiKey, secretKey, useType, phoneNo, senderId, textMessage):
  req_params = {
  'apikey':apiKey,
  'secret':secretKey,
  'usetype':useType,
  'phone': phoneNo,
  'message':textMessage,
  'senderid':senderId
  }
  return requests.post(reqUrl, req_params)


def message(request):
    response = sendPostRequest(URL, 'WCFYODN7VQC5I6DLCQCO6I8N1MD49TAK', 'HIWCNELA3GTONXIP', 'stage', '8888673032', 'Vikash', 'hii you have shortlisted for python interview ' )
    """
      Note:-
        you must provide apikey, secretkey, usetype, mobile, senderid and message values
        and then requst to api
    """
    # print response if you want
    return HttpResponse("message sent successfully")
    # print(response.text)
