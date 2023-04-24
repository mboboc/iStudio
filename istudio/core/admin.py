from django.contrib import admin

from istudio.core.models import Reservation, User
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin


@admin.register(User)
class iStudioUserAdmin(UserAdmin):
    ordering = ["email"]


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    pass