from django.urls import path
from . import views, AdminViews

urlpatterns = [
    path('stock/', views.stock_page_view, name='stock'),
    path('add_product/', views.add_product_page_view, name='add_product'),
    path('update_product/<id>', views.update_product_view, name='update_product'),
    path('delete_product/<id>', views.delete_product_view, name='delete_product'),
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

    # url for Adminviews.py file for merchant Merchant User

    path('merchant_create',AdminViews.MerchantUserCreateView.as_view(),name="merchant_create"),
    path('merchant_list',AdminViews.MerchantUserListView.as_view(),name="merchant_list"),
    path('merchant_update/<slug:pk>',AdminViews.MerchantUserUpdateView.as_view(),name="merchant_update"),


    # genral admin

    path('admin/', views.adminLogin, name="admin_login"),
    path('demo', views.demoPage),
    path('demoPage', views.demoPageTemplate),
    path('admin_login_process', views.adminLoginProcess, name="admin_login_process"),
    path('admin_logout_process', views.adminLogoutProcess, name="admin_logout_process"),

    # PAGE FOR ADMIN
    path('admin_home', AdminViews.admin_home, name="admin_home")
]
