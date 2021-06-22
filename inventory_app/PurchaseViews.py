from django.shortcuts import render
from .models import AdminUser, MerchantUser


def create_requirements(request):
    return render(request, "purchase/create_requirements.html")


def accepting_quotation(request):
    return render(request, "purchase/accepting_quotation.html")


def purchase_order(request):
    return render(request, "purchase/purchase_order.html")


def receiving_invoice(request):
    return render(request, "purchase/receiving_invoice.html")
