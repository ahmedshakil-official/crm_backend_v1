from rest_framework import serializers

from organization.models import Organization, OrganizationUser
from .models import Case, Files
from authentication.models import User
from common.serializers import CommonUserSerializer, CommonOrganizationSerializer


class CaseListCreateSerializer(serializers.ModelSerializer):
    organization = CommonOrganizationSerializer(read_only=True)
    lead_user = CommonUserSerializer(read_only=True, source="lead")
    lead = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.none(),
        write_only=True,
        required=True,
    )
    created_by = CommonUserSerializer(read_only=True)
    updated_by = CommonUserSerializer(read_only=True)

    class Meta:
        model = Case
        fields = [
            "alias",
            "name",
            "lead",
            "lead_user",
            "organization",
            "case_category",
            "applicant_type",
            "case_status",
            "case_stage",
            "notes",
            "is_removed",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "alias",
            "name",
            "lead_user",
            "created_by",
            "is_removed",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        write_only_fields = ["lead"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically adjust the queryset for the 'lead' field based on the organization of the current user
        organization = Organization.objects.filter(
            organization_users__user=self.context["request"].user
        ).first()
        if organization:
            # Only allow users who are Leads and belong to the same organization as the current user

            self.fields["lead"].queryset = User.objects.filter(
                user_type="LEAD", organization_users__organization=organization
            )


class CaseRetrieveUpdateDeleteSerializer(serializers.ModelSerializer):
    organization = CommonOrganizationSerializer(read_only=True)
    lead_user = CommonUserSerializer(read_only=True, source="lead")
    created_by = CommonUserSerializer(read_only=True)
    updated_by = CommonUserSerializer(read_only=True)

    class Meta:
        model = Case
        fields = [
            "alias",
            "name",
            "lead_user",
            "organization",
            "case_category",
            "applicant_type",
            "case_status",
            "case_stage",
            "notes",
            "is_removed",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "alias",
            "name",
            "lead_user",
            "created_by",
            "is_removed",
            "updated_by",
            "created_at",
            "updated_at",
        ]


class FileSerializer(serializers.ModelSerializer):
    file_owner_info = CommonUserSerializer(read_only=True, source="file_owner")
    created_by = CommonUserSerializer(read_only=True)
    updated_by = CommonUserSerializer(read_only=True)
    file_owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.none(), write_only=True)

    class Meta:
        model = Files
        fields = [
            "alias",
            "file",
            "file_type",
            "file_owner",
            "file_owner_info",
            "name",
            "description",
            "special_notes",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "alias",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        write_only_fields = ["file_owner"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get the case from the context and limit the queryset for file_owner
        case = self.context.get("case")
        if case:
            lead = case.lead
            joint_users = case.joint_users.values_list("joint_user", flat=True)
            self.fields["file_owner"].queryset = User.objects.filter(
                pk__in=[lead.pk, *joint_users]
            )

    def validate_file_owner(self, value):
        # Ensure file_owner is either the lead or one of the joint users of the case
        case = self.context.get("case")
        if not case:
            raise serializers.ValidationError("Case context is not provided.")

        # Fetch the lead and joint users as user objects
        valid_owners = [case.lead] + list(
            User.objects.filter(pk__in=case.joint_users.values_list("joint_user", flat=True)))

        if value not in valid_owners:
            raise serializers.ValidationError(
                "File owner must be the lead or a joint user of this case."
            )
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        if not user or not user.is_authenticated:
            raise serializers.ValidationError(
                "User must be authenticated to create files."
            )

        validated_data["case"] = self.context["case"]
        validated_data["created_by"] = user
        validated_data["user_ip"] = self.context["request"].META.get(
            "REMOTE_ADDR", None
        )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["updated_by"] = self.context["request"].user
        validated_data["user_ip"] = self.context["request"].META.get(
            "REMOTE_ADDR", None
        )
        return super().update(instance, validated_data)
