import json
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from istudio.core.forms import ReservationForm, UserRegisterForm
from django.shortcuts import render
from django.http import JsonResponse

from istudio.core.models import Reservation


class SignupView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    form_class = UserRegisterForm


def home(request):
    user = request.user
    booked_invervals = list(Reservation.objects.all().values_list("date", flat=True))
    print(booked_invervals)
    if request.method == "POST":
        form = ReservationForm(json.loads(request.body.decode("utf-8")))
        form.user = user

        if form.is_valid():
            try:
                form.save()
                return JsonResponse({"ok": True})
            except:
                return JsonResponse({"ok": False})
        else:
            return JsonResponse({"error": "Form not valid"}, status=400)
    return render(
        request,
        "home.html",
        {"user": user, "hydrate": {"booked_intervals": booked_invervals}},
    )


def qr(request):
    return render(request, "qr.html", {})
