from django.db import models
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from organization.models import Organization, OrganizationUser
from organization.serializers import OrganizationSerializer, OrganizationUserSerializer


class OrganizationUserListCreateView(ListCreateAPIView):
    serializer_class = OrganizationUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the user's organization(s)
        user_organizations = Organization.objects.filter(
            organization_users__user=self.request.user
        )

        # Return users created by the user or associated with their organization(s)
        return OrganizationUser.objects.filter(
            models.Q(created_by=self.request.user) |
            models.Q(organization__in=user_organizations)
        )

    def perform_create(self, serializer):
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
            updated_by=self.request.user
        )


class OrganizationUserRetrieveUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrganizationUserSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_queryset(self):
        # Similar filtering as in the ListCreateAPIView
        user_organizations = Organization.objects.filter(
            organization_users__user=self.request.user
        )

        return OrganizationUser.objects.filter(
            models.Q(created_by=self.request.user) |
            models.Q(organization__in=user_organizations)
        )

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

