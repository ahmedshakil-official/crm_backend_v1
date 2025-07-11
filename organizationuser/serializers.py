from django.db import transaction
from rest_framework import serializers
from authentication.models import User
from common.serializers import CommonUserSerializer, CommonUserWithPasswordSerializer
from organization.models import OrganizationUser, NetworkUser, Network
from common.enums import OrganizationRoleChoices, NetworkRoleChoices, UserTypeChoices


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
    user = serializers.SerializerMethodField()
    alias = serializers.UUIDField(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = OrganizationUser
        fields = [
            "alias",
            "user",
            "role",
            "official_email",
            "official_phone",
            "permanent_address",
            "present_address",
            "dob",
            "gender",
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

    def get_fields(self):
        fields = super().get_fields()

        # Get the role from the request data to determine which serializer to use
        role = None
        if hasattr(self, 'initial_data') and self.initial_data:
            role = self.initial_data.get('role')

        # Use CommonUserWithPasswordSerializer for LEAD roles
        if role == OrganizationRoleChoices.LEAD or role == UserTypeChoices.LEAD:
            fields['user'] = CommonUserWithPasswordSerializer()
        else:
            fields['user'] = UserSerializer()

        return fields

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop("user")
        role = validated_data.get("role")

        # Use CommonUserWithPasswordSerializer for LEAD roles
        if role == OrganizationRoleChoices.LEAD or role == UserTypeChoices.LEAD:
            user_serializer = CommonUserWithPasswordSerializer(data=user_data)
        else:
            user_serializer = UserSerializer(data=user_data)

        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # Map role to user_type
        role_to_user_type_map = {
            OrganizationRoleChoices.LEAD: UserTypeChoices.LEAD,
            UserTypeChoices.LEAD: UserTypeChoices.LEAD,
            OrganizationRoleChoices.CLIENT: UserTypeChoices.CLIENT,
            OrganizationRoleChoices.ADVISOR: UserTypeChoices.ADVISOR,
            OrganizationRoleChoices.INTRODUCER: UserTypeChoices.INTRODUCER,
        }
        user.user_type = role_to_user_type_map.get(role, user.user_type)
        user.save()

        # Get the organization from the request's context
        organization_user = self.context["request"].user.organization_users.first()
        if not organization_user:
            raise serializers.ValidationError(
                "User is not associated with any organization."
            )
        organization = organization_user.organization

        # Create OrganizationUser
        return OrganizationUser.objects.create(
            user=user,
            organization=organization,
            role=role,
            created_by=self.context["request"].user,
            official_email=user.email,
            official_phone=user.phone,
            permanent_address=validated_data.get("permanent_address", ""),
            present_address=validated_data.get("present_address", ""),
            dob=validated_data.get("dob", ""),
            gender=validated_data.get("gender", ""),
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
            instance.user.address = validated_data["permanent_address"]
            instance.user.save()

        # Set the `updated_by` field to the current authenticated user (request.user)
        instance.updated_by = self.context["request"].user

        # Update OrganizationUser fields and save
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance


class NetworkUserListSerializer(serializers.ModelSerializer):
    """Base serializer for NetworkUser listing"""

    user_detail = CommonUserSerializer(read_only=True, source="user")
    network_detail = serializers.SerializerMethodField()

    class Meta:
        model = NetworkUser
        fields = [
            "id",
            "alias",
            "user_detail",
            "network_detail",
            "role",
            "designation",
            "official_email",
            "official_phone",
            "gender",
            "joining_date",
        ]
        read_only_fields = [
            "id",
            "alias",
            "user_detail",
            "network_detail",
        ]

    def get_network_detail(self, obj):
        return {
            "id": obj.network.id,
            "name": obj.network.name,
            "email": obj.network.email,
        }


class NetworkUserSerializer(NetworkUserListSerializer):
    """Full NetworkUser serializer with all fields"""

    user_detail = CommonUserSerializer(read_only=True, source="user")
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    created_by = CommonUserSerializer(read_only=True)
    updated_by = CommonUserSerializer(read_only=True)

    class Meta(NetworkUserListSerializer.Meta):
        model = NetworkUser
        fields = NetworkUserListSerializer.Meta.fields + [
            "user",
            "network",
            "permanent_address",
            "present_address",
            "dob",
            "registration_number",
            "degree",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = NetworkUserListSerializer.Meta.read_only_fields + [
            "network",
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
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            # Get users from the same network or users created by the requesting user
            user_networks = Network.objects.filter(network_users__user=request.user)

            fields["user"].queryset = User.objects.filter(
                Q(network_users__network__in=user_networks) | Q(created_by=request.user)
            ).distinct()
        return fields


class NetworkUserListCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating NetworkUsers with specific roles"""

    user = serializers.SerializerMethodField()
    alias = serializers.UUIDField(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = NetworkUser
        fields = [
            "alias",
            "user",
            "role",
            "official_email",
            "official_phone",
            "permanent_address",
            "present_address",
            "dob",
            "gender",
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

    def get_fields(self):
        fields = super().get_fields()

        # Get the role from the request data to determine which serializer to use
        role = None
        if hasattr(self, 'initial_data') and self.initial_data:
            role = self.initial_data.get('role')

        # Use CommonUserWithPasswordSerializer for LEAD roles
        if role == NetworkRoleChoices.LEAD or role == UserTypeChoices.LEAD:
            fields['user'] = CommonUserWithPasswordSerializer()
        else:
            fields['user'] = UserSerializer()

        return fields

    @transaction.atomic
    def create(self, validated_data):
        user_data = validated_data.pop("user")
        role = validated_data.get("role")

        # Use CommonUserWithPasswordSerializer for LEAD roles
        if role == NetworkRoleChoices.LEAD or role == UserTypeChoices.LEAD:
            user_serializer = CommonUserWithPasswordSerializer(data=user_data)
        else:
            user_serializer = UserSerializer(data=user_data)

        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        # Map role to user_type
        role_to_user_type_map = {
            NetworkRoleChoices.LEAD: UserTypeChoices.LEAD,
            UserTypeChoices.LEAD: UserTypeChoices.LEAD,
            NetworkRoleChoices.CLIENT: UserTypeChoices.CLIENT,
            NetworkRoleChoices.ADVISOR: UserTypeChoices.ADVISOR,
            NetworkRoleChoices.INTRODUCER: UserTypeChoices.INTRODUCER,
        }
        user.user_type = role_to_user_type_map.get(role, user.user_type)
        user.save()

        # Get the network from the request's context
        network_user = self.context["request"].user.network_users.first()
        if not network_user:
            raise serializers.ValidationError(
                "User is not associated with any network."
            )
        network = network_user.network

        # Create NetworkUser
        return NetworkUser.objects.create(
            user=user,
            network=network,
            role=role,
            created_by=self.context["request"].user,
            official_email=user.email,
            official_phone=user.phone,
            permanent_address=validated_data.get("permanent_address", ""),
            present_address=validated_data.get("present_address", ""),
            dob=validated_data.get("dob", ""),
            gender=validated_data.get("gender", ""),
        )


class NetworkUserRetrieveUpdateDeleteSerializer(serializers.ModelSerializer):
    """Serializer for retrieving, updating, and deleting NetworkUsers"""

    user = UserRetrieveUpdateDeleteSerializer(write_only=True)
    user_details = UserSerializer(read_only=True, source="user")
    created_by = UserSerializer(read_only=True)
    updated_by = UserSerializer(read_only=True)

    class Meta:
        model = NetworkUser
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
        # Extract user data and update
        user_data = validated_data.pop("user", {})
        if user_data:
            user_serializer = UserRetrieveUpdateDeleteSerializer(
                instance.user, data=user_data, partial=True
            )
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        # Update NetworkUser fields
        if "permanent_address" in validated_data:
            instance.user.address = validated_data["permanent_address"]
            instance.user.save()

        # Set the updated_by field
        instance.updated_by = self.context["request"].user

        # Update NetworkUser fields and save
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance