from django.db import transaction
from rest_framework import serializers
from authentication.models import User
from organization.models import OrganizationUser
from common.enums import RoleChoices, UserTypeChoices


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    alias = serializers.UUIDField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "alias",
            "email",
            "first_name",
            "last_name",
            "phone",
            "password",
            "user_type",
        ]
        read_only_fields = ["user_type"]

    def create(self, validated_data):
        # Create a new user with the provided data
        user = User.objects.create_user(
            email=validated_data["email"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            phone=validated_data.get("phone", ""),
            password=validated_data["password"],
        )
        return user


class OrganizationUserListCreateSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    alias = serializers.UUIDField(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = OrganizationUser
        fields = [
            "alias",
            "user",
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
            "created_at",
        ]
        read_only_fields = [
            "alias",
            "official_email",
            "official_phone",
            "created_by",
            "role",
            "created_at",
        ]

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop("user")

        # Create or update the user
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # Map role to user_type
        role_to_user_type_map = {
            RoleChoices.LEAD: UserTypeChoices.LEAD,
            RoleChoices.CLIENT: UserTypeChoices.CLIENT,
            RoleChoices.ADVISOR: UserTypeChoices.ADVISOR,
            RoleChoices.INTRODUCER: UserTypeChoices.INTRODUCER,
        }
        user.user_type = role_to_user_type_map.get(
            validated_data.get("role", None), user.user_type
        )
        user.save()

        # Get the organization from the request's context
        organization_user = self.context["request"].user.organization_users.first()
        if not organization_user:
            raise serializers.ValidationError(
                "User is not associated with any organization."
            )
        organization = organization_user.organization

        # Set official_email and official_phone based on user data
        validated_data["official_email"] = user.email
        validated_data["official_phone"] = user.phone

        # Remove 'organization' from validated_data if present
        validated_data.pop("organization", None)

        # Create OrganizationUser
        return OrganizationUser.objects.create(
            user=user,
            organization=organization,  # Set the organization based on the user's organization
            role=validated_data.get("role", ""),
            created_by=self.context[
                "request"
            ].user,  # Set the user who created this entry
            official_email=user.email,
            official_phone=user.phone,
            designation=validated_data.get("designation", ""),
            permanent_address=validated_data.get("permanent_address", ""),
            present_address=validated_data.get("present_address", ""),
            dob=validated_data.get("dob", ""),
            gender=validated_data.get("gender", ""),
            joining_date=validated_data.get("joining_date", ""),
            registration_number=validated_data.get("registration_number", ""),
            degree=validated_data.get("degree", ""),
        )


class UserRetrieveUpdateDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "profile_image",
            "nid",
            "user_type",
            "city",
            "state",
            "country",
            "zip_code",
            "address",
        ]

    def update(self, instance, validated_data):
        # Handle updating the user fields, including special logic for `address`
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class OrganizationUserRetrieveUpdateDeleteSerializer(serializers.ModelSerializer):
    user = UserRetrieveUpdateDeleteSerializer(write_only=True)
    user_details = UserSerializer(read_only=True, source="user")
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = OrganizationUser
        fields = [
            "alias",
            "user",
            "user_details",
            "role",
            "designation",
            "official_email",
            "official_phone",
            "permanent_address",
            "present_address",
            "dob",
            "joining_date",
            "registration_number",
            "degree",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "alias",
            "user_details",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]

    def update(self, instance, validated_data):
        # Extract user data and update using UserRetrieveUpdateDeleteSerializer
        user_data = validated_data.pop("user", {})
        if user_data:
            user_serializer = UserRetrieveUpdateDeleteSerializer(
                instance.user, data=user_data, partial=True
            )
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        # Update the OrganizationUser fields
        if "permanent_address" in validated_data:
            instance.user.address = validated_data[
                "permanent_address"
            ]  # Update `address` in User
            instance.user.save()

        # Set the `updated_by` field to the current authenticated user (request.user)
        instance.updated_by = self.context["request"].user

        # Update OrganizationUser fields and save
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance
