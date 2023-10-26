from django import forms
from transactions.models import CreditCard

class CreditCardForm(forms.ModelForm):
    class Meta:
        model = CreditCard
        fields = ['name','number','month','year','cvv','card_type']
