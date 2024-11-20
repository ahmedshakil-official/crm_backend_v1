from django.db import transaction
from rest_framework import serializers
from djoser.conf import settings
from djoser.serializers import UserCreateSerializer
from authentication.models import User
from organization.models import Organization, OrganizationUser
from common.enums import RoleChoices, UserTypeChoices


class CustomUserCreateSerializer(UserCreateSerializer):
    # Fields for the required information during registration
    phone = serializers.CharField(max_length=24, required=False)
    profile_image = serializers.ImageField(required=False)
    user_type = serializers.ChoiceField(choices=UserTypeChoices.choices, default=UserTypeChoices.SERVICE_HOLDER, required=False)

    # Additional fields for organization and role information
    organization_name = serializers.CharField(write_only=True)

    class Meta(UserCreateSerializer.Meta):
        fields = [
            'email', 'phone', 'first_name', 'last_name', 'profile_image',
            'user_type', 'password', 'organization_name'
        ]

    def create(self, validated_data):
        # Extract user and organization fields
        organization_name = validated_data.pop('organization_name')
        email = validated_data.get('email')
        phone = validated_data.get('phone')
        password = validated_data.pop('password')  # Remove password for manual handling

        # Wrap the entire operation in a transaction
        with transaction.atomic():
            # Step 1: Create and save the User, then set the password
            user = User(**validated_data)
            user.set_password(password)  # Hash and set the password
            user.save()  # Save the user instance to get an ID for foreign key use

            # Step 2: Create the Organization
            organization = Organization.objects.create(
                name=organization_name,
                email=email,
                primary_mobile=phone,
                contact_person=f"{user.first_name} {user.last_name}",
            )

            # Step 3: Create the OrganizationUser with RoleChoices.ADMIN
            OrganizationUser.objects.create(
                user=user,  # Now this user has an ID in the database
                organization=organization,
                role=RoleChoices.ADMIN,
                official_email=user.email,
                official_phone=user.phone
            )

        # Return the user after the transaction completes successfully
        return user

