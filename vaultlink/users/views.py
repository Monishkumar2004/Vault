from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser
from django.db import IntegrityError

# Create your views here.

def login_view(request):
    return render(request, 'login.html')

def doLogin_view(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get("password")

        user = authenticate(
            request,
            email = email,
            password = password
        )

        if user is not None:

            login(request, user)
            user_type = user.user_type

            if user_type == 1:
                return render(request, 'ops_user_page.html')
            elif user_type == 2:
                return render(request, "client_page.html")
            else:
                messages.error(request, "Email or Password Invalid")
                return redirect('login_path')
        else:
            messages.error(request, "Email or Password Invalid")
            return redirect('login_path')
            

def register_client_view(request):
    return render(request, 'register_user.html')


def register(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Password do not match")
            return redirect("register_client_path")
        
        try:
            user = CustomUser(username = username, email = email)
            user.set_password(password1)
            user.save()

            messages.success(request, "Registraion Successfull. Please Login")
            return redirect("login_path")
        except IntegrityError:
            messages.error(request, "Username or Email already exists")
            return redirect('register')
        
    
    return render(request, 'register.html')




@login_required
def Logout_view(request):
    logout(request)

    return redirect('login_view')


@login_required
def ops_user_view(request):

    return render(request, 'ops_user_page.html')
