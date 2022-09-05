from .models import Reservation, User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm


class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "phone", "password1", "password2"]

class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ["date"]