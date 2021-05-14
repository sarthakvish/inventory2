from django.shortcuts import render
import pandas as pd

from datascience.forms import PurchaseForm
from datascience.models import Purchase
from datetime import datetime
from datascience.utils import get_simple_plot
from inventory_app.models import Stock, StockHistory
# Create your views here.
# def chart_select_view(request):
#     graph=None
#     error_msg=None
#     price=None
#     product_df=pd.DataFrame(Purchase.objects.all().values())
#     stock_df=pd.DataFrame(Stock.objects.all().values())
#     corr=round(stock_df['receive_quantity'].corr(stock_df['issue_quantity']),2)
#     print(stock_df)
#     if product_df.shape[0]>0:
#         price=product_df['price']
#         if request.method == 'POST':
#             chart_type = request.POST['sales']
#             date_from = request.POST['date_from']
#             date_to = request.POST['date_to']
#             product_df['date']=product_df['date'].apply(lambda x:x.strftime('%Y-%m-%d'))
#             # product_df=product_df.groupby('date', as_index=False)['total_price'].agg('sum')
#             if chart_type!= "":
#                 if date_from!="" and date_to!="":
#                     product_df=product_df[product_df['date']>date_from & (product_df['date']<date_to)]
#                     product_df = product_df.groupby('date', as_index=False)['total_price'].agg('sum')
#                     print(product_df)
#                     # function to get graph
#                 graph = get_simple_plot(chart_type, x=product_df['item_name'], y=product_df['total_price'], data=product_df, data2=stock_df)
#
#             else:
#                 error_msg = "Please select the chart type to continue"
#
#     else:
#         error_msg = 'No records found in the database'
#     context={
#         'products':product_df.to_html(),
#         'error_message':error_msg,
#         'graph':graph,
#         'price':price,
#         'corr':corr,
#     }
#     return render(request, 'datascience_html/main.html', context)

def chart_select_view(request):
    graph=None
    error_msg=None
    issue_quantity=None
    auth_user_id=request.user.id
    product_df=pd.DataFrame(StockHistory.objects.filter(auth_user_id=auth_user_id).values())
    stock_df=pd.DataFrame(Stock.objects.all().values())
    corr=round(stock_df['receive_quantity'].corr(stock_df['issue_quantity']),2)
    print(stock_df)
    if product_df.shape[0]>0:
        issue_quantity=product_df['issue_quantity']
        if request.method == 'POST':
            chart_type = request.POST['sales']
            date_from = request.POST['date_from']
            date_to = request.POST['date_to']
            product_df['last_updated']=product_df['last_updated'].apply(lambda x:x.strftime('%Y-%m-%d'))
            # product_df=product_df.groupby('date', as_index=False)['total_price'].agg('sum')
            if chart_type!= "":
                if date_from!="" and date_to!="":
                    product_df=product_df[product_df['last_updated']>date_from & (product_df['last_updated']<date_to)]
                    product_df = product_df.groupby('last_updated', as_index=False)['issue_quantity']
                    print(product_df)
                    # function to get graph
                graph = get_simple_plot(chart_type, x=product_df['item_name'], y=product_df['issue_quantity'].aggregate, data=product_df, data2=stock_df)

            else:
                error_msg = "Please select the chart type to continue"

    else:
        error_msg = 'No records found in the database'
    context={
        'products':product_df.to_html(),
        'error_message':error_msg,
        'graph':graph,
        'issue_quantity':issue_quantity,
        'corr':corr,
    }
    return render(request, 'datascience_html/main.html', context)


def add_purchase_view(request):
   form=PurchaseForm(request.POST or None)
   if form.is_valid():
       obj=form.save(commit=False)
       obj.salesman=request.user
       obj.save()
       form = PurchaseForm()
   context={
       'form':form,
   }
   return render(request, 'datascience_html/add_purchase.html', context)