from django.urls import path
from .views import login_view, doLogin_view, Logout_view, register_client_view, register, client_view

urlpatterns = [
    path("", login_view, name = "login_path"),
    path('doLogin', doLogin_view, name = "doLogin_path"),
    path('Logout', Logout_view, name = "Logout_path"),
    path('client/', client_view, name = "client_path"),

    path('register_client', register_client_view, name = "register_client_path"),
    path('register', register, name = "register_path"),

]
