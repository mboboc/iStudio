from django.urls import path
from django.contrib.auth import views as auth_views
from django_email_verification import urls as email_urls

from . import views


urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("", views.home, name="home"),
    path(
        "login/",
        auth_views.LoginView.as_view(redirect_authenticated_user=True),
        name="login",
    ),
    path("qr", views.qr, name="qr")
]
