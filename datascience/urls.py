from django.urls import path
from datascience import views

app_name='datascience'

urlpatterns = [
    path('chart/', views.chart_select_view),
    path('add_purchase/', views.add_purchase_view, name='add_purchase'),

]