from django import forms
from Reports.models import *


class AuctionQueryForm(forms.ModelForm):
    class Meta:
        model = AuctionQuery
        fields = '__all__'
