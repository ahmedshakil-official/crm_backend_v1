from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
)
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from authentication.models import User
from common.serializers import CommonUserSerializer, CommonUserWithIdSerializer
from organization.models import Organization
from .filter import CaseFilter, FileFilter
from .models import Case, Files, JointUser, LoanDetails, ApplicantDetails
from .serializers import (
    CaseListCreateSerializer,
    CaseRetrieveUpdateDeleteSerializer,
    FileSerializer,
    JointUserSerializer,
    CaseUserListSerializer,
    LoanDetailsSerializer,
    ApplicantDetailsSerializer,
)


class CaseListCreateApiView(ListCreateAPIView):
    serializer_class = CaseListCreateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CaseFilter
    search_fields = [
        "name",
        "case_category",
        "applicant_type",
        "case_status",
        "case_stage",
        "lead__first_name",
        "lead__last_name",
        "lead__phone",
        "lead__email",
    ]

    def get_queryset(self):
        # Get the organization associated with the user
        organization = get_object_or_404(
            Organization, organization_users__user=self.request.user
        )
        return Case.objects.select_related("organization", "lead", "created_by").filter(
            organization=organization, is_removed=False
        )

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


class JointUserListCreateApiView(ListCreateAPIView):
    serializer_class = JointUserSerializer

    def get_queryset(self):
        case_alias = self.kwargs.get("case_alias")
        case = get_object_or_404(Case, alias=case_alias)
        return JointUser.objects.filter(case=case, is_removed=False)

    def perform_create(self, serializer):
        case_alias = self.kwargs.get("case_alias")
        case = get_object_or_404(Case, alias=case_alias)
        serializer.save(case=case)


class JointUserRetrieveUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = JointUserSerializer
    lookup_field = "alias"

    def get_queryset(self):
        case_alias = self.kwargs.get("case_alias")
        case = get_object_or_404(Case, alias=case_alias)
        return JointUser.objects.filter(case=case)

    def perform_destroy(self, instance):
        instance.is_removed = True
        instance.updated_by = self.request.user
        instance.save()


class CaseUserListApiView(ListAPIView):
    serializer_class = CaseUserListSerializer

    def get_queryset(self):
        case_alias = self.kwargs["case_alias"]

        try:
            case = Case.objects.get(alias=case_alias)
        except Case.DoesNotExist:
            raise NotFound("Case not found.")

        return JointUser.objects.filter(case=case, is_removed=False)

    def list(self, request, *args, **kwargs):
        joint_users = self.get_queryset()

        case_alias = self.kwargs["case_alias"]
        try:
            case = Case.objects.get(alias=case_alias)
        except Case.DoesNotExist:
            raise NotFound("Case not found.")

        lead_user = CommonUserWithIdSerializer(case.lead).data
        joint_users_data = CaseUserListSerializer(joint_users, many=True).data

        return Response({"lead_user": lead_user, "joint_users": joint_users_data})


class LoanDetailsListCreateApiView(ListCreateAPIView):
    serializer_class = LoanDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        case_alias = self.kwargs.get("case_alias")
        case = get_object_or_404(Case, alias=case_alias)
        return LoanDetails.objects.filter(case=case)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        case_alias = self.kwargs.get("case_alias")
        case = get_object_or_404(Case, alias=case_alias)
        context.update({"case": case})
        return context

    def perform_create(self, serializer):
        case = self.get_serializer_context().get("case")
        serializer.save(created_by=self.request.user, case=case)


class LoanDetailsRetrieveUpdateApiView(RetrieveUpdateAPIView):
    serializer_class = LoanDetailsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_object(self):
        case_alias = self.kwargs.get("case_alias")
        loan_alias = self.kwargs.get("alias")
        case = get_object_or_404(Case, alias=case_alias)
        loan_details = get_object_or_404(LoanDetails, case=case, alias=loan_alias)
        return loan_details

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"case": self.get_object().case})
        return context

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class CaseUserListViewOnlyApiView(ListAPIView):
    serializer_class = CommonUserSerializer

    def get_queryset(self):
        # Retrieve the Case by alias from the URL
        case_alias = self.kwargs.get("case_alias")
        case = get_object_or_404(Case, alias=case_alias)

        # Collect user IDs from the lead and joint users
        user_ids = set()
        if case.lead:
            user_ids.add(case.lead.id)

        # Add joint_user IDs (excluding removed ones)
        joint_user_ids = case.joint_users.filter(is_removed=False).values_list(
            "joint_user_id", flat=True
        )
        user_ids.update(joint_user_ids)

        # Return a QuerySet of User objects matching the collected IDs
        return User.objects.filter(id__in=user_ids)


class ApplicantDetailsListApiView(RetrieveUpdateAPIView):

    serializer_class = ApplicantDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        case_alias = self.kwargs.get("case_alias")
        return ApplicantDetails.objects.filter(case__alias=case_alias)


class ApplicantDetailsRetrieveUpdateApiView(RetrieveUpdateAPIView):
    queryset = ApplicantDetails.objects.all()
    serializer_class = ApplicantDetailsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_object(self):
        case_alias = self.kwargs.get("case_alias")
        alias = self.kwargs.get("alias")
        return get_object_or_404(ApplicantDetails, case__alias=case_alias, alias=alias)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)
