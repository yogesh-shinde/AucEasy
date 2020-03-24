from django import forms
from Product.models import *

class ProductCategoryForm(forms.ModelForm):
    class Meta:
        model=ProductCategory
        fields='__all__'

class ProductSubcategoryForm(forms.ModelForm):
    class Meta:
        model=ProductSubcategory
        fields='__all__'

class ProductImagesForm(forms.ModelForm):
    class Meta:
        model=ProductImages
        fields='__all__'

class ProductInformationForm(forms.ModelForm):
    class Meta:
        model=ProductInformation
        fields='__all__'
        exclude=['user','product_verify']
