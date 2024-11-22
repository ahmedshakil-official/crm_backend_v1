from django.db.models import Q
from rest_framework import serializers

from authentication.models import User
from common.serializers import ListSerializer, OrganizationUserListSerializer, CommonUserSerializer
from organization.models import Organization, OrganizationUser


class OrganizationSerializer(ListSerializer):
    class Meta:
        model = Organization

        fields = [
            "slug",
            "name",
            "email",
            "logo",
            "profile_image",
            "hero_image",
            "primary_mobile",
            "other_contact",
            "contact_person",
            "contact_person_designation",
            "website",
            "license_no",
            "license_image",
            "is_removed",
            "is_approved",
            "is_active",
            "is_staff",
        ]

        read_only_fields = [
            "id",
            "slug",
            "is_removed",
            "is_approved",
            "is_active",
            "is_staff",
        ]

        extra_kwargs = {
            "logo": {"required": False, "allow_null": True},
            "profile_image": {"required": False, "allow_null": True},
            "hero_image": {"required": False, "allow_null": True},
            "other_contact": {"required": False, "allow_null": True},
            "contact_person": {"required": False, "allow_null": True},
            "contact_person_designation": {"required": False, "allow_null": True},
            "website": {"required": False, "allow_null": True},
            "license_no": {"required": False, "allow_null": True},
            "license_image": {"required": False, "allow_null": True},
        }


class OrganizationUserSerializer(OrganizationUserListSerializer):
    user_detail = CommonUserSerializer(read_only=True, source="user")  # Nested serializer for user details
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)  # Accepts user ID only during creation
    created_by = CommonUserSerializer(read_only=True)
    updated_by = CommonUserSerializer(read_only=True)
    class Meta(OrganizationUserListSerializer.Meta):
        model = OrganizationUser
        fields = OrganizationUserListSerializer.Meta.fields + [
            "user",  # This is the user ID field (write-only)
            "user_detail",  # This will show the user details in the response
            "organization",  # Automatically set, will be read-only
            "role",
            "designation",
            "official_email",
            "official_phone",
            "permanent_address",
            "present_address",
            "dob",
            "gender",
            "joining_date",
            "registration_number",
            "degree",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = OrganizationUserListSerializer.Meta.read_only_fields + [
            "organization",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        extra_kwargs = {
            "designation": {"required": False, "allow_null": True},
            "official_email": {"required": False, "allow_null": True},
            "official_phone": {"required": False, "allow_null": True},
            "permanent_address": {"required": False, "allow_null": True},
            "present_address": {"required": False, "allow_null": True},
            "dob": {"required": False, "allow_null": True},
            "joining_date": {"required": False, "allow_null": True},
            "registration_number": {"required": False, "allow_null": True},
            "degree": {"required": False, "allow_null": True},
        }

    def get_fields(self):
        fields = super().get_fields()

        # Limit user selection to request user's users or their organization's users
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user_organizations = Organization.objects.filter(
                organization_users__user=request.user
            )
            fields["user"].queryset = User.objects.filter(
                Q(organization_users__organization__in=user_organizations) |
                Q(created_by=request.user)
            ).distinct()
        return fields