from django.db import transaction
from rest_framework import serializers
from djoser.conf import settings
from djoser.serializers import UserCreateSerializer
from authentication.models import User
from organization.models import Organization, OrganizationUser
from common.enums import RoleChoices, UserTypeChoices
from common.serializers import CommonUserSerializer


class CustomUserCreateSerializer(UserCreateSerializer):
    # Fields for the required information during registration
    phone = serializers.CharField(max_length=24, required=False)
    profile_image = serializers.ImageField(required=False)
    user_type = serializers.ChoiceField(
        choices=UserTypeChoices.choices,
        default=UserTypeChoices.SERVICE_HOLDER,
        required=False,
    )
    created_by = CommonUserSerializer(read_only=True)
    updated_by = CommonUserSerializer(read_only=True)

    class Meta(UserCreateSerializer.Meta):
        fields = [
            "email",
            "phone",
            "first_name",
            "last_name",
            "profile_image",
            "user_type",
            "password",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        # Check if the request context has a user
        request_user = (
            self.context["request"].user if "request" in self.context else None
        )
        print("="*20)
        print(request_user)
        print("="*20)

        # Extract user data
        password = validated_data.pop("password")

        with transaction.atomic():
            # Create the user
            user = User(**validated_data)
            user.set_password(password)

            # Assign created_by only if the request user is authenticated
            if request_user and request_user.is_authenticated:
                user.created_by = request_user

            user.save()

        return user

    def update(self, instance, validated_data):
        # Check if the request context has a user
        request_user = (
            self.context["request"].user if "request" in self.context else None
        )

        with transaction.atomic():
            # Update user fields
            for attr, value in validated_data.items():
                if attr == "password":
                    instance.set_password(value)
                else:
                    setattr(instance, attr, value)

            # Assign updated_by only if the request user is authenticated
            if request_user and request_user.is_authenticated:
                instance.updated_by = request_user

            instance.save()

        return instance
