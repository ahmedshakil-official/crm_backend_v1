from django.db import models
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from common.enums import UserTypeChoices
from organization.models import Organization, OrganizationUser
from organization.serializers import OrganizationUserSerializer
from .serializers import (
    OrganizationUserListCreateSerializer,
    OrganizationUserRetrieveUpdateDeleteSerializer,
)


class AuthenticationRequiredMixin:
    """Mixin to handle authentication checks"""

    def check_authentication(self):
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated.")

    def get_user_organization(self):
        self.check_authentication()
        organization = Organization.objects.filter(
            organization_users__user=self.request.user
        ).first()
        if not organization:
            raise PermissionDenied(
                "You cannot perform this action without being associated with an organization."
            )
        return organization


class BaseOrganizationUserView:
    """Base class containing common functionality for organization user views"""
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_base_queryset(self):
        self.check_authentication()
        user_organizations = Organization.objects.filter(
            organization_users__user=self.request.user
        )
        return OrganizationUser.objects.filter(
            organization__in=user_organizations
        ).select_related("organization", "user", "created_by", "updated_by")


class OrganizationUserListCreateView(AuthenticationRequiredMixin, BaseOrganizationUserView, ListCreateAPIView):
    """Generic view for listing and creating organization users without role restriction"""
    serializer_class = OrganizationUserSerializer

    def get_queryset(self):
        return self.get_base_queryset()

    def perform_create(self, serializer):
        organization = self.get_user_organization()
        serializer.save(
            organization=organization,
            created_by=self.request.user,
            updated_by=self.request.user,
        )


class OrganizationUserRetrieveUpdateDeleteView(AuthenticationRequiredMixin, BaseOrganizationUserView,
                                               RetrieveUpdateDestroyAPIView):
    """Generic view for retrieving, updating and deleting organization users without role restriction"""
    serializer_class = OrganizationUserSerializer

    def get_queryset(self):
        return self.get_base_queryset()

    def perform_update(self, serializer):
        self.check_authentication()
        serializer.save(updated_by=self.request.user)


class BaseRoleSpecificView:
    """Base class for role-specific views"""
    role = None  # Must be set by subclasses

    def get_role_filtered_queryset(self):
        base_queryset = self.get_base_queryset()
        return base_queryset.filter(role=self.role)


class RoleSpecificListCreate(BaseRoleSpecificView, OrganizationUserListCreateView):
    serializer_class = OrganizationUserListCreateSerializer

    def get_queryset(self):
        return self.get_role_filtered_queryset()

    def perform_create(self, serializer):
        organization = self.get_user_organization()
        serializer.save(
            role=self.role,
            organization=organization,
            created_by=self.request.user,
        )


class RoleSpecificRetrieveUpdateDelete(BaseRoleSpecificView, OrganizationUserRetrieveUpdateDeleteView):
    serializer_class = OrganizationUserRetrieveUpdateDeleteSerializer

    def get_queryset(self):
        return self.get_role_filtered_queryset()


# Role-specific view implementations
class LeadListCreateView(RoleSpecificListCreate):
    role = UserTypeChoices.LEAD


class LeadRetrieveUpdateDeleteView(RoleSpecificRetrieveUpdateDelete):
    role = UserTypeChoices.LEAD


class ClientListCreateView(RoleSpecificListCreate):
    role = UserTypeChoices.CLIENT


class ClientRetrieveUpdateDeleteView(RoleSpecificRetrieveUpdateDelete):
    role = UserTypeChoices.CLIENT


class IntroducerListCreateView(RoleSpecificListCreate):
    role = UserTypeChoices.INTRODUCER


class IntroducerRetrieveUpdateDeleteView(RoleSpecificRetrieveUpdateDelete):
    role = UserTypeChoices.INTRODUCER


class AdvisorListCreateView(RoleSpecificListCreate):
    role = UserTypeChoices.ADVISOR


class AdvisorRetrieveUpdateDeleteView(RoleSpecificRetrieveUpdateDelete):
    role = UserTypeChoices.ADVISOR
