from rest_framework import serializers

from case.models import Case
from common.serializers import CommonOrganizationSerializer, CommonUserSerializer


class CommonCaseSerializer(serializers.ModelSerializer):
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
