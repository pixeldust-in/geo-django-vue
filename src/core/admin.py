from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

from core.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(DefaultUserAdmin):
    list_display = (
        "id",
        "uuid",
        "email",
        "is_staff",
        "is_active",
        "date_joined",
    )
    list_filter = ("date_joined",)
    search_fields = (
        "username",
        "email",
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Personal info", {"fields": ("email",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_superuser",
                    "is_staff",
                    "groups",
                    "user_permissions",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    ordering = ("id",)
