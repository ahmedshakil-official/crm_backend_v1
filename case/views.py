from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from organization.models import Organization
from .filter import CaseFilter, FileFilter
from .models import Case, Files
from .serializers import (
    CaseListCreateSerializer,
    CaseRetrieveUpdateDeleteSerializer,
    FileSerializer,
)


class CaseListCreateApiView(ListCreateAPIView):
    serializer_class = CaseListCreateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CaseFilter

    def get_queryset(self):
        # Get the organization associated with the user
        organization = get_object_or_404(
            Organization, organization_users__user=self.request.user
        )
        return Case.objects.filter(organization=organization)

    def perform_create(self, serializer):
        # Get the organization associated with the user
        organization = get_object_or_404(
            Organization, organization_users__user=self.request.user
        )
        serializer.save(
            organization=organization,
            created_by=self.request.user,
        )

    def get_serializer_context(self):
        # Add the request to the serializer context to allow dynamic queryset for 'lead' field
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class CaseRetrieveUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = CaseRetrieveUpdateDeleteSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_queryset(self):
        # Retrieve the organization for the logged-in user
        organization = get_object_or_404(
            Organization, organization_users__user=self.request.user
        )
        return Case.objects.filter(organization=organization)

    def perform_update(self, serializer):
        instance = serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.is_removed = True
        instance.updated_by = self.request.user
        instance.save()


class FileListCreateApiView(ListCreateAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FileFilter

    def get_filterset_kwargs(self):
        kwargs = super().get_filterset_kwargs()
        kwargs["request"] = self.request
        kwargs["case"] = self.get_case()  # Ensure you pass the relevant case
        return kwargs

    def get_case(self):
        """
        Fetches and caches the case instance based on the alias in the URL.
        """
        if not hasattr(self, "_case"):
            case_alias = self.kwargs.get("case_alias")
            try:
                self._case = Case.objects.get(alias=case_alias)
            except Case.DoesNotExist:
                raise NotFound("Case not found.")
        return self._case

    def get_queryset(self):
        case = self.get_case()  # Ensure case is fetched
        return Files.objects.filter(case=case)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "case": self.get_case(),  # Use the helper method to get the case
                "request": self.request,
            }
        )
        return context


class FileRetrieveUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"  # Lookup by alias for file

    def get_object(self):
        # Fetch the case and file associated with the case_alias and alias
        case_alias = self.kwargs.get("case_alias")
        file_alias = self.kwargs.get("alias")

        # Get the case associated with the case_alias
        case = get_object_or_404(Case, alias=case_alias)

        # Fetch the file by its alias and case
        file = get_object_or_404(Files, case=case, alias=file_alias)

        return file

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update(
            {
                "case": self.get_object().case,  # Access the case associated with the file
                "request": self.request,
            }
        )
        return context

    def perform_update(self, serializer):
        # Assign updated_by on update
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        # Permanently delete the file
        instance.delete()  # This will permanently delete the file from the database

        # Return a 204 No Content response after deleting the file
        return Response(status=status.HTTP_204_NO_CONTENT)

