from django.shortcuts import render, redirect, get_object_or_404
from Product.models import *
from django.forms import modelformset_factory
from .forms import *
from django.views import View
from django.contrib import messages
from User.decorator import user_login
# Create your views here.


# view for to display product information
class DisplayProduct(View):
    @user_login
    def get(self, request):
        uid=request.session.get('uid')
        user = request.session.get('uname')
        information = ProductInformation.objects.filter(user__user_id=uid)
        return render(request, 'display_product.html', {'information': information,'user':user})

# view for to add new product information


class AddProduct(View):
    @user_login
    def get(self, request):
        imgform = ProductInformationForm()
        uname=request.session.get('uname')
        return render(request, 'add_product.html', {'imgform': imgform,'user':uname})

    def post(self, request):
        if (request.method == 'POST'):
            imgform = ProductInformationForm(request.POST, request.FILES)
            prod = ProductInformation()
            if imgform.is_valid():
                uid = request.session.get('uid')
                obj = get_object_or_404(User, user_id=uid)
                prod.productinformation_name = imgform.cleaned_data.get('productinformation_name')
                prod.productinformation_details = imgform.cleaned_data.get('productinformation_details')
                prod.user = obj
                prod.productsubcategory = imgform.cleaned_data.get('productsubcategory')
                prod.productcategory = imgform.cleaned_data.get('productcategory')
                prod.productinformation_baseprice = imgform.cleaned_data.get('productinformation_baseprice')
                prod.save()
            for file in request.FILES.getlist('images'):
                instance = ProductImages(
                    productinformation=ProductInformation.objects.all().last())
                instance.productimages_image = file
                instance.save()
            return redirect('/product/display-product/')


# confirm verification of product before sending to admin
class UpdateProduct(View):
    @user_login
    def get(self, request, id):
        obj = ProductInformation.objects.get(productinformation_id=id)
        img = ProductImages.objects.filter(productinformation=obj)
        form = ProductInformationForm(instance=obj)
        uname=request.session.get('uname')
        return render(request, 'update_product.html', {'form': form,'user':uname, 'obj': obj, 'img': img})

    def post(self, request, id):
        obj = ProductInformation.objects.get(productinformation_id=id)
        form = ProductInformationForm(
            request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()

        for file in request.FILES.getlist('images'):
            instance = ProductImages(
                productinformation=ProductInformation.objects.all().last())
            instance.productimages_image = file
            instance.save()
        return redirect('/product/display-product/')


# view for to add product category
class SendProduct(View):
    def get(self, request, *args, **kwargs):
        prod_id = kwargs.get('id')
        if prod_id:
            messages.success(request, 'Product is send to verification !!! ')
            obj = ProductInformation.objects.get(pk=prod_id)
            user_id = request.session.get('uid')
            uobj = User.objects.get(pk=user_id)
            obj.save()
            return redirect('/product/display-product/')


class MyProduct(View):
    @user_login
    def get(self, request):
        uid=request.session.get('uid')
        information = ProductInformation.objects.filter(user__user_id=uid)
        user = request.session.get('uname')
        return render(request, 'myproduct.html', {'information': information,'user':user})
