from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import User, AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
#
# class CustomUserManager(BaseUserManager):
#     """Define a model manager for User model with no username field."""
#
#     use_in_migrations = True
#
#     def _create_user(self, phone, password, **extra_fields):
#         """Create and save a User with the given phone and password."""
#         if not phone:
#             raise ValueError('The given phone must be set')
#         self.phone = phone
#         user = self.model(phone=phone, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_user(self, phone, password=None, **extra_fields):
#         """Create and save a regular User with the given phone and password."""
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(phone, password, **extra_fields)
#
#     def create_superuser(self, phone, password, **extra_fields):
#         """Create and save a SuperUser with the given phone and password."""
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#
#         return self._create_user(phone, password, **extra_fields)
# class CustomUser(AbstractUser):
#     phone_regex = RegexValidator(regex=r'^\+?1?\d{9,10}$',
#                                  message="Phone number must be entered in the format: '+999999999'. Up to 10 digits allowed.")
#     phone = models.CharField(_('phone'),validators=[phone_regex], max_length=10,blank=False,
#                                     null=False)  # validators should be a list
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['phone']
#
#     objects = CustomUserManager()
#     def __str__(self):
#         return self.username
# models for Normal app.
class Stock(models.Model):
    unit = 'un'
    kilogram = 'kg'
    bori = 'br'
    choices = [
        (unit, 'unit'),
        (kilogram, 'kg'),
        (bori, 'bori'),
    ]
    # user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_quantity = models.IntegerField(default='0', blank=True, null=True)
    measurement_unit = models.CharField(choices=choices, max_length=255, default='Choose measurement unit')
    receive_by = models.CharField(max_length=50, blank=True, null=True)
    issue_quantity = models.IntegerField(default='0', blank=True, null=True)
    issue_by = models.CharField(max_length=50, blank=True, null=True)
    issue_to = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    export_to_CSV = models.BooleanField(default=False)

    def __str__(self):
        return self.item_name +' '+ str(self.quantity) +' '+ self.measurement_unit

class StockHistory(models.Model):
    category = models.CharField(max_length=50, blank=True, null=True)
    item_name = models.CharField(max_length=50, blank=True, null=True)
    quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_quantity = models.IntegerField(default='0', blank=True, null=True)
    receive_by = models.CharField(max_length=50, blank=True, null=True)
    issue_quantity = models.IntegerField(default='0', blank=True, null=True)
    issue_by = models.CharField(max_length=50, blank=True, null=True)
    issue_to = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.CharField(max_length=50, blank=True, null=True)
    reorder_level = models.IntegerField(default='0', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)
    timestamp = models.DateTimeField(auto_now_add=False, auto_now=False, null=True)

# Models for Invoice
class Invoice(models.Model):
    comments = models.TextField(max_length=3000, default='', blank=True, null=True)
    invoice_number = models.IntegerField(blank=True, null=True)
    invoice_date = models.DateField(auto_now_add=False, auto_now=False, blank=True, null=True)
    name = models.CharField('Customer Name', max_length=120, default='', blank=True, null=True)

    line_one = models.CharField('Line 1', max_length=120, default='', blank=True, null=True)
    line_one_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_one_unit_price = models.IntegerField('Unit Price (D)', default=0, blank=True, null=True)
    line_one_total_price = models.IntegerField('Line Total (D)', default=0, blank=True, null=True)

    line_two = models.CharField('Line 2', max_length=120, default='', blank=True, null=True)
    line_two_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_two_unit_price = models.IntegerField('Unit Price (D)', default=0, blank=True, null=True)
    line_two_total_price = models.IntegerField('Line Total (D)', default=0, blank=True, null=True)

    line_three = models.CharField('Line 3', max_length=120, default='', blank=True, null=True)
    line_three_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_three_unit_price = models.IntegerField('Unit Price (D)', default=0, blank=True, null=True)
    line_three_total_price = models.IntegerField('Line Total (D)', default=0, blank=True, null=True)

    line_four = models.CharField('Line 4', max_length=120, default='', blank=True, null=True)
    line_four_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_four_unit_price = models.IntegerField('Unit Price (D)', default=0, blank=True, null=True)
    line_four_total_price = models.IntegerField('Line Total (D)', default=0, blank=True, null=True)

    line_five = models.CharField('Line 5', max_length=120, default='', blank=True, null=True)
    line_five_quantity = models.IntegerField('Quantity', default=0, blank=True, null=True)
    line_five_unit_price = models.IntegerField('Unit Price (D)', default=0, blank=True, null=True)
    line_five_total_price = models.IntegerField('Line Total (D)', default=0, blank=True, null=True)

    phone_number = models.CharField(max_length=120, default='', blank=True, null=True)
    total = models.IntegerField(default='0', blank=True, null=True)
    balance = models.IntegerField(default='0', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    last_updated = models.DateTimeField(auto_now_add=False, auto_now=True, blank=True)
    paid = models.BooleanField(default=False)
    invoice_type_choice = (
        ('Receipt', 'Receipt'),
        ('Proforma Invoice', 'Proforma Invoice'),
        ('Invoice', 'Invoice'),
    )
    invoice_type = models.CharField(max_length=50, default='', blank=True, null=True, choices=invoice_type_choice)

    def __unicode__(self):
        return self.invoice_number
# models for react app.
class Provider(models.Model):
    id=models.AutoField(primary_key=True)
    provider_name=models.CharField(max_length=255)
    license_no=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    provider_contact=models.CharField(max_length=255, unique=True)
    email=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    added_on=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Product(models.Model):
    choices = ((1, "Bori"), (2, "Kg"), (3, "unit"))

    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255, unique=True)
    buy_price=models.CharField(max_length=255)
    sell_price=models.CharField(max_length=255)
    c_gst=models.CharField(max_length=255)
    s_gst=models.CharField(max_length=255)
    description=models.CharField(max_length=255)
    measurement_unit=models.CharField(choices=choices,max_length=255)
    in_stock_total=models.IntegerField()
    qty_in_strip=models.IntegerField()
    added_on=models.DateTimeField(auto_now_add=True)
    provider_name=models.CharField(max_length=255)
    provider_contact=models.CharField(max_length=255, unique=True)
    Provider_id=models.IntegerField()
    objects=models.Manager()

class Employee(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    joining_date=models.DateField()
    phone=models.CharField(max_length=255, unique=True)
    address=models.CharField(max_length=255)
    added_on=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Customer(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    contact=models.CharField(max_length=255, unique=True)
    added_on=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Bill(models.Model):
    id=models.AutoField(primary_key=True)
    added_on=models.DateTimeField(auto_now_add=True)
    customer_id = models.IntegerField()
    contact=models.CharField(max_length=255, unique=True)
    objects=models.Manager()

class BillDetails(models.Model):
    id=models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=255, unique=True)
    product_id=models.IntegerField()
    qty=models.IntegerField()
    added_on=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class CustomerRequest(models.Model):
    id=models.AutoField(primary_key=True)
    customer_name=models.CharField(max_length=255)
    phone=models.CharField(max_length=255)
    product_details=models.CharField(max_length=255)
    status=models.BooleanField(default=False)
    added_on=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class ProviderAccount(models.Model):
    choices=((1,"Debit"),(2,"Credit"))

    id=models.AutoField(primary_key=True)
    provider_name=models.CharField(max_length=255, unique=True)
    provider_contact=models.CharField(max_length=255, unique=True)
    provider_id=models.IntegerField(unique=True)
    transaction_type=models.CharField(choices=choices,max_length=255)
    transaction_amt=models.CharField(max_length=255)
    transaction_date=models.DateField()
    payment_mode=models.CharField(max_length=255)
    added_on=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

# class ProviderBank(models.Model):
#     id=models.AutoField(primary_key=True)
#     bank_account_no=models.CharField(max_length=255)
#     ifsc_no=models.CharField(max_length=255)
#     company_id=models.ForeignKey(Company,on_delete=models.CASCADE)
#     added_on=models.DateTimeField(auto_now_add=True)
#     objects=models.Manager()

# class EmployeeBank(models.Model):
#     id=models.AutoField(primary_key=True)
#     bank_account_no=models.CharField(max_length=255)
#     ifsc_no=models.CharField(max_length=255)
#     employee_id=models.ForeignKey(Employee,on_delete=models.CASCADE)
#     added_on=models.DateTimeField(auto_now_add=True)
#     objects=models.Manager()



