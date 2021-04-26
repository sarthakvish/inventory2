from django import forms
from datascience.models import Purchase

class PurchaseForm(forms.ModelForm):
    class Meta:
        model=Purchase
        fields=['item_name','price','quantity']