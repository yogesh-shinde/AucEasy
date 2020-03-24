from django import forms
from User.models import *
from django.contrib.auth.password_validation import validate_password
from django.core import validators
from django.core.exceptions import ValidationError
class MessagesForm(forms.ModelForm):
    class Meta:
        model=Messages
        fields='__all__'

class PostForm(forms.ModelForm):
    user_password=forms.CharField(widget=forms.PasswordInput,validators=[validate_password])
    user_confirm_password=forms.CharField(widget=forms.PasswordInput,validators=[validate_password])

    class Meta:
        model=User
        fields=['user_id','user_name','user_username','user_password','user_confirm_password',
        'user_email','user_contact','gender','idproof','idproof_images','country','state','city','area']

    def clean(self):
        user_email=self.cleaned_data.get('user_email')
        user_contact = self.cleaned_data.get('user_contact')
        user_password=self.cleaned_data.get('user_password')
        user_confirm_password=self.cleaned_data.get('user_confirm_password')
        user_username = self.cleaned_data.get('user_username')
        user_email=self.cleaned_data.get('user_email')
        if '.edu' in user_email:
            self._errors['user_email']=self.error_class(['Educational emails are not allowed'])
        if user_password != user_confirm_password:
            self._errors['user_confirm_password'] = self.error_class([
                "Password didn't match"])
        if len(str(user_contact)) !=10:
            self._errors['user_contact'] = self.error_class([
                'contact no. should be 10 digit only'])
        username_qs = User.objects.filter(user_username=user_username)
        if username_qs.exists():
                self._errors['user_username']=self.error_class(['Username already exists'])
        
        return self.cleaned_data
        
class LoginForm(forms.Form):
    user_username=forms.CharField()
    user_confirm_password=forms.CharField(widget=forms.PasswordInput)

class UserForm(forms.ModelForm):
    Password = forms.CharField(widget=forms.PasswordInput)
    Confirmpassword = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = "__all__"


class UserProfile(forms.ModelForm):
    class Meta:
        model = User
        # exclude = ['user_password', 'user_confirm_password']
        fields=['user_id','user_name','user_username','user_email','user_contact','gender','idproof','idproof_images','country','state','city','area']

    def clean(self):
        user_email=self.cleaned_data.get('user_email')
        user_contact = self.cleaned_data.get('user_contact')
        user_username = self.cleaned_data.get('user_username')
        # user_email=self.cleaned_data.get('user_email')
        if '.edu' in user_email:
            self._errors['user_email']=self.error_class(['Educational emails are not allowed'])
        if len(str(user_contact)) !=10:
            self._errors['user_contact'] = self.error_class([
                'contact no. should be 10 digit only'])

        # if user_username.exists():
        #         self._errors['user_username']=self.error_class(['Username already exists'])
        return self.cleaned_data
