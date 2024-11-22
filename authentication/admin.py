from django.contrib import admin

from authentication.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "first_name",
        "last_name",
        "phone",
        "email",
        "country",
        "user_type",
        "created_by",
    )
    search_fields = ("first_name", "last_name", "email", "phone", "country")
    list_filter = ("user_type", "is_active", "is_staff")
