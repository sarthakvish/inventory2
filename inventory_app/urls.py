from django.urls import path
from . import views


urlpatterns = [
    # path('store/', views.store_page_view, name='store'),
    # path('cart/', views.cart_page_view, name='cart'),
    # path('checkout/', views.checkout_page_view, name='checkout'),
    path('stock/', views.stock_page_view),
    path('add_product/', views.add_product_page_view),
    path('update_product/<id>', views.update_product_view),
    path('delete_product/<id>', views.delete_product_view),
    # path('update_item/', views.updateItem, name='update_item'),
    path('issue_items/<id>/', views.issue_items, name="issue_items"),
    path('receive_items/<id>/', views.receive_items, name="receive_items"),
    path('reorder_level/<id>/', views.reorder_level, name="reorder_level"),
    path('list_history/', views.list_history, name='list_history'),
    path('delete_history/', views.delete_history, name='delete_history'),
    path('import/', views.import_data, name='import'),
    path('export/', views.export_data, name='export'),

    # urls for Invoice management
    path('add_invoice/', views.add_invoice, name='add_invoice'),
    path('list_invoice/', views.list_invoice, name='list_invoice'),
]
