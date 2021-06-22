from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.urls import reverse
from tablib import Dataset

from inventory_app.models import Stock, StockHistory, Dropdown
from inventory_app.forms import StockCreateForm, ReceiveForm, IssueForm, ReorderLevelForm, DropdownForm
from django.http import HttpResponse, HttpResponseRedirect
from .filter import StockFilter
import csv

# for normal app-->
from inventory_app.resources import StockResource


@login_required(login_url="/userloginviews")
def stock_page_view(request):


    auth_user_id = request.user.id
    print(auth_user_id)
    stocks = Stock.objects.all()

    filter_list = StockFilter(request.POST, queryset=stocks)


#  Ritik code begins here
    drop = DropdownForm()
    print(drop)
    if request.method == 'POST':

        formdate= request.POST.get('formdate')
        todate = request.POST.get('todate')
        searchResult = Stock.objects.raw('SELECT * FROM stock WHERE timestamp between "'+str(formdate)+'" and "'+str(todate)+'"')
        print(searchResult)
        return render(request, 'inventory_html/stock_list.html', {'stocks': stocks, 'filter': filter_list, 'drop': drop,  'data': searchResult})


# Ritik's code end here

    # below statement is to fetch data from database and passing it in the form of list for use of twilio
    # stockitem=list(Stock.objects.all().values_list('item_name', flat=True))
    # print(stockitem)
    return render(request, 'inventory_html/stock_list.html', {'stocks': stocks, 'filter': filter_list} )





@login_required(login_url="/userloginviews")
def add_product_page_view(request):
    form = StockCreateForm()
    if request.method == 'POST':
        form = StockCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/stock')
        else:
            form.save()

    return render(request, 'inventory_html/product_add.html', {'form': form})


@login_required(login_url="/userloginviews")
def update_product_view(request, id):
    product = Stock.objects.get(id=id)
    form = StockCreateForm(instance=product)
    # image_form=product_image_Form(instance=product)
    if request.method == 'POST':
        form = StockCreateForm(request.POST, request.FILES, instance=product)
        # image_form = product_image_Form(request.POST,request.FILES,instance=product)
        if form.is_valid():
            auth_user_id = request.POST.get('auth_user_id')
            form.auth_user_id = auth_user_id
            form.save()
            # image_form.save()
            return redirect('/stock')
    context = {'form': form}
    return render(request, 'inventory_html/product_update.html', context)


@login_required(login_url="/userloginviews")
def delete_product_view(request, id):
    product = Stock.objects.get(id=id)
    product.delete()
    return redirect('/stock')


@login_required(login_url="/userloginviews")
def issue_items(request, id):
    product = Stock.objects.get(id=id)
    form = IssueForm(request.POST or None, instance=product)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.receive_quantity = 0
        instance.quantity -= instance.issue_quantity
        instance.issue_by = str(request.user)
        messages.success(request, "Issued SUCCESSFULLY. " + str(instance.quantity) + " " + str(
            instance.item_name) + "s now left in Store")
        instance.save()

        return redirect('/stock')
    # return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": 'Issue ' + str(product.item_name),
        "queryset": product,
        "form": form,
        "username": 'Issue By: ' + str(request.user),
    }
    return render(request, "inventory_html/issue_items.html", context)


@login_required(login_url="/userloginviews")
def receive_items(request, id):
    product = Stock.objects.get(id=id)
    form = ReceiveForm(request.POST or None, instance=product)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.issue_quantity = 0
        instance.quantity += instance.receive_quantity
        instance.save()
        messages.success(request, "Received SUCCESSFULLY. " + str(instance.quantity) + " " + str(
            instance.item_name) + "s now in Store")

        return redirect('/stock/')
    # return HttpResponseRedirect(instance.get_absolute_url())
    context = {
        "title": 'Receive ' + str(product.item_name),
        "instance": product,
        "form": form,
        "username": 'Receive By: ' + str(request.user),
    }
    return render(request, "inventory_html/recieve_items.html", context)


@login_required(login_url="/userloginviews")
def reorder_level(request, id):
    product = Stock.objects.get(id=id)
    form = ReorderLevelForm(request.POST or None, instance=product)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Reorder level for " + str(instance.item_name) + " is updated to " + str(
            instance.reorder_level))

        return redirect("/stock")
    context = {
        "instance": product,
        "form": form,
    }
    return render(request, "inventory_html/reorder_items.html", context)


@login_required(login_url="/userloginviews")
def list_history(request):
    header = 'LIST OF ITEMS'
    auth_user_id = request.user.id
    queryset = StockHistory.objects.filter(auth_user_id=auth_user_id)
    context = {
        "header": header,
        "queryset": queryset,
    }
    return render(request, "inventory_html/list_history.html", context)


@login_required(login_url="/userloginviews")
def delete_history(request):
    auth_user_id = request.user.id
    stock_history = StockHistory.objects.filter(auth_user_id=auth_user_id)
    stock_history.delete()
    return redirect('/list_history')


@login_required(login_url="/userloginviews")
def import_data(request):
    global result
    if request.method == 'POST':
        try:
            file_format = request.POST['file-format']
            employee_resource = StockResource()
            dataset = Dataset()
            new_employees = request.FILES['importData']
            if file_format == 'CSV':
                imported_data = dataset.load(new_employees.read().decode('utf-8'), format='csv')
                result = employee_resource.import_data(dataset, dry_run=True)
            elif file_format == 'JSON':
                imported_data = dataset.load(new_employees.read().decode('utf-8'), format='json')
                # Testing data import
                result = employee_resource.import_data(dataset, dry_run=True)

            elif file_format == 'XLS (Excel)':
                imported_data = dataset.load(new_employees.read().decode('utf-8'), format='xls')
                result = employee_resource.import_data(dataset, dry_run=True)

            if result.has_errors():
                messages.error(request, 'Uh oh! Something went wrong...')

            else:
                # Import now
                employee_resource.import_data(dataset, dry_run=False)
                messages.success(request, 'Your words were successfully imported')

        except KeyError:
            messages.error(request, 'please attach the file')
        except NameError:
            messages.error(request, 'Please Select the file format')
    return render(request, 'inventory_html/import.html')


@login_required(login_url="/userloginviews")
def export_data(request):
    auth_user_id = request.user.id
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        employee_resource = StockResource()
        dataset = employee_resource.export(auth_user_id=auth_user_id)
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
            return response
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
            return response
        elif file_format == 'XLS (Excel)':
            response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xls"'
            return response
        else:
            messages.error(request, 'You have not selected file format')

    return render(request, 'inventory_html/export.html')


# views for Inovoice management
from inventory_app.forms import InvoiceForm
from inventory_app.models import Invoice


def add_invoice(request):
    form = InvoiceForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('/add_invoice')
    context = {
        "form": form,
        "title": "New Invoice",
    }
    return render(request, "inventory_html/entry.html", context)


def list_invoice(request):
    title = 'List of Invoices'
    queryset = Invoice.objects.all()
    context = {
        "title": title,
        "queryset": queryset,
    }
    return render(request, "inventory_html/list_invoice.html", context)


# Admin login logout home related views


# Create your views here.
def demoPage(request):
    return HttpResponse("demo Page")


def demoPageTemplate(request):
    return render(request, "demo.html")


def adminLogin(request):
    return render(request, "admin_templates/signin.html")


def adminLoginProcess(request):
    username = request.POST.get("username")
    password = request.POST.get("password")

    user = authenticate(request=request, username=username, password=password)
    if user is not None:
        login(request=request, user=user)
        return HttpResponseRedirect(reverse("admin_home"))
    else:
        messages.error(request, "Error in Login! Invalid Login Details!")
        return HttpResponseRedirect(reverse("admin_login"))


def adminLogoutProcess(request):
    logout(request)
    messages.success(request, "Logout Successfully!")
    return HttpResponseRedirect(reverse("show_login"))


# firebase code

def showFirebaseJS(request):
    data = 'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-app.js");' \
           'importScripts("https://www.gstatic.com/firebasejs/7.14.6/firebase-messaging.js"); ' \
           'var firebaseConfig = {' \
           '        apiKey: "AIzaSyBu0d0iW41tmu6rR9JJG-ODlwJgz5nmOPM",' \
           '        authDomain: "kolentry-2569b.firebaseapp.com",' \
           '        databaseURL: "https://kolentry-2569b-default-rtdb.firebaseio.com",' \
           '        projectId: "kolentry-2569b",' \
           '        storageBucket: "kolentry-2569b.appspot.com",' \
           '        messagingSenderId: "858489842790",' \
           '        appId: "1:858489842790:web:ae99848a638ad5850651a7",' \
           '        measurementId: "G-MH7VTBJKJK"' \
           ' };' \
           'firebase.initializeApp(firebaseConfig);' \
           'const messaging=firebase.messaging();' \
           'messaging.setBackgroundMessageHandler(function (payload) {' \
           '    console.log(payload);' \
           '    const notification=JSON.parse(payload);' \
           '    const notificationOption={' \
           '        body:notification.body,' \
           '        icon:notification.icon' \
           '    };' \
           '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
           '});'

    return HttpResponse(data, content_type="text/javascript")
