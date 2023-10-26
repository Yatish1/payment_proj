from django.urls import path
from bankaccounts import views


app_name = 'bankaccounts'

urlpatterns = [
    path('',views.KYC_reg,name="KYC"),
    path('logout/',views.ulogout, name='logout'),
    path('account/',views.account, name='account'), 
    path('dashboard/',views.dashboard, name='dashboard'), 
    path('transaction_details/<transaction_id>/',views.transaction_details,name="transaction_details"),
]