from django import forms
from Admin.models import *
from django.contrib.auth.password_validation import validate_password
from django.core import validators
from django.core.exceptions import ValidationError

class CountryForm(forms.ModelForm):
    class Meta:
        model=Country
        fields='__all__'

class StateForm(forms.ModelForm):
    class Meta:
        model=State
        fields='__all__'

class CityForm(forms.ModelForm):
    class Meta:
        model=City
        fields='__all__'

class AreaForm(forms.ModelForm):
    class Meta:
        model=Area
        fields='__all__'
    
    def clean_pincode(self):
        area_pincode=self.cleaned_data.get('area_pincode')
        if len(str(area_pincode)) != 6:
            self._errors['area_pincode']=self.error_class(['Pin code must be 6 digits only'])
        return area_pincode

class IdProofForm(forms.ModelForm):
    class Meta:
        model=IdProof
        fields='__all__'

class AdminUserForm(forms.ModelForm):
    admin_password=forms.CharField(widget=forms.PasswordInput,validators=[validate_password])
    admin_confirm_password=forms.CharField(widget=forms.PasswordInput,validators=[validate_password])

    class Meta:
        model=AdminUser
        fields=['admin_id','admin_name','admin_username','admin_password','admin_confirm_password',
        'admin_email','admin_contact','country','state','city','area']

    def clean(self):
        admin_username=self.cleaned_data.get('admin_username')
        admin_password = self.cleaned_data.get('admin_password')
        admin_confirm_password = self.cleaned_data.get('admin_confirm_password')
        admin_email=self.cleaned_data.get('admin_email')
        admin_contact=self.cleaned_data.get('admin_contact')

        username_qs = AdminUser.objects.filter(admin_username=admin_username)
        if username_qs.exists():
            self._errors['admin_username']=self.error_class(['Username already exists'])
        if admin_password != admin_confirm_password:
            self._errors['admin_confirm_password']=self.error_class(["Password didn't match"])

        if '.edu' in admin_email:
            self._errors['admin_email']=self.error_class(['Educational emails are not allowed'])

        if len(str(admin_contact)) !=10:
            self.errors['admin_contact']=self.error_class(['Contact No. must be of 10 digits'])

        return self.cleaned_data   
    
class AdminLoginForm(forms.Form):
    admin_username=forms.CharField()
    admin_confirm_password=forms.CharField(widget=forms.PasswordInput)

class AdminForm(forms.ModelForm):
    admin_password=forms.CharField(widget=forms.PasswordInput)
    admin_confirm_password=forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model=AdminUser
        fields='__all__'


class AdminProfile(forms.ModelForm):
    class Meta:
        model=AdminUser
        fields=['admin_id','admin_name','admin_username','admin_email','admin_contact','country','state','city','area']

    def clean(self):
        admin_username=self.cleaned_data.get('admin_username')
        admin_email=self.cleaned_data.get('admin_email')
        admin_contact=self.cleaned_data.get('admin_contact')

        # username_qs = AdminUser.objects.filter(admin_username=admin_username)
        # if username_qs.exists():
        #     self._errors['admin_username']=self.error_class(['Username already exists'])

        if '.edu' in admin_email:
            self._errors['admin_email']=self.error_class(['Educational emails are not allowed'])

        if len(str(admin_contact)) !=10:
            self.errors['admin_contact']=self.error_class(['Contact No. must be of 10 digits'])

        return self.cleaned_data   

