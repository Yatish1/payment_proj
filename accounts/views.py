from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from accounts.forms import user_form
from django.contrib.auth import authenticate,login
from django.contrib import messages

# Create your views here.


# def ulogin(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")
#         try:
#             user = authenticate(username=username, password=password)
#             print(user)
#             if user: # if there is a user
#                 login(request, user)
#                 messages.success(request, "You are logged.")
#                 return HttpResponseRedirect("dashboard")
#             else:
#                 messages.warning(request, "Invalid Username or password")
#                 return redirect("ulogin")
#         except:
#             messages.warning(request, "User does not exist")
#     return render(request,"ulogin.html")

def ulogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, "You are logged in.")  # Success message
                return redirect("bankaccounts:account")
            else:
                messages.error(request, "User is inactive.")  # Error message
        else:
            messages.error(request, "Please check your credentials.")  # Error message
    
    return render(request, "ulogin.html", {})

    
def register(request):    
    registered = False
    
    if request.method == "POST":
        form = user_form(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Hey {username}, your account was created successfully.")
    else:
        form = user_form()
    return render(request,"register.html",{'form':form})

