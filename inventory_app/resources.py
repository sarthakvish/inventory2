from import_export import resources
from inventory_app.models import Stock

class StockResource(resources.ModelResource):
    class Meta:
        model=Stock
