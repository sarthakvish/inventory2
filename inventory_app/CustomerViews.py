from django.shortcuts import render


def customer_home(request):
    return render(request,"student_templates/customer_home.html")
