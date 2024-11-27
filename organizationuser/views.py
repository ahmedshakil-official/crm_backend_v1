from django.db import models
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, NotFound

from common.enums import RoleChoices, UserTypeChoices
from common.models import User
from common.views import (
    BaseOrganizationUserListCreateView,
    BaseOrganizationUserRetrieveUpdateDeleteView,
)
from organization.models import Organization, OrganizationUser
from organization.serializers import OrganizationSerializer, OrganizationUserSerializer
from .serializers import OrganizationUserListCreateSerializer

# from organizationuser.serializers import LeadSerializer, ClientSerializer, AdvisorSerializer, IntroducerSerializer


class OrganizationUserListCreateView(ListCreateAPIView):
    serializer_class = OrganizationUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the user's organization(s)
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated.")

        user_organizations = Organization.objects.filter(
            organization_users__user=self.request.user
        )

        # Return users created by the user or associated with their organization(s)
        return OrganizationUser.objects.filter(
            models.Q(created_by=self.request.user)
            | models.Q(organization__in=user_organizations)
        )

    def perform_create(self, serializer):

        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated.")
        # Automatically assign the organization of the request user
        # Assuming a single organization for simplicity
        organization = Organization.objects.filter(
            organization_users__user=self.request.user
        ).first()

        if not organization:
            raise ValidationError("You are not associated with any organization.")

        serializer.save(
            organization=organization,
            created_by=self.request.user,
            updated_by=self.request.user,
        )


class OrganizationUserRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrganizationUserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_queryset(self):
        # Similar filtering as in the ListCreateAPIView
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated.")

        user_organizations = Organization.objects.filter(
            organization_users__user=self.request.user
        )

        return OrganizationUser.objects.filter(
            models.Q(created_by=self.request.user)
            | models.Q(organization__in=user_organizations)
        )

    def perform_update(self, serializer):
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated.")
        serializer.save(updated_by=self.request.user)


class LeadListCreateView(ListCreateAPIView):
    """
    View to list and create Leads for the authenticated user's organization.
    """

    serializer_class = OrganizationUserListCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated.")
        # Get all organizations the user is associated with
        user_organizations = Organization.objects.filter(
            organization_users__user=self.request.user
        )

        # Get Leads either created by the user or belonging to their organizations
        return OrganizationUser.objects.filter(
            models.Q(created_by=self.request.user)
            & models.Q(organization__in=user_organizations, role=RoleChoices.LEAD)
        )

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated.")
        # Ensure the user is part of at least one organization
        user_organization = Organization.objects.filter(
            organization_users__user=self.request.user
        ).first()

        if not user_organization:
            raise PermissionDenied(
                "You cannot create leads without being associated with an organization."
            )

        # Save the Lead with the organization and role
        serializer.save(
            role=RoleChoices.LEAD,
            organization=user_organization,
            created_by=self.request.user,
        )


class LeadRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific Lead.
    """

    serializer_class = OrganizationUserListCreateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated.")
        # Get all organizations the user is associated with
        user_organizations = Organization.objects.filter(
            organization_users__user=self.request.user
        )

        # Restrict access to Leads created by the user or within their organizations
        return OrganizationUser.objects.filter(
            models.Q(created_by=self.request.user)
            & models.Q(organization__in=user_organizations, role=RoleChoices.LEAD)
        )

    def perform_update(self, serializer):
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated.")
        # Set the updated_by field during updates
        serializer.save(updated_by=self.request.user)


class ClientListCreateView(ListCreateAPIView):
    """
    View to list and create Clients for the authenticated user's organization.
    """

    serializer_class = OrganizationUserListCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated.")
        # Get all organizations the user is associated with
        user_organizations = Organization.objects.filter(
            organization_users__user=self.request.user
        )

        # Get Clients either created by the user or belonging to their organizations
        return OrganizationUser.objects.filter(
            models.Q(created_by=self.request.user)
            & models.Q(organization__in=user_organizations, role=RoleChoices.CLIENT)
        )

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated.")
        # Ensure the user is part of at least one organization
        user_organization = Organization.objects.filter(
            organization_users__user=self.request.user
        ).first()

        if not user_organization:
            raise PermissionDenied(
                "You cannot create clients without being associated with an organization."
            )

        # Save the Client with the organization and role
        serializer.save(
            role=RoleChoices.CLIENT,
            organization=user_organization,
            created_by=self.request.user,
        )


class ClientRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific Client.
    """

    serializer_class = OrganizationUserListCreateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated.")
        # Get all organizations the user is associated with
        user_organizations = Organization.objects.filter(
            organization_users__user=self.request.user
        )

        # Restrict access to Clients created by the user or within their organizations
        return OrganizationUser.objects.filter(
            models.Q(created_by=self.request.user)
            & models.Q(organization__in=user_organizations, role=RoleChoices.CLIENT)
        )

    def perform_update(self, serializer):
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated.")
        # Set the updated_by field during updates
        serializer.save(updated_by=self.request.user)


class IntroducerListCreateView(ListCreateAPIView):
    """
    View to list and create Clients for the authenticated user's organization.
    """

    serializer_class = OrganizationUserListCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated.")
        # Get all organizations the user is associated with
        user_organizations = Organization.objects.filter(
            organization_users__user=self.request.user
        )

        # Get Clients either created by the user or belonging to their organizations
        return OrganizationUser.objects.filter(
            models.Q(created_by=self.request.user)
            & models.Q(organization__in=user_organizations, role=RoleChoices.INTRODUCER)
        )

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated.")
        # Ensure the user is part of at least one organization
        user_organization = Organization.objects.filter(
            organization_users__user=self.request.user
        ).first()

        if not user_organization:
            raise PermissionDenied(
                "You cannot create clients without being associated with an organization."
            )

        # Save the Client with the organization and role
        serializer.save(
            role=RoleChoices.INTRODUCER,
            organization=user_organization,
            created_by=self.request.user,
        )


class IntroducerRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific Client.
    """

    serializer_class = OrganizationUserListCreateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated.")
        # Get all organizations the user is associated with
        user_organizations = Organization.objects.filter(
            organization_users__user=self.request.user
        )

        # Restrict access to Clients created by the user or within their organizations
        return OrganizationUser.objects.filter(
            models.Q(created_by=self.request.user)
            & models.Q(organization__in=user_organizations, role=RoleChoices.INTRODUCER)
        )

    def perform_update(self, serializer):
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated.")
        # Set the updated_by field during updates
        serializer.save(updated_by=self.request.user)


class AdvisorListCreateView(ListCreateAPIView):
    """
    View to list and create Clients for the authenticated user's organization.
    """

    serializer_class = OrganizationUserListCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated.")
        # Get all organizations the user is associated with
        user_organizations = Organization.objects.filter(
            organization_users__user=self.request.user
        )

        # Get Clients either created by the user or belonging to their organizations
        return OrganizationUser.objects.filter(
            models.Q(created_by=self.request.user)
            & models.Q(organization__in=user_organizations, role=RoleChoices.ADVISOR)
        )

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated.")
        # Ensure the user is part of at least one organization
        user_organization = Organization.objects.filter(
            organization_users__user=self.request.user
        ).first()

        if not user_organization:
            raise PermissionDenied(
                "You cannot create clients without being associated with an organization."
            )

        # Save the Client with the organization and role
        serializer.save(
            role=RoleChoices.ADVISOR,
            organization=user_organization,
            created_by=self.request.user,
        )


class AdvisorRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update, or delete a specific Client.
    """

    serializer_class = OrganizationUserListCreateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated.")
        # Get all organizations the user is associated with
        user_organizations = Organization.objects.filter(
            organization_users__user=self.request.user
        )

        # Restrict access to Clients created by the user or within their organizations
        return OrganizationUser.objects.filter(
            models.Q(created_by=self.request.user)
            & models.Q(organization__in=user_organizations, role=RoleChoices.ADVISOR)
        )

    def perform_update(self, serializer):
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated.")
        # Set the updated_by field during updates
        serializer.save(updated_by=self.request.user)
