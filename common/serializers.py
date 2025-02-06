from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
)
from djoser.serializers import UserCreateSerializer

from case.models import Case
from common.enums import UserTypeChoices, RoleChoices
from common.models import User
from organization.models import OrganizationUser, Organization


class ListSerializer(ModelSerializer):

    class Meta:
        ref_name = ""
        fields = (
            "id",
            "slug",
        )
        read_only_fields = ("id", "slug")


class OrganizationUserListSerializer(ModelSerializer):
    class Meta:
        model = OrganizationUser
        ref_name = "OrganizationUserList"
        fields = [
            "id",
            "alias",
        ]
        read_only_fields = [
            "id",
            "alias",
        ]


class CommonUserSerializer(UserCreateSerializer):
    phone = serializers.CharField(max_length=24, required=False)
    profile_image = serializers.ImageField(required=False)
    user_type = serializers.ChoiceField(
        choices=UserTypeChoices.choices,
        default=UserTypeChoices.SERVICE_HOLDER,
        required=False,
    )

    class Meta(UserCreateSerializer.Meta):
        fields = [
            "email",
            "phone",
            "first_name",
            "last_name",
            "profile_image",
            "user_type",
        ]


class CommonUserWithIdSerializer(UserCreateSerializer):
    phone = serializers.CharField(max_length=24, required=False)
    profile_image = serializers.ImageField(required=False)
    user_type = serializers.ChoiceField(
        choices=UserTypeChoices.choices,
        default=UserTypeChoices.SERVICE_HOLDER,
        required=False,
    )

    class Meta(UserCreateSerializer.Meta):
        fields = [
            "id",
            "alias",
            "email",
            "phone",
            "first_name",
            "last_name",
            "profile_image",
            "user_type",
        ]


class CommonUserWithPasswordSerializer(UserCreateSerializer):
    phone = serializers.CharField(max_length=24, required=False)
    profile_image = serializers.ImageField(required=False)
    user_type = serializers.ChoiceField(
        choices=UserTypeChoices.choices,
        default=UserTypeChoices.SERVICE_HOLDER,
        required=False,
    )

    class Meta(UserCreateSerializer.Meta):
        fields = [
            "email",
            "phone",
            "password",
            "first_name",
            "last_name",
            "profile_image",
            "user_type",
        ]


class CommonOrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = [
            "alias",
            "email",
            "name",
            "logo",
            "profile_image",
            "hero_image",
        ]


class CommonCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Case
        fields = [
            "alias",
            "name",
            "case_category",
            "applicant_type",
            "case_status",
            "case_stage",
            "created_at",
        ]
