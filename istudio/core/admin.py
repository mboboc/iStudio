from django.contrib import admin

from istudio.core.models import User
from django.contrib.auth.admin import UserAdmin


@admin.register(User)
class iStudioUserAdmin(UserAdmin):
    ordering = ["email"]
