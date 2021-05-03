from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
# For normal app

from .forms import StockCreateForm, InvoiceForm
from .models import Stock, Invoice, CustomUser


class StockCreateAdmin(ImportExportModelAdmin):
   list_display = ['category', 'item_name', 'quantity', 'provider_merchant_name']
   form = StockCreateForm
   list_filter = ['category']
   search_fields = ['category', 'item_name']
admin.site.register(Stock, StockCreateAdmin)

class InvoiceAdmin(admin.ModelAdmin):
   list_display = ['name', 'invoice_number', 'invoice_date']
   form = InvoiceForm
   list_filter = ['name']
   search_fields = ['name', 'invoice_number']
admin.site.register(Invoice, InvoiceAdmin)

admin.site.register(CustomUser)


