from django.db import models
from User.models import User

# Create your models here.


class ProductCategory(models.Model):
    productcategory_id = models.AutoField(primary_key=True)
    productcategory_name = models.CharField(max_length=36)

    def __str__(self):
        return self.productcategory_name


class ProductSubcategory(models.Model):
    productsubcategory_id = models.AutoField(primary_key=True)
    productsubcategory_name = models.CharField(max_length=36)
    productcategory = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.productsubcategory_name


class ProductInformation(models.Model):
    productinformation_id = models.AutoField(primary_key=True)
    productcategory = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE)
    productsubcategory = models.ForeignKey(
        ProductSubcategory, on_delete=models.CASCADE)
    productinformation_name = models.CharField(max_length=36)
    productinformation_details = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_verify = models.BooleanField(default=False)
    productinformation_baseprice = models.FloatField()

    def __str__(self):
        return (f'{self.productinformation_id}')


class ProductImages(models.Model):
    productimages_id = models.AutoField(primary_key=True)
    productinformation = models.ForeignKey(
        ProductInformation, on_delete=models.CASCADE)
    productimages_image = models.FileField(upload_to="product/")

    def __str__(self):
        return f'{self.productimages_id}'
