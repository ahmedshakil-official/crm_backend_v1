from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.db import models

from authentication.models import User
from organization.models import Organization, OrganizationUser
from organization.serializers import OrganizationUserSerializer


class BaseOrganizationUserListCreateView(ListCreateAPIView):
    """
    Base view for handling OrganizationUser creation and listing for a specific role.
    Subclasses must define `user_type` and `role` attributes.
    """
    permission_classes = [IsAuthenticated]

    user_type = None  # Subclass must define this
    role = None  # Subclass must define this

    def get_queryset(self):
        # Ensure role is not None and is valid
        if not self.role:
            raise ValidationError("Role is not defined for this view.")

        user_organizations = Organization.objects.filter(
            organization_users__user=self.request.user
        )

        return OrganizationUser.objects.filter(
            models.Q(organization__in=user_organizations) & models.Q(role=self.role)
        )

    def perform_create(self, serializer):
        organization = Organization.objects.filter(
            organization_users__user=self.request.user
        ).first()

        if not organization:
            raise ValidationError("You are not associated with any organization.")

        # Create a User and link to OrganizationUser
        user_data = self.request.data.get("user", {})
        created_user = User.objects.create(
            email=user_data.get("email"),
            first_name=user_data.get("first_name"),
            last_name=user_data.get("last_name"),
            user_type=self.user_type,
            created_by=self.request.user,
        )

        serializer.save(
            user=created_user,
            organization=organization,
            role=self.role,
            created_by=self.request.user,
            updated_by=self.request.user,
        )


class BaseOrganizationUserRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    Base view for handling OrganizationUser retrieval, update, and deletion for a specific role.
    Subclasses must define the `role` attribute.
    """
    serializer_class = OrganizationUserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    role = None  # Subclass must define this

    def get_queryset(self):
        user_organizations = Organization.objects.filter(
            organization_users__user=self.request.user
        )
        return OrganizationUser.objects.filter(
            models.Q(organization__in=user_organizations) & models.Q(role=self.role)
        )

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()
