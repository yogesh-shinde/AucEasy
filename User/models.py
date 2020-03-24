from django.db import models
from Admin.models import *

# Create your models here.


class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=36)
    user_username = models.CharField(max_length=36)
    user_password = models.CharField(max_length=36)
    user_confirm_password = models.CharField(max_length=36)
    user_email = models.EmailField()
    user_contact = models.IntegerField()
    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = [(GENDER_MALE, 'Male'), (GENDER_FEMALE, 'Female')]
    gender = models.IntegerField(choices=GENDER_CHOICES)
    idproof = models.ManyToManyField(IdProof)
    idproof_images=models.ImageField(upload_to='idproof/')
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_name
class Messages(models.Model):
    messages_id = models.AutoField(primary_key=True)
    messages_text = models.TextField()
    '''USer foreign key we have to use here'''
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.messages_id

