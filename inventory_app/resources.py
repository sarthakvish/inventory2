from import_export import resources
from inventory_app.models import Stock

class StockResource(resources.ModelResource):
    class Meta:
        model=Stock
        # import_id_field=['item_name']

    def export(self, queryset=None, *args, **kwargs):
        queryset = Stock.objects.filter(auth_user_id=kwargs['auth_user_id'])
        return super(StockResource, self).export(queryset, *args, **kwargs)