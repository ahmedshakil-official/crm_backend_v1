from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, RetrieveAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from organization.models import Organization
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
        return get_object_or_404(Organization, organization_users__user=self.request.user)
