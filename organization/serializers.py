from common.serializers import ListSerializer
from organization.models import Organization


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
            "is_staff"
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
