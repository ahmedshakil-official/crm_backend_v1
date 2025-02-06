from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    get_object_or_404,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from organization.models import Organization, Network, NetworkUser
from organization.serializers import OrganizationSerializer


class UserOrganizationListAPIView(ListAPIView):
    """
    ListAPIView to retrieve the logged-in user's organization.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = OrganizationSerializer

    def get_queryset(self):
        """
        Return the organization associated with the logged-in user.
        """
        return Organization.objects.filter(organization_users__user=self.request.user)


class UserOrganizationRetrieveAPIView(RetrieveAPIView):
    """
    RetrieveAPIView to get the organization details for the logged-in user.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = OrganizationSerializer

    def get_object(self):
        """
        Return the organization associated with the logged-in user or raise 404.
        """
        return get_object_or_404(
            Organization, organization_users__user=self.request.user
        )


class OrganizationListCreateApiView(ListCreateAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["name", "email", "primary_mobile"]

    def get_queryset(self):
        """
        Filter organizations based on the network of the logged-in user.
        If the user has no network, return an empty queryset.
        """
        user_network = Network.objects.filter(
            network_users__user=self.request.user
        ).first()
        if user_network:
            return Organization.objects.filter(network=user_network, is_removed=False)
        return Organization.objects.none()

    def perform_create(self, serializer):
        """
        Automatically set the network field from the request.user's network.
        If the user has no network, do not assign any network.
        """
        user_network = Network.objects.filter(
            network_users__user=self.request.user
        ).first()
        serializer.save(network=user_network if user_network else None)


class OrganizationRetrieveUpdateDestroyApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = OrganizationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "slug"

    def get_queryset(self):
        """
        Filter organizations based on the network of the logged-in user.
        If the user has no network, return an empty queryset.
        """
        user_network = Network.objects.filter(
            network_users__user=self.request.user
        ).first()
        if user_network:
            return Organization.objects.filter(network=user_network)
        return Organization.objects.none()

    def perform_destroy(self, instance):
        """
        Perform a soft delete by setting the `is_removed` field to True.
        """
        instance.is_removed = True
        instance.save()

    def perform_update(self, serializer):
        """
        Ensure the `network` field remains consistent with the user's network on update.
        """
        user_network = Network.objects.filter(
            network_users__user=self.request.user
        ).first()
        serializer.save(network=user_network if user_network else None)
