from django.db import models
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status, viewsets
from organization.models import Organization, OrganizationUser
from organization.serializers import OrganizationSerializer, OrganizationUserSerializer


class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.filter()  # Only fetch non-removed records
    serializer_class = OrganizationSerializer
    lookup_field = "slug"

    def destroy(self, request, *args, **kwargs):
        """
        Override the destroy method to set `is_removed` to True
        instead of deleting the object.
        """
        instance = self.get_object()
        instance.is_removed = True
        instance.save()
        return Response(
            {"detail": "Organization marked as removed."},
            status=status.HTTP_204_NO_CONTENT,
        )


class DirectorOrganizationViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_object(self):
        """
        Retrieve the logged-in user's organization.
        Assumes the user is associated with only one organization.
        """
        try:
            print("=" * 20)
            org = Organization.objects.get(organization_users__user=self.request.user)
            print(org)
            print("=" * 20)
            return Organization.objects.get(organization_users__user=self.request.user)
        except Organization.DoesNotExist:
            return None

    def retrieve(self, request, pk=None):
        """
        Retrieve the organization details.
        """
        print("=" * 20)
        org = Organization.objects.get(organization_users__user=self.request.user)
        print(org)
        organization = self.get_object()
        if not organization:
            return Response(
                {"detail": "Organization not found or removed."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = OrganizationSerializer(organization)
        return Response(serializer.data)

    def update(self, request, pk=None):
        """
        Update the organization's details.
        """
        organization = self.get_object()
        if not organization:
            return Response(
                {"detail": "Organization not found or removed."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = OrganizationSerializer(
            organization, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        """
        Soft delete the organization by setting `is_removed` to True.
        """
        organization = self.get_object()
        if not organization:
            return Response(
                {"detail": "Organization not found or already removed."},
                status=status.HTTP_404_NOT_FOUND,
            )
        organization.is_removed = True
        organization.save()
        return Response(
            {"detail": "Organization soft deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


