from django.shortcuts import render,redirect
from bankaccounts.models import Account,KYC
from django.db.models import Q
from django.contrib import messages
from transactions.models import Transaction
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.

def search_user_by_acc_num(request):
    account = Account.objects.all()

    query = request.POST.get("account_number")

    if query:   
        account = account.filter(
            Q(account_number=query)
    ).distinct()

    context = {
        'account': account,
        'query':query
    }
    return render(request,'transactions/search_user_by_acc_num.html',context)

def amount_transfer(request, account_number):
    try:
        account = Account.objects.get(account_number=account_number)
    except:
        messages.warning("Account doesn't exist")
    
    context = {
        'account': account,
    
    }
    return render(request,'transactions/amount_transfer.html',context)

def amount_transfer_process(request,account_number):
    account = Account.objects.get(account_number=account_number)
    
    sender = request.user
    receiver = account.user
    sender_account = request.user.account
    receiver_account = account
    
    if request.method == 'POST':
        amount = request.POST.get('amount-send')
        description = request.POST.get('description')

        print(amount)
        print(description)

        if sender_account.account_balance > 0 and amount:
            new_transaction = Transaction.objects.create(
                user = request.user,
                amount = amount,
                description = description,
                sender_account = sender_account,  
                sender = sender,
                receiver = receiver,
                receiver_account = receiver_account,
                status = 'processing',
                transaction_type = "transfer"
            )
            new_transaction.save()

            transaction_id = new_transaction.transaction_id

            return redirect("transaction:transfer_confirmation",account.account_number,transaction_id)

    return render(request, 'transactions/amount_transfer_process.html')

def transfer_confirmation(request,account_number,transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    context = {
        'account':account,
        'transaction':transaction   
    }
    return render(request,"transactions/transfer_confirmation.html",context)

def transfer_process(request, account_number, transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    sender_account = request.user.account
    # receiver_account = account

    if request.method == "POST":
        pin_number = request.POST.get('pin-number') 
        print(pin_number)

        if pin_number == sender_account.pin_number:
            transaction.status = "completed"
            transaction.save()
            print(sender_account.account_balance)
            print(transaction.amount)
            
            sender_account.account_balance -= transaction.amount
            sender_account.save()

            account.account_balance += transaction.amount
            account.save()

            messages.success(request,"Transaction complete")
            return redirect("transaction:transfer_completed",account.account_number,transaction.transaction_id)
        else:
            messages.warning(request,"Incorrect pin")
            return redirect("transaction:transfer_confirmation",account.account_number,transaction.transaction_id)
    else:
        return redirect("transaction:transfer_confirmation",account.account_number,transaction.transaction_id)


def transfer_completed(request,account_number,transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)
    
    context = {
        'account':account,
        'transaction':transaction   
    }

    return render(request,"transactions/transfer_completed.html",context)
                
def transaction_list(request):
    sender_transaction=Transaction.objects.filter(sender=request.user, transaction_type="transfer").order_by("-id")
    receiver_transaction=Transaction.objects.filter(receiver=request.user, transaction_type="transfer").order_by("-id")
    
    request_sender_transaction=Transaction.objects.filter(sender=request.user, transaction_type="request").order_by("-id")
    request_receiver_transaction=Transaction.objects.filter(receiver=request.user, transaction_type="request").order_by("-id")

    context = {
       'sender_transaction':sender_transaction,
       'receiver_transaction':receiver_transaction,

       'request_sender_transaction':request_sender_transaction,
       'request_receiver_transaction':request_receiver_transaction,
    }
    return render(request,'transactions/transaction_list.html',context)
