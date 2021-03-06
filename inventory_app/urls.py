from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views, AdminViews, CustomerViews, MerchantViews, StaffViews, UsersLoginViews, PurchaseViews

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

    path('merchant_create',login_required(AdminViews.MerchantUserCreateView.as_view()),name="merchant_create"),
    path('merchant_list',login_required(AdminViews.MerchantUserListView.as_view()),name="merchant_list"),
    path('merchant_update/<slug:pk>',login_required(AdminViews.MerchantUserUpdateView.as_view()),name="merchant_update"),

    # url for Adminviews.py file for Purchase Journey

    path('create_requirements/', PurchaseViews.create_requirements, name='create_requirements'),
    path('accepting_quotation/', PurchaseViews.accepting_quotation, name='accepting_quotation'),
    path('purchase_order/', PurchaseViews.purchase_order, name='purchase_order'),
    path('receiving/', PurchaseViews.receiving_invoice, name='receiving'),


    # genral admin

    path('admin/', views.adminLogin, name="admin_login"),
    path('demo', views.demoPage),
    path('demoPage', views.demoPageTemplate),
    path('admin_login_process', views.adminLoginProcess, name="admin_login_process"),
    path('admin_logout_process', views.adminLogoutProcess, name="admin_logout_process"),

    # PAGE FOR ADMIN
    path('userloginviews', UsersLoginViews.ShowLoginPage, name="show_login"),
    path('doLogin', UsersLoginViews.doLogin, name="do_login"),
    # PAGE FOR ADMIN
    path('admin_home', AdminViews.admin_home, name="admin_home"),
    path('admin_profile', AdminViews.admin_profile, name="admin_profile"),
    path('admin_profile_save', AdminViews.admin_profile_save, name="admin_profile_save"),

     # Staff Login URL Path
    path('staff_home', StaffViews.staff_home, name="staff_home"),

    # merchant Login URL Path
    path('merchant_home', MerchantViews.merchant_home, name="merchant_home"),

    # customer Login URL Path
    path('customer_home', CustomerViews.customer_home, name="customer_home"),


    # Multiusers Sign Up URL Path---

    path('signup_admin', UsersLoginViews.signup_admin, name="signup_admin"),
    path('signup_customer', UsersLoginViews.signup_student, name="signup_customer"),
    path('signup_staff', UsersLoginViews.signup_staff, name="signup_staff"),
    path('signup_merchant', UsersLoginViews.signup_merchant, name="signup_merchant"),

    path('do_admin_signup', UsersLoginViews.do_admin_signup, name="do_admin_signup"),
    path('do_merchant_signup', UsersLoginViews.do_merchant_signup, name="do_merchant_signup"),


    path('admin_fcmtoken_save', AdminViews.admin_fcmtoken_save, name="admin_fcmtoken_save"),
    path('firebase-messaging-sw.js', views.showFirebaseJS, name="show_firebase_js"),



]
