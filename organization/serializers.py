from django.db.models import Q
from rest_framework import serializers

from authentication.models import User
from common.serializers import (
    ListSerializer,
    OrganizationUserListSerializer,
    CommonUserSerializer,
)
from organization.models import Organization, OrganizationUser, Network, NetworkUser


class NetworkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Network
        fields = [
            "slug",
            "name",
            "email",
            "logo",
            "profile_image",
            "hero_image",
            "primary_mobile",
        ]


class OrganizationSerializer(serializers.ModelSerializer):
    network = NetworkSerializer(read_only=True)

    class Meta:
        model = Organization
        fields = [
            "slug",
            "network",
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
    user_detail = CommonUserSerializer(read_only=True, source="user")
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )
    created_by = CommonUserSerializer(read_only=True)
    updated_by = CommonUserSerializer(read_only=True)

    class Meta(OrganizationUserListSerializer.Meta):
        model = OrganizationUser
        fields = OrganizationUserListSerializer.Meta.fields + [
            "user",
            "user_detail",
            "organization",
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
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user_organizations = Organization.objects.filter(
                organization_users__user=request.user
            )
            fields["user"].queryset = User.objects.filter(
                Q(organization_users__organization__in=user_organizations)
                | Q(created_by=request.user)
            ).distinct()
        return fields


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
            "user_detail",
            "network",
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
            # Get users from network's organizations or direct network users
            user_networks = Network.objects.filter(network_users__user=request.user)

            # Users from organizations within the network + direct network users
            fields["user"].queryset = User.objects.filter(
                Q(organization_users__organization__network__in=user_networks)
                | Q(network_users__network__in=user_networks)
                | Q(created_by=request.user)
            ).distinct()
        return fields


class NetworkUserListCreateSerializer(NetworkUserListSerializer):
    """Serializer for creating NetworkUsers with specific roles"""

    class Meta(NetworkUserListSerializer.Meta):
        fields = NetworkUserListSerializer.Meta.fields + ["user"]
        extra_kwargs = {
            "user": {"write_only": True},
        }


class NetworkUserRetrieveUpdateDeleteSerializer(NetworkUserSerializer):
    """Serializer for retrieving, updating, and deleting NetworkUsers"""

    pass
