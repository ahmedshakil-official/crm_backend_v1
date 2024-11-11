from django.contrib import admin
from .models import Organization, OrganizationUser


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "license_no", "is_approved")
    search_fields = ("name", "email", "license_no")
    list_filter = ("is_approved", "is_active")


@admin.register(OrganizationUser)
class OrganizationUserAdmin(admin.ModelAdmin):
    list_display = (
        "get_user_first_name",
        "get_user_last_name",
        "get_organization_name",
        "role",
        "designation",
        "gender",
        "joining_date",
        "degree",
    )
    search_fields = (
        "user__first_name",
        "user__last_name",
        "organization__name",
        "role",
    )
    list_filter = (
        "gender",
        "role",
        "joining_date",
    )

    def get_user_first_name(self, obj):
        return obj.user.first_name

    get_user_first_name.short_description = "First Name"

    def get_user_last_name(self, obj):
        return obj.user.last_name

    get_user_last_name.short_description = "Last Name"

    def get_organization_name(self, obj):
        return obj.organization.name

    get_organization_name.short_description = "Organization"
