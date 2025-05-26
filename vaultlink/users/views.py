from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import CustomUser
from django.db import IntegrityError
from django.core.exceptions import PermissionDenied

# Create your views here.

# Anonymous required
def anonymous_required(function = None, redirect_url = None):

    if not redirect_url:
        redirect_url = 'ops_user_path'
    
    actual_decorator = user_passes_test(
        lambda u: u.is_anonymous,
        login_url=redirect_url
    )

    if function:
        return actual_decorator(function)
    return actual_decorator

@anonymous_required
def login_view(request):
    return render(request, 'login.html')


@anonymous_required
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
                return redirect('client_path')
            else:
                messages.error(request, "Email or Password Invalid")
                return redirect('login_path')
        else:
            messages.error(request, "Email or Password Invalid")
            return redirect('login_path')
            
@anonymous_required
def register_client_view(request):
    return render(request, 'register_user.html')

@anonymous_required
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

    return redirect('login_path')

# New view for client page
@login_required
def client_view(request):
    # Ensure the logged-in user is a client
    if request.user.user_type != 2:
        raise PermissionDenied("You do not have permission to access this page.")
    return render(request, 'client_page.html')


