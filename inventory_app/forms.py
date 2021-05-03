from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db.models import Q

from .models import Stock, Invoice, MerchantUser,CustomUser


class StockCreateForm(forms.ModelForm):
    provider_merchant_name=forms.ModelChoiceField(queryset=MerchantUser.objects.all())
    class Meta:
        model = Stock
        fields = ['category', 'item_name','quantity','measurement_unit','reorder_level','provider_merchant_name']

class IssueForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['issue_quantity', 'issue_to']


class ReceiveForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['receive_quantity', 'receive_by']

class ReorderLevelForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['reorder_level']


# forms for Invoice management
# class InvoiceForm(forms.ModelForm):
#     class Meta:
#         model = Invoice
#         fields = ['name', 'phone_number', 'invoice_date',
#                 'line_one', 'line_one_quantity', 'line_one_unit_price', 'line_one_total_price',
#                 'line_two', 'line_two_quantity', 'line_two_unit_price', 'line_two_total_price',
#                 'line_three', 'line_three_quantity', 'line_three_unit_price', 'line_three_total_price',
#                 'line_four', 'line_four_quantity', 'line_four_unit_price', 'line_four_total_price',
#                 'line_five', 'line_five_quantity', 'line_five_unit_price', 'line_five_total_price',
#                 'total', 'paid', 'invoice_type'
#                 ]
class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = ['name', 'phone_number', 'invoice_date',
                'line_one', 'line_one_quantity', 'line_one_unit_price', 'line_one_total_price',
                'total', 'paid', 'invoice_type'
                ]
# for mobile login signup

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


# class UserAdminCreationForm(UserCreationForm):
#     """
#     A Custom form for creating new users.
#     """
#
#     class Meta:
#         model = CustomUser
#         fields = ['phone']


from allauth.account.forms import SignupForm
from django import forms

# class CustomSignupForm(SignupForm):
#     phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$',
#                                  message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")
#     phone = forms.CharField()  # validators should be a list
#
#     class Meta:
#         model = CustomUser
#         fields = ['username', 'password1', 'password2']
#
#     def signup(self, request, user):
#
#         user.save()
#         return user
