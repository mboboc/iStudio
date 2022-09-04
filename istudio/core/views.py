from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from istudio.core.forms import UserRegisterForm
from django.shortcuts import render


class SignupView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    form_class = UserRegisterForm


def home(request):
    user = request.user
    return render(request, "home.html", {"user": user})
