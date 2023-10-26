from django.shortcuts import render
from bankaccounts.models import Account
from django.db.models import Q
from transactions.models import Transaction
from django.shortcuts import redirect
from django.contrib import messages
# Create your views here.

def payment_request(request):
    account=Account.objects.all()
    query=request.POST.get("account_number")
    print(query)
    if query:
        account=account.filter(
            Q(account_number=query)
        ).distinct()
        
    context={
        'account':account,
        'query':query
    }
    return render(request,'payment_request/user_request_payment.html',context)

def request_amount(request,account_number):
    account=Account.objects.get(account_number=account_number)
    sender=request.user
    receiver=account.user
    sender_account=request.user.account
    receiver_account=account
    if request.method =='POST':
        amount=request.POST.get('amount-request')
        description=request.POST.get('description')
        if sender_account.account_balance > 0 and amount:
            new_transaction=Transaction.objects.create(
                description=description,
                user=request.user,
                amount=amount,
                sender_account=sender_account,
                sender=sender,
                receiver=receiver,
                receiver_account=receiver_account,
                status='request_sent',
                transaction_type='request',
            )
            new_transaction.save()
            transaction_id=new_transaction.transaction_id
            return redirect('transaction:request_amount_confirmation',account.account_number,transaction_id)
    return render(request,'payment_request/request_amount.html',{'account':account})


def request_amount_confirmation(request,account_number,transaction_id):
    try:
        account=Account.objects.get(account_number=account_number)
        transaction=Transaction.objects.get(transaction_id=transaction_id)
        # kyc=KYC.objects.get(account_number=account_number)
        print(account.pin_number)
        if request.method == 'POST':
            pin_num=request.POST.get('pin-number')
            if transaction.amount <= account.account_balance:
                if account.pin_number == pin_num:
                    print('intial balance',account.account_balance)
                    account.account_balance=account.account_balance-transaction.amount
                    account.save()
                    print('final amount',account.account_balance)
                    transaction.status='request_sent'
                    transaction.save()
                    print(transaction.status)
                    print('entered pin number',pin_num)
                    return redirect('transaction:request_confirmation_success',account.account_number,transaction.transaction_id)
            else:
                print('pin number is not matching')
          
        else:
           print('insuffcient balance')
      
    except:
        messages.warning('account doesnot exit')
    context={
       'account':account,
       'transaction':transaction,
      
       }
    return render(request,'payment_request/request_amount_confirmation.html',context)  

def request_confirmation_success(request,account_number,transaction_id):
    account=Account.objects.get(account_number=account_number)
    transaction=Transaction.objects.get(transaction_id=transaction_id)
    context={
       'account':account,
       'transaction':transaction,
      
       }
    return render(request,'payment_request/request_confirmation_success.html',context)
    
def send_confirmation(request,account_number):
    account=Account.objects.get(account_number=account_number)
    sender=request.user
    receiver=account.user
    sender_account=request.user.account
    receiver_account=account
    if request.method =='POST':
        amount=request.POST.get('amount-send')
        description=request.POST.get('description')
        if sender_account.account_balance > 0 and amount:
            new_transaction=Transaction.objects.create(
                description=description,
                user=request.user,
                amount=amount,
                sender_account=sender_account,
                sender=sender,
                receiver=receiver,
                receiver_account=receiver_account,
                status='request_sent',
                transaction_type='request',
            )
            new_transaction.save()
            transaction_id=new_transaction.transaction_id
            return  redirect('transaction:send_completed',account.account_number,transaction_id)
    return render(request,"payment_request/send_confirmation.html")

def send_process(request,account_number,transaction_id):
    account = Account.objects.get(account_number=account_number)
    transaction = Transaction.objects.get(transaction_id=transaction_id)

    sender = request.user
    sender_account = request.user.account

    if request.method == "POST":
        pin_number = request.POST.get("pin-number")
        if pin_number == request.user.account.pin_number:
            if sender_account.account_balance <= 0 or sender_account.account_balance < transaction.amount:
                messages.warning(request,"Insufficient Funds,fund your account and try again.")
            else:
                sender_account.account_balance -= transaction.amount
                sender_account.save()

                account.account_balance += transaction.amount
                account.save()

                transaction.status = "request_settled"
                transaction.save()

                messages.success(request,f"Settled to { account.user.kyc.full_name } was successfull")
                return redirect("transaction:send_amount_completed",account.account_number,transaction.transaction_id)
        else:
            messages.warning(request,"Incorrect Pin")
            return redirect("transaction:send_confirmation",account.account_number)
    else:
        messages.warning(request,"Error Occured")
        # return redirect("bankaccounts:dashboard")
    
    context={
       'account':account,
       'transaction':transaction,
    }
    return render(request,"payment_request/send_completed.html",context)

def send_amount_completed(request,account_number,transaction_id):
    account=Account.objects.get(account_number=account_number)
    transaction=Transaction.objects.get(transaction_id=transaction_id)

    sender = request.user
    sender_account = request.user.account

    context={
       'account':account,
       'transaction':transaction,
       'sender':sender,
       'sender_account':sender_account
      
       }
    return render(request,'payment_request/send_amount_completed.html',context)