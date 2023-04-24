import dateutil.parser as dp
import json
import qrcode
import tempfile
import pytz
import pyrebase

from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import JsonResponse
from django.core.files.images import ImageFile

from istudio.core.models import Reservation
from istudio.core.forms import ReservationForm, UserRegisterForm

config = {
  "apiKey": "AIzaSyDVoPt75RpCkReVnf04O9mO1d94f5p8VeI",
  "authDomain": "istudio-70ff0.firebaseapp.com",
  "databaseURL": "https://istudio-70ff0-default-rtdb.firebaseio.com",
  "projectId": "istudio-70ff0",
  "storageBucket": "istudio-70ff0.appspot.com",
  "messagingSenderId": "17753533532",
  "appId": "1:17753533532:web:9603dc3a94d0cd4c99ca99",
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database = firebase.database()

days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
months = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


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
            # database.child("appointments").push(str(reservation.date.split(":")[0]))
            database.child("appointments").child(str(reservation.date.split(":")[0])).set(str(reservation.user))
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
        {
            "user": user,
            "hydrate": {
                "booked_intervals": booked_invervals
            },
        },
    )


def qr(request, date):
    print(type(date))
    reservation = Reservation.objects.get(user=request.user, date=date)
    utc_date = dp.parse(date)
    eet = pytz.timezone('Europe/Bucharest')
    date = utc_date.astimezone(eet)
    time = f"{days[date.weekday()]}, {date.day} {months[date.month]} {date.year} at {date.time()}, {eet} time"
    return render(
        request,
        "qr.html",
        {
            "qr": reservation.qr.path.split("static", 1)[1],
            "code": int(date.timestamp()),
            "time": time,
        },
    )
