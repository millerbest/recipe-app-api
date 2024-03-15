"""Django admin customization"""

from django.contrib import admin  # noqa
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import (
    gettext_lazy as _,
)  # for future proofing (support translation in django)
from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin page for users."""

    ordering = ["id"]
    list_display = ["email", "name"]

    # The following are shown in the change page
    # first element is title, second element is a list of field names (which values to be shown in the page)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser")}),
        (
            _("Important dates"),
            {"fields": ("last_login",)},
        ),
    )
    readonly_fields = ["last_login"]

    # For adding new user
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


admin.site.register(models.User, UserAdmin)
