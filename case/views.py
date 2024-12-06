from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated

from organization.models import Organization
from .models import Case
from .serializers import CaseListCreateSerializer, CaseRetrieveUpdateDeleteSerializer


class CaseListCreateApiView(ListCreateAPIView):
    serializer_class = CaseListCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Get the organization associated with the user
        organization = get_object_or_404(Organization, organization_users__user=self.request.user)
        return Case.objects.filter(organization=organization, is_removed=False)

    def perform_create(self, serializer):
        # Get the organization associated with the user
        organization = get_object_or_404(Organization, organization_users__user=self.request.user)
        serializer.save(
            organization=organization,
            created_by=self.request.user,
        )

    def get_serializer_context(self):
        # Add the request to the serializer context to allow dynamic queryset for 'lead' field
        context = super().get_serializer_context()
        context['request'] = self.request
        return context

class CaseRetrieveUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = CaseRetrieveUpdateDeleteSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_queryset(self):
        # Retrieve the organization for the logged-in user
        organization = get_object_or_404(Organization, organization_users__user=self.request.user)
        return Case.objects.filter(organization=organization)

    def perform_update(self, serializer):
        instance = serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_removed = True
        instance.updated_by = self.request.user
        instance.save()
