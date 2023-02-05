import json
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password, **kwargs):
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        return self.create_user(email, password, **kwargs)


class User(AbstractUser):
    name = models.CharField(max_length=100, blank=True)
    username = None
    ordering = ("email",)
    email = models.EmailField(("email address"), unique=True)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

class Reservation(models.Model):
    user = models.ForeignKey("User", null=True, blank=True, on_delete=models.CASCADE)
    date = models.CharField(max_length=100, unique=True)
    qr = models.ImageField(blank=True, null=True, upload_to='static/qrcodes')
