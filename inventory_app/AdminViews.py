from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView,CreateView,UpdateView,DetailView,View
from inventory_app.models import CustomUser, MerchantUser, AdminUser
from django.contrib.messages.views import SuccessMessageMixin
from django.core.files.storage import FileSystemStorage
from django.contrib.messages.views import messages
from django.urls import reverse
from django.http import HttpResponseRedirect,HttpResponse
from django.db.models import Q, Sum, F
from inventory_app.models import Stock, StockHistory, MerchantUser


@login_required(login_url="/userloginviews")
def admin_home(request):
    auth_user_id = request.user.id
    stock_count=Stock.objects.filter(auth_user_id=auth_user_id).count()
    stock_reorder_count=Stock.objects.filter(auth_user_id=auth_user_id,quantity__lte=F('reorder_level')).count()
    total_issue_quantity= StockHistory.objects.filter(auth_user_id=auth_user_id).aggregate(Sum('issue_quantity'))['issue_quantity__sum']
    total_receive_quantity = StockHistory.objects.filter(auth_user_id=auth_user_id).aggregate(Sum('receive_quantity'))['receive_quantity__sum']
    total_merchant_user= MerchantUser.objects.all().count()
    context={
        'stock_count':stock_count,
        'issue_quantity': total_issue_quantity,
        'receive_quantity': total_receive_quantity,
        'total_merchant_user': total_merchant_user,
        'stock_reorder_count': stock_reorder_count,
    }
    return render(request,"admin_templates/admin_home.html", context)


@login_required(login_url="/userloginviews")
def admin_profile(request):
    admin_user= AdminUser.objects.get(auth_user_id=request.user.id)
    return render(request, "admin_templates/admin_profile.html", {"admin_user":admin_user})

@login_required(login_url="/userloginviews")
def admin_profile_save(request):
    if request.method=="POST":
        first_name=request.POST.get("first_name")
        last_name=request.POST.get("last_name")
        password=request.POST.get("password")
        profile_pic = request.FILES.get("profile_pic")
        try:
            customuser=CustomUser.objects.get(id=request.user.id)
            customuser.first_name=first_name
            customuser.last_name=last_name
            # if password!=None and password!="":
            #     customuser.set_password(password)
            customuser.save()
            admin_user=AdminUser.objects.get(auth_user_id=request.user.id)

            fs = FileSystemStorage()
            filename = fs.save(profile_pic.name, profile_pic)
            profile_pic_url = fs.url(filename)
            admin_user.profile_pic=profile_pic_url
            admin_user.save()
            messages.success(request, "Successfully Updated Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
        except:
            messages.error(request, "Failed to Update Profile")
            return HttpResponseRedirect(reverse("admin_profile"))
    return HttpResponseRedirect(reverse("admin_profile"))

# @login_required(login_url="/userloginviews")
class MerchantUserListView(ListView):

    template_name="admin_templates/merchant_list.html"
    paginate_by=3

    def get_queryset(self):
        filter_val=self.request.GET.get("filter","")
        order_by=self.request.GET.get("orderby","id")
        if filter_val!="":
            cat=MerchantUser.objects.filter(Q(auth_user_id__first_name__contains=filter_val) |Q(auth_user_id__last_name__contains=filter_val) | Q(auth_user_id__email__contains=filter_val) | Q(auth_user_id__username__contains=filter_val)).order_by(order_by)
        else:
            cat=MerchantUser.objects.all().order_by(order_by)

        return cat

    def get_context_data(self,**kwargs):
        context=super(MerchantUserListView,self).get_context_data(**kwargs)
        context["filter"]=self.request.GET.get("filter","")
        context["orderby"]=self.request.GET.get("orderby","id")
        context["all_table_fields"]=MerchantUser._meta.get_fields()
        return context


# @login_required(login_url="/userloginviews")
class MerchantUserCreateView(SuccessMessageMixin,CreateView):
    template_name="admin_templates/merchant_create.html"
    model=CustomUser
    fields=["first_name","last_name","phone", "email","username","password"]

    def form_valid(self,form):

        #Saving Custom User Object for Merchant User
        user=form.save(commit=False)
        user.is_active=True
        user.user_type=3
        user.set_password(form.cleaned_data["password"])
        user.save()

        #Saving Merchant user
        profile_pic=self.request.FILES["profile_pic"]
        fs=FileSystemStorage()
        filename=fs.save(profile_pic.name,profile_pic)
        profile_pic_url=fs.url(filename)

        user.merchantuser.profile_pic=profile_pic_url
        user.merchantuser.company_name=self.request.POST.get("company_name")
        user.merchantuser.gst_details=self.request.POST.get("gst_details")
        user.merchantuser.address=self.request.POST.get("address")
        is_added_by_admin=False

        if self.request.POST.get("is_added_by_admin")=="on":
            is_added_by_admin=True

        user.merchantuser.is_added_by_admin=is_added_by_admin
        user.save()
        messages.success(self.request,"Merchant User Created")
        return HttpResponseRedirect(reverse("merchant_list"))

# @login_required(login_url="/userloginviews")
class MerchantUserUpdateView(SuccessMessageMixin,UpdateView):
    template_name="admin_templates/merchant_update.html"
    model=CustomUser
    fields=["first_name","last_name","email","username","password"]

    def get_context_data(self,**kwargs):
        context=super().get_context_data(**kwargs)
        merchantuser=MerchantUser.objects.get(auth_user_id=self.object.pk)
        context["merchantuser"]=merchantuser
        return context

    def form_valid(self,form):

        #Saving Custom User Object for Merchant User
        user=form.save(commit=False)
        user.set_password(form.cleaned_data["password"])
        user.save()

        #Saving Merchant user
        merchantuser=MerchantUser.objects.get(auth_user_id=user.id)
        if self.request.FILES.get("profile_pic",False):
            profile_pic=self.request.FILES["profile_pic"]
            fs=FileSystemStorage()
            filename=fs.save(profile_pic.name,profile_pic)
            profile_pic_url=fs.url(filename)
            merchantuser.profile_pic=profile_pic_url

        merchantuser.company_name=self.request.POST.get("company_name")
        merchantuser.gst_details=self.request.POST.get("gst_details")
        merchantuser.address=self.request.POST.get("address")
        is_added_by_admin=False

        if self.request.POST.get("is_added_by_admin")=="on":
            is_added_by_admin=True

        merchantuser.is_added_by_admin=is_added_by_admin
        merchantuser.save()
        messages.success(self.request,"Merchant User Updated")
        return HttpResponseRedirect(reverse("merchant_list"))


# views for firebase push notification

@csrf_exempt
def admin_fcmtoken_save(request):
    if request.method=='POST':
        token = request.POST.get("token")
        try:
            admin = AdminUser.objects.get(auth_user_id=request.user.id)
            admin.fcm_token = token
            admin.save()
            return HttpResponse("True")
        except:
            return HttpResponse("False")

