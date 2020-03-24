from django.contrib import admin
from Product.models import *

# Register your models here.
admin.site.register(ProductCategory)
admin.site.register(ProductSubcategory)
admin.site.register(ProductImages)
admin.site.register(ProductInformation)