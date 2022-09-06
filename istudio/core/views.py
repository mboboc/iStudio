import json
import os
import tempfile
import qrcode
from pathlib import Path
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from istudio.core.forms import ReservationForm, UserRegisterForm
from django.shortcuts import render
from django.http import JsonResponse
import dateutil.parser as dp
from django.core.files.images import ImageFile

from istudio.core.models import Reservation

days = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
months = ['January','February','March','April','May','June','July','August','September','October','November','December'];

class SignupView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"
    form_class = UserRegisterForm


def getCode(date):
    return int(dp.parse(date).timestamp())

def home(request):
    user = request.user
    booked_invervals = list(Reservation.objects.all().values_list("date", flat=True))
    if request.method == "POST":
        form = ReservationForm(json.loads(request.body.decode("utf-8")))
        if form.is_valid():
            reservation = form.save(commit=False)
            reservation.user = user

            # Generate qr code for reservation
            with tempfile.TemporaryDirectory(dir=".") as tmpdirname:
                filename = f"reservation-{getCode(reservation.date)}.png"
                qr_path = f"{tmpdirname}/{filename}"
                qr = qrcode.make(reservation.date)
                qr.save(qr_path)
                reservation.qr = ImageFile(open(qr_path, "rb"), name=filename)

            try:
                reservation.save()
                print(f"A {reservation.date}")
                return JsonResponse({"ok": True, "date": reservation.date}, status=200)
            except Exception as e:
                print(e)
                return JsonResponse({"ok": False})
        else:
            return JsonResponse({"error": "Form not valid"}, status=400)
    return render(
        request,
        "home.html",
        {"user": user, "hydrate": {"booked_intervals": booked_invervals}},
    )


def qr(request, date):
    print(type(date))
    reservation = Reservation.objects.get(user=request.user, date=date)
    date = dp.parse(date)
    time = f"{days[date.weekday()]}, {date.day} {months[date.month]} {date.year} at {date.time()}, Europe/Bucharest time"
    return render(request, "qr.html", {"qr": reservation.qr.path.split("static", 1)[1], "code": int(date.timestamp()), "time": time})
