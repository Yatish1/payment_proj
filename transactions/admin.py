from django.contrib import admin
from transactions.models import Transaction,CreditCard
# Register your models here.

class Tadmin(admin.ModelAdmin):
    list_display = ['user', 'amount','status','transaction_type','receiver','sender']

admin.site.register(Transaction,Tadmin)

class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'amount', 'number', 'month', 'year', 'card_type', 'card_status')

admin.site.register(CreditCard, CreditCardAdmin)