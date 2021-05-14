from django.shortcuts import render
from.models import AdminUser, MerchantUser


def merchant_home(request):
    total_admin=AdminUser.objects.all().count()
    return render(request,"merchant_templates/merchant_home.html", {'total_admin':total_admin})