import datetime
import json
import os
from inventory_app.decorators import anonymous_required, login_excluded


import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from .EmailBackEnd import EmailBackend
from .models import CustomUser

@login_excluded('/stock')
def ShowLoginPage(request):
    return render(request,"admin_templates/login_page.html")

@login_excluded('/stock')
def doLogin(request):
    if request.method!="POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        # captcha_token=request.POST.get("g-recaptcha-response")
        # cap_url="https://www.google.com/recaptcha/api/siteverify"
        # cap_secret="6LeWtqUZAAAAANlv3se4uw5WAg-p0X61CJjHPxKT"
        # cap_data={"secret":cap_secret,"response":captcha_token}
        # cap_server_response=requests.post(url=cap_url,data=cap_data)
        # cap_json=json.loads(cap_server_response.text)
        #
        # if cap_json['success']==False:
        #     messages.error(request,"Invalid Captcha Try Again")
        #     return HttpResponseRedirect("/userloginviews")

        user=EmailBackend.authenticate(request, username=request.POST.get("email"),password=request.POST.get("password"))
        if user!=None:
            login(request,user)
            if user.user_type=="1":
                return HttpResponseRedirect('/admin_home')
            elif user.user_type=="2":
                return HttpResponseRedirect(reverse("staff_home"))
            elif user.user_type=="3":
                return HttpResponseRedirect(reverse("merchant_home"))
            else:
                return HttpResponseRedirect(reverse("customer _home"))

        else:
            messages.error(request,"Invalid Login Details")
            return HttpResponseRedirect("/userloginviews")


 # Users Sign up Views

@login_excluded('/stock')
def signup_admin(request):
    return render(request,"admin_templates/signup_admin_page.html")

@login_excluded('/stock')
def signup_student(request):
    courses=Courses.objects.all()
    session_years=SessionYearModel.object.all()
    return render(request,"admin_templates/signup_student_page.html",{"courses":courses,"session_years":session_years})

@login_excluded('/stock')
def signup_staff(request):
    return render(request,"admin_templates/signup_staff_page.html")

@login_excluded('/stock')
def signup_merchant(request):
    return render(request,"admin_templates/signup_merchant_page.html")

@login_excluded('/stock')
def do_admin_signup(request):
    username=request.POST.get("username")
    phone = request.POST.get("phone")
    email=request.POST.get("email")
    password1=request.POST.get("password1")
    password2 = request.POST.get("password2")

    if password1==password2:
        # if CustomUser.objects.filter(username=username).exists():
        #     msg="Username Already Registered"
        #     return HttpResponse(msg)
        if CustomUser.objects.filter(phone=phone).exists():
            msg="Phone Number Already Registered"
            return HttpResponse(msg)
        if CustomUser.objects.filter(email=email).exists():
            msg="Email Already Registered"
            return HttpResponse(msg)
        else:
            try:
                user = CustomUser.objects.create_user(username=username, password=password1,phone=phone, email=email, user_type=1)
                user.save()
                messages.success(request, "Successfully Created Admin")
                return redirect("show_login")
            except:
                messages.error(request, "Failed to Create Admin")
                return redirect("show_login")
    else:
        msg="Password not Matched"
        return HttpResponse(msg)

@login_excluded('/stock')
def do_staff_signup(request):
    username=request.POST.get("username")
    email=request.POST.get("email")
    password=request.POST.get("password")
    address=request.POST.get("address")

    try:
        user=CustomUser.objects.create_user(username=username,password=password,email=email,user_type=2)
        user.staffs.address=address
        user.save()
        messages.success(request,"Successfully Created Staff")
        return HttpResponseRedirect(reverse("show_login"))
    except:
        messages.error(request,"Failed to Create Staff")
        return HttpResponseRedirect(reverse("show_login"))

@login_excluded('/stock')
def do_signup_student(request):
    first_name = request.POST.get("first_name")
    last_name = request.POST.get("last_name")
    username = request.POST.get("username")
    email = request.POST.get("email")
    password = request.POST.get("password")
    address = request.POST.get("address")
    session_year_id = request.POST.get("session_year")
    course_id = request.POST.get("course")
    sex = request.POST.get("sex")

    profile_pic = request.FILES['profile_pic']
    fs = FileSystemStorage()
    filename = fs.save(profile_pic.name, profile_pic)
    profile_pic_url = fs.url(filename)

    #try:
    user = CustomUser.objects.create_user(username=username, password=password, email=email, last_name=last_name,
                                          first_name=first_name, user_type=3)
    user.students.address = address
    course_obj = Courses.objects.get(id=course_id)
    user.students.course_id = course_obj
    session_year = SessionYearModel.object.get(id=session_year_id)
    user.students.session_year_id = session_year
    user.students.gender = sex
    user.students.profile_pic = profile_pic_url
    user.save()
    messages.success(request, "Successfully Added Student")
    return HttpResponseRedirect(reverse("show_login"))
    #except:
     #   messages.error(request, "Failed to Add Student")
      #  return HttpResponseRedirect(reverse("show_login"))

@login_excluded('/stock')
def do_merchant_signup(request):
    username=request.POST.get("username")
    phone = request.POST.get("phone")
    email=request.POST.get("email")
    password1=request.POST.get("password1")
    password2 = request.POST.get("password2")
    profile_pic = request.FILES["profile_pic"]
    fs = FileSystemStorage()
    filename = fs.save(profile_pic.name, profile_pic)
    profile_pic_url = fs.url(filename)
    profile_pic = profile_pic_url
    company_name = request.POST.get("company_name")
    gst_details = request.POST.get("gst_details")
    address = request.POST.get("address")
    is_added_by_admin = False

    if password1==password2:
        # if CustomUser.objects.filter(username=username).exists():
        #     msg="Username Already Registered"
        #     return HttpResponse(msg)

        if CustomUser.objects.filter(phone=phone).exists():
            msg="Phone Number Already Registered"
            return HttpResponse(msg)
        if CustomUser.objects.filter(email=email).exists():
            msg="Email Already Registered"
            return HttpResponse(msg)
        else:
            try:
                user = CustomUser.objects.create_user(username=username, password=password1,phone=phone, email=email, user_type=3)
                user.merchantuser.address = address
                user.merchantuser.company_name = company_name
                user.merchantuser.gst_details = gst_details
                user.merchantuser.is_added_by_admin = is_added_by_admin
                user.merchantuser.profile_pic = profile_pic_url
                user.save()
                messages.success(request, "Successfully Created Merchant")
                return redirect("show_login")
            except:
                messages.error(request, "Failed to Create Admin")
                return redirect("show_login")
    else:
        msg="Password not Matched"
        return HttpResponse(msg)