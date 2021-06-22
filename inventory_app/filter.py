# ritik code

from .models import Stock
import django_filters


class StockFilter(django_filters.FilterSet):

    class Meta:
        model = Stock
        fields = ['category', 'sub_category', 'item_name', 'location']
