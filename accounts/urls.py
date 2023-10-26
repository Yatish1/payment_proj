from django.urls import path
from accounts import views

app_name="accounts"

urlpatterns = [
    path('',views.ulogin,name='ulogin'),
    path('register/',views.register,name='register'),
]