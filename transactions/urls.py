from django.urls import path
from transactions import transfer,payment_request,credit_card

app_name = 'transaction'

urlpatterns = [
    path('',transfer.search_user_by_acc_num,name='transfer'),
    path('amount_transfer/<account_number>/',transfer.amount_transfer,name='amount_transfer'),
    path('amount_transfer_process/<account_number>/', transfer.amount_transfer_process, name='amount_transfer_process'),
    path('transfer_confirmation/<account_number>/<transaction_id>/', transfer.transfer_confirmation, name='transfer_confirmation'),
    path('transfer_process/<account_number>/<transaction_id>/', transfer.transfer_process, name='transfer_process'),
    path('transfer_completed/<account_number>/<transaction_id>/',transfer.transfer_completed,name="transfer_completed"),
    path('user_request_payment/',payment_request.payment_request,name='payment_request'),
    path('request_amount/<account_number>/',payment_request.request_amount,name='request_amount'),
    path('request_amount_confirmation/<account_number>/<transaction_id>/',payment_request.request_amount_confirmation,name='request_amount_confirmation'),
    path('request_confirmation_success/<account_number>/<transaction_id>/',payment_request.request_confirmation_success,name='request_confirmation_success'),
    path('transaction_list/',transfer.transaction_list,name='transaction_list'),
    path('send_confirmation/<account_number>/',payment_request.send_confirmation,name='send_confirmation'),
    path('send_completed/<account_number>/<transaction_id>/',payment_request.send_process,name='send_completed'),
    path('send_amount_completed/<account_number>/<transaction_id>/',payment_request.send_amount_completed,name='send_amount_completed'),
    path('credit_card_details/<number>/',credit_card.credit_card,name="credit_card"),
    path('credit_card_bill/<card_id>/',credit_card.credit_card_bill,name="credit_card_bill"),
    path('withdraw_amount/<card_id>/',credit_card.withdraw_amount,name='withdraw_amount'),
    path('credit_card_delete/<card_id>/',credit_card.credit_card_delete,name='credit_card_delete'),
]