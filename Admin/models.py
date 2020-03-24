from django.db import models

# Create your models here.


class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length=36)

    def __str__(self):
        return self.country_name


class State(models.Model):
    state_id = models.AutoField(primary_key=True)
    state_name = models.CharField(max_length=36)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.state_name


class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=36)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return self.city_name


class Area(models.Model):
    area_id = models.AutoField(primary_key=True)
    area_name = models.CharField(max_length=36)
    area_pincode = models.IntegerField(unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.area_name


class IdProof(models.Model):
    idproof_id = models.AutoField(primary_key=True)
    idproof_type = models.CharField(max_length=36)

    def __str__(self):
        return self.idproof_type


class AdminUser(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=36)
    admin_username = models.CharField(max_length=36,unique=True)
    admin_password = models.CharField(max_length=36)
    admin_confirm_password = models.CharField(max_length=36)
    admin_email = models.EmailField()
    admin_contact = models.IntegerField(unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return self.admin_name
