from django.db import transaction
from rest_framework import serializers
from rest_framework.serializers import (
    ModelSerializer,
)
from djoser.serializers import UserCreateSerializer

from case.models import Case
from case.utils import get_random_string
from common.enums import UserTypeChoices
from common.models import User
from organization.models import OrganizationUser, Organization, Network


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
            "alias",
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
        default=UserTypeChoices.LEAD,
        required=False,
    )

    class Meta(UserCreateSerializer.Meta):
        fields = [
            "email",
            "phone",
            "title",
            "first_name",
            "middle_name",
            "last_name",
            "profile_image",
            "user_type",
        ]

    def validate(self, attrs):
        if not attrs.get("password"):
            attrs["password"] = get_random_string(8)
        return super().validate(attrs)

    def create(self, validated_data):
        user = super().create(validated_data)

        return user


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


class CommonNetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = [
            "alias",
            "slug",
            "name",
            "email",
            "logo",
            "profile_image",
            "hero_image",
            "primary_mobile",
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
