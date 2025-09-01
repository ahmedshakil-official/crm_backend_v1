import io
from datetime import datetime

from django.db import transaction

from django.db.models import Q
from django.db.models.functions import Lead
from django.http import HttpResponse

from django_filters.rest_framework.backends import DjangoFilterBackend
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT

from rest_framework.filters import SearchFilter
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateAPIView,
    UpdateAPIView,
)
from django.shortcuts import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.models import User
from common.serializers import CommonUserSerializer, CommonUserWithIdSerializer
from organization.models import Organization, Network, OrganizationUser, NetworkUser
from common.enums import UserTypeChoices as CommonUserTypeChoices
from organization.permissions import CasePermission, IsInOrgOrNetwork, CasePermissionForClintUpdate
from .common import (
    RegisterLoan,
    PaymentCommitment,
    PropertyRepossessed,
    Bankrupt,
    IndividualVoluntary,
    DebtManagementPlan,
    PayDayLoan,
    CCJ,
)
from .enums import UserTypeChoices, FeesChoices
from .filter import CaseFilter, FileFilter
from .models import (
    Case,
    Files,
    JointUser,
    LoanDetails,
    ApplicantDetails,
    Dependant,
    CompanyInfo,
    DirectorShareholder,
    EmploymentDetails,
    Adverse,
    Property,
    SolicitorAccountant,
    CaseAccountant,
    CaseSolicitor,
    ExistingProtection,
    Notes,
    PropertyDetails,
    OtherOccupants,
    Product,
    BudgetPlanner,
    Fees,
    DipHistory,
    CreditCommitments,
    Suitability,
    ExtraAnswer,
    Compliance,
    MortgageNeeds,
    MortgageFeatures, ClientSurvey,
)
from .serializers import (
    CaseListCreateSerializer,
    CaseRetrieveUpdateDeleteSerializer,
    FileSerializer,
    JointUserSerializer,
    CaseUserListSerializer,
    LoanDetailsSerializer,
    ApplicantDetailsSerializer,
    DependantSerializer,
    CompanyInfoSerializer,
    DirectorShareholderSerializer,
    EmploymentDetailsSerializer,
    AdverseSerializer,
    RegisterLoanSerializer,
    PaymentCommitmentSerializer,
    PropertyRepossessedSerializer,
    BankruptSerializer,
    IndividualVoluntarySerializer,
    DebtManagementPlanSerializer,
    PayDayLoanSerializer,
    CCJSerializer,
    PropertySerializer,
    SolicitorAccountantSerializer,
    CaseSolicitorSerializer,
    CaseAccountantSerializer,
    ExistingProtectionSerializer,
    NotesSerializer,
    PropertyDetailsSerializer,
    OtherOccupantsSerializer,
    ProductSerializer,
    BudgetPlannerSerializer,
    FeesSerializer,
    DipHistorySerializer,
    CreditCommitmentsSerializer,
    SuitabilitySerializer,
    ExtraAnswerSerializers,
    ComplianceSerializers,
    MortgageNeedsSerializers, ClientSurveySerializers,
)


class CaseRelatedViewMixin:
    """
    Mixin providing common functionality for case-related views.
    Handles case retrieval and caching to avoid repetitive database queries.
    """

    def get_case(self):
        """
        Fetches and caches the case instance based on the alias in the URL.
        Raises NotFound if the case doesn't exist.
        """
        if not hasattr(self, "_cached_case"):
            case_alias = self.kwargs.get("case_alias")
            if not case_alias:
                raise NotFound("Case alias not provided in URL.")
            try:
                self._cached_case = Case.objects.get(alias=case_alias)
            except Case.DoesNotExist:
                raise NotFound("Case not found.")
        return self._cached_case

    def get_serializer_context(self):
        """Add case to serializer context if the view is case-related."""
        context = super().get_serializer_context()
        if "case_alias" in self.kwargs:
            context["case"] = self.get_case()
        return context

    def get_user_context(self):
        """
        Determines if user is associated with an organization or network.
        Returns a dict with 'type' and 'instance' keys.
        """
        user = self.request.user

        # Check if user is associated with an organization
        try:
            organization = Organization.objects.get(organization_users__user=user)
            return {"type": "organization", "instance": organization}
        except Organization.DoesNotExist:
            pass

        # Check if user is associated with a network
        try:
            network = Network.objects.get(network_users__user=user)
            return {"type": "network", "instance": network}
        except Network.DoesNotExist:
            pass

        # If neither found, raise error
        raise NotFound("User is not associated with any organization or network.")


class CaseAuthenticationMixin:
    """Mixin to handle case-specific authentication and permissions"""

    def check_authentication(self):
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated.")

    def get_user_association(self):
        """Get user's organization or network association"""
        self.check_authentication()
        user = self.request.user

        # Check organization association
        org_user = OrganizationUser.objects.filter(user=user).first()
        if org_user:
            return {
                "type": "organization",
                "organization": org_user.organization,
                "network": org_user.organization.network,
            }

        # Check network association
        network_user = NetworkUser.objects.filter(user=user).first()
        if network_user:
            return {
                "type": "network",
                "network": network_user.network,
                "organization": None,
            }

        raise PermissionDenied(
            "You cannot perform this action without being associated with an organization or network."
        )

    def get_case_queryset(self):
        """Get cases based on user association"""
        self.check_authentication()
        user_association = self.get_user_association()

        if user_association["type"] == "organization":
            # Organization users see cases from their organization
            return Case.objects.filter(
                organization=user_association["organization"]
            ).select_related(
                "organization", "network", "lead", "assigned_to", "created_by", "updated_by"
            )

        elif user_association["type"] == "network":
            # Network users see cases from their entire network
            return Case.objects.filter(
                network=user_association["network"]
            ).select_related(
                "organization", "network", "lead", "assigned_to", "created_by", "updated_by"
            )

        return Case.objects.none()


class CaseListCreateApiView(CaseAuthenticationMixin, ListCreateAPIView):
    """List and create cases for both organization and network users"""

    serializer_class = CaseListCreateSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CaseFilter
    search_fields = [
        "name",
        "lead__first_name",
        "lead__last_name",
        "lead__phone",
        "lead__email",
        "case_category",
        "case_status",
    ]
    pagination_class = PageNumberPagination

    lookup_field = "alias"

    def get_queryset(self):
        return self.get_case_queryset()

    def perform_create(self, serializer):
        user_association = self.get_user_association()

        # The serializer's create method will handle organization/network assignment
        # based on the user's association
        serializer.save()


class CaseRetrieveUpdateDeleteApiView(
    CaseAuthenticationMixin, RetrieveUpdateDestroyAPIView
):
    """Retrieve, update, and delete cases for both organization and network users"""

    serializer_class = CaseRetrieveUpdateDeleteSerializer
    permission_classes = [IsAuthenticated, CasePermission]
    lookup_field = "alias"

    def get_queryset(self):
        return self.get_case_queryset()

    def perform_update(self, serializer):
        # The serializer's update method will handle user tracking
        serializer.save()


class FileListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated, CasePermission]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FileFilter

    def get_filterset_kwargs(self):
        kwargs = super().get_filterset_kwargs()
        kwargs["request"] = self.request
        kwargs["case"] = self.get_case()
        return kwargs

    def get_queryset(self):
        return Files.objects.filter(case=self.get_case())


class FileRetrieveUpdateDeleteApiView(
    CaseRelatedViewMixin, RetrieveUpdateDestroyAPIView
):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated, CasePermission]
    lookup_field = "alias"

    def get_object(self):
        case = self.get_case()
        file_alias = self.kwargs.get("alias")
        return get_object_or_404(Files, case=case, alias=file_alias)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class JointUserListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = JointUserSerializer

    def get_queryset(self):
        return JointUser.objects.filter(case=self.get_case(), is_removed=False)

    def perform_create(self, serializer):
        serializer.save(
            case=self.get_case()
        )


class JointUserRetrieveUpdateDeleteApiView(
    CaseRelatedViewMixin, RetrieveUpdateDestroyAPIView
):
    serializer_class = JointUserSerializer
    lookup_field = "alias"

    def get_queryset(self):
        return JointUser.objects.filter(case=self.get_case())

    def perform_destroy(self, instance):
        instance.is_removed = True
        instance.updated_by = self.request.user
        instance.save()


class CaseUserListApiView(CaseRelatedViewMixin, ListAPIView):
    serializer_class = CaseUserListSerializer

    def get_queryset(self):
        return JointUser.objects.filter(case=self.get_case(), is_removed=False)

    def list(self, request, *args, **kwargs):
        joint_users = self.get_queryset()
        case = self.get_case()
        lead_user = CommonUserWithIdSerializer(case.lead).data
        joint_users_data = CaseUserListSerializer(joint_users, many=True).data
        return Response({"lead_user": lead_user, "joint_users": joint_users_data})


class LoanDetailsListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = LoanDetailsSerializer
    permission_classes = [IsAuthenticated, CasePermissionForClintUpdate]

    def get_queryset(self):
        return LoanDetails.objects.filter(case=self.get_case())

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, case=self.get_case())


class LoanDetailsRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateAPIView):
    serializer_class = LoanDetailsSerializer
    permission_classes = [IsAuthenticated, CasePermissionForClintUpdate]
    lookup_field = "alias"

    def get_object(self):
        case = self.get_case()
        loan_alias = self.kwargs.get("alias")
        return get_object_or_404(LoanDetails, case=case, alias=loan_alias)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class CaseUserListViewOnlyApiView(CaseRelatedViewMixin, ListAPIView):
    serializer_class = CommonUserWithIdSerializer

    def get_queryset(self):
        case = self.get_case()
        user_ids = set()
        if case.lead:
            user_ids.add(case.lead.id)
        joint_user_ids = case.joint_users.filter(is_removed=False).values_list(
            "joint_user_id", flat=True
        )
        user_ids.update(joint_user_ids)
        return User.objects.filter(id__in=user_ids)


class ApplicantDetailsListApiView(CaseRelatedViewMixin, ListAPIView):
    serializer_class = ApplicantDetailsSerializer
    permission_classes = [IsAuthenticated,CasePermissionForClintUpdate]

    def get_queryset(self):
        return ApplicantDetails.objects.filter(case=self.get_case())


class ApplicantDetailsRetrieveUpdateApiView(
    CaseRelatedViewMixin, RetrieveUpdateAPIView
):
    queryset = ApplicantDetails.objects.all()
    serializer_class = ApplicantDetailsSerializer
    permission_classes = [IsAuthenticated, CasePermissionForClintUpdate]
    lookup_field = "alias"

    def get_object(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return get_object_or_404(ApplicantDetails, case=case, alias=alias)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class DependantListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = DependantSerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return Dependant.objects.filter(
            applicant_details__case=case, applicant_details__alias=alias
        )

    def perform_create(self, serializer):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        applicant_details = get_object_or_404(ApplicantDetails, case=case, alias=alias)
        serializer.save(applicant_details=applicant_details)


class CompanyInfoListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = CompanyInfoSerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        case = self.get_case()
        alias = self.kwargs["alias"]
        return CompanyInfo.objects.filter(
            applicant_details__case=case, applicant_details__alias=alias
        )

    def perform_create(self, serializer):
        case = self.get_case()
        alias = self.kwargs["alias"]
        applicant_details = get_object_or_404(ApplicantDetails, case=case, alias=alias)
        serializer.save(applicant_details=applicant_details)


class DirectorShareholderListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = DirectorShareholderSerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        case = self.get_case()
        alias = self.kwargs["alias"]
        company_name = self.kwargs["company_name"]
        return DirectorShareholder.objects.filter(
            company__applicant_details__case=case,
            company__applicant_details__alias=alias,
            company__company_name=company_name,
        )

    def perform_create(self, serializer):
        case = self.get_case()
        alias = self.kwargs["alias"]
        company_name = self.kwargs["company_name"]
        company = get_object_or_404(
            CompanyInfo,
            applicant_details__case=case,
            applicant_details__alias=alias,
            company_name=company_name,
        )
        serializer.save(company=company)


class EmploymentDetailsListApiView(CaseRelatedViewMixin, ListAPIView):
    serializer_class = EmploymentDetailsSerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        return EmploymentDetails.objects.filter(case=self.get_case())


class EmploymentDetailsCreateApiView(CaseRelatedViewMixin, CreateAPIView):
    serializer_class = EmploymentDetailsSerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        return EmploymentDetails.objects.all()

    def perform_create(self, serializer):
        case = self.get_case()
        user_obj = get_object_or_404(User, pk=self.kwargs["pk"])
        serializer.save(
            case=case,
            user=user_obj,
            created_by=self.request.user,
        )


class EmploymentDetailsRetrieveUpdateApiView(
    CaseRelatedViewMixin, RetrieveUpdateAPIView
):
    serializer_class = EmploymentDetailsSerializer
    permission_classes = [IsAuthenticated, CasePermission]
    lookup_field = "alias"

    def get_queryset(self):
        return EmploymentDetails.objects.filter(case=self.get_case())

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class AdverseListApiView(CaseRelatedViewMixin, ListAPIView):
    serializer_class = AdverseSerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        return Adverse.objects.filter(case=self.get_case())


class AdverseRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateAPIView):
    serializer_class = AdverseSerializer
    permission_classes = [IsAuthenticated, CasePermission]
    lookup_field = "alias"

    def get_queryset(self):
        return Adverse.objects.filter(case=self.get_case())

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class RegisterLoanListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = RegisterLoanSerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return RegisterLoan.objects.filter(adverse__case=case, adverse__alias=alias)

    def perform_create(self, serializer):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        adverse = get_object_or_404(Adverse, case=case, alias=alias)
        serializer.save(adverse=adverse)


class CCJListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = CCJSerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return CCJ.objects.filter(adverse__case=case, adverse__alias=alias)

    def perform_create(self, serializer):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        adverse = get_object_or_404(Adverse, case=case, alias=alias)
        serializer.save(adverse=adverse)


class PaymentCommitmentListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = PaymentCommitmentSerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return PaymentCommitment.objects.filter(
            adverse__case=case, adverse__alias=alias
        )

    def perform_create(self, serializer):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        adverse = get_object_or_404(Adverse, case=case, alias=alias)
        serializer.save(adverse=adverse)


class PropertyRepossessedListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = PropertyRepossessedSerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return PropertyRepossessed.objects.filter(
            adverse__case=case, adverse__alias=alias
        )

    def perform_create(self, serializer):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        adverse = get_object_or_404(Adverse, case=case, alias=alias)
        serializer.save(adverse=adverse)


class BankruptListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = BankruptSerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return Bankrupt.objects.filter(adverse__case=case, adverse__alias=alias)

    def perform_create(self, serializer):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        adverse = get_object_or_404(Adverse, case=case, alias=alias)
        serializer.save(adverse=adverse)


class IndividualVoluntaryListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = IndividualVoluntarySerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return IndividualVoluntary.objects.filter(
            adverse__case=case, adverse__alias=alias
        )

    def perform_create(self, serializer):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        adverse = get_object_or_404(Adverse, case=case, alias=alias)
        serializer.save(adverse=adverse)


class DebtManagementPlanListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = DebtManagementPlanSerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return DebtManagementPlan.objects.filter(
            adverse__case=case, adverse__alias=alias
        )

    def perform_create(self, serializer):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        adverse = get_object_or_404(Adverse, case=case, alias=alias)
        serializer.save(adverse=adverse)


class PayDayLoanListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = PayDayLoanSerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return PayDayLoan.objects.filter(adverse__case=case, adverse__alias=alias)

    def perform_create(self, serializer):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        adverse = get_object_or_404(Adverse, case=case, alias=alias)
        serializer.save(adverse=adverse)


class PropertyListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated, CasePermissionForClintUpdate]

    def get_queryset(self):
        return Property.objects.filter(case=self.get_case())

    def perform_create(self, serializer):
        case = self.get_case()
        serializer.save(case=case, created_by=self.request.user)


class SolicitorListCreateApiView(ListCreateAPIView):
    serializer_class = SolicitorAccountantSerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        return SolicitorAccountant.objects.filter(user_type="SOLICITOR")

    def perform_create(self, serializer):
        serializer.save(user_type="SOLICITOR", created_by=self.request.user)


class AccountantListCreateApiView(ListCreateAPIView):
    serializer_class = SolicitorAccountantSerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        return SolicitorAccountant.objects.filter(user_type="ACCOUNTANT")

    def perform_create(self, serializer):
        serializer.save(user_type="ACCOUNTANT", created_by=self.request.user)


class CaseAccountantsApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = CaseAccountantSerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        return CaseAccountant.objects.filter(case=self.get_case())

    def perform_create(self, serializer):
        case = self.get_case()
        serializer.save(case=case, created_by=self.request.user)


class CaseSolicitorApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = CaseSolicitorSerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        return CaseSolicitor.objects.filter(case=self.get_case())

    def perform_create(self, serializer):
        case = self.get_case()
        serializer.save(case=case, created_by=self.request.user)


class SolicitorRetrieveUpdateApiView(RetrieveUpdateAPIView):
    serializer_class = SolicitorAccountantSerializer
    permission_classes = [IsAuthenticated, CasePermission]
    lookup_field = "alias"

    def get_queryset(self):
        return SolicitorAccountant.objects.filter(user_type="SOLICITOR")

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class AccountantRetrieveUpdateApiView(RetrieveUpdateAPIView):
    serializer_class = SolicitorAccountantSerializer
    permission_classes = [IsAuthenticated, CasePermission]
    lookup_field = "alias"

    def get_queryset(self):
        return SolicitorAccountant.objects.filter(user_type="ACCOUNTANT")

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class ExistingProtectionListApiView(CaseRelatedViewMixin, ListAPIView):
    serializer_class = ExistingProtectionSerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        return ExistingProtection.objects.filter(case=self.get_case())


class ExistingProtectionCreateApiView(CaseRelatedViewMixin, CreateAPIView):
    serializer_class = ExistingProtectionSerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def perform_create(self, serializer):
        case = self.get_case()
        user_obj = get_object_or_404(User, pk=self.kwargs["pk"])
        serializer.save(case=case, user=user_obj, created_by=self.request.user)


class ExistingProtectionRetrieveUpdateApiView(
    CaseRelatedViewMixin, RetrieveUpdateAPIView
):
    serializer_class = ExistingProtectionSerializer
    permission_classes = [IsAuthenticated, CasePermission]
    lookup_field = "alias"

    def get_object(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return get_object_or_404(ExistingProtection, case=case, alias=alias)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class NoteListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = NotesSerializer
    permission_classes = [IsAuthenticated, CasePermissionForClintUpdate]

    def get_queryset(self):
        return Notes.objects.filter(case=self.get_case())

    def perform_create(self, serializer):
        case = self.get_case()
        serializer.save(case=case, created_by=self.request.user)


class NoteRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateAPIView):
    serializer_class = NotesSerializer
    permission_classes = [IsAuthenticated, CasePermissionForClintUpdate]
    lookup_field = "alias"

    def get_object(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return get_object_or_404(Notes, case=case, alias=alias)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class PropertyDetailsListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = PropertyDetailsSerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        return PropertyDetails.objects.filter(case=self.get_case())

    def perform_create(self, serializer):
        case = self.get_case()
        serializer.save(case=case, created_by=self.request.user)


class PropertyDetailsRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateAPIView):
    serializer_class = PropertyDetailsSerializer
    permission_classes = [IsAuthenticated, CasePermission]
    lookup_field = "alias"

    def get_object(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return get_object_or_404(PropertyDetails, case=case, alias=alias)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class OtherOccupantsListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = OtherOccupantsSerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        return OtherOccupants.objects.filter(case=self.get_case())

    def perform_create(self, serializer):
        case = self.get_case()
        serializer.save(case=case, created_by=self.request.user)


class OtherOccupantsRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateAPIView):
    serializer_class = OtherOccupantsSerializer
    permission_classes = [IsAuthenticated, CasePermission]
    lookup_field = "alias"

    def get_object(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return get_object_or_404(OtherOccupants, case=case, alias=alias)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class ProductListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, CasePermissionForClintUpdate]

    def get_queryset(self):
        return Product.objects.filter(case=self.get_case())

    def perform_create(self, serializer):
        case = self.get_case()
        serializer.save(case=case, created_by=self.request.user)


class ProductRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, CasePermissionForClintUpdate]
    lookup_field = "alias"

    def get_object(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return get_object_or_404(Product, case=case, alias=alias)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class BudgetPlannerListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = BudgetPlannerSerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        return BudgetPlanner.objects.filter(case=self.get_case())

    def perform_create(self, serializer):
        case = self.get_case()
        serializer.save(case=case, created_by=self.request.user)


class BudgetPlannerRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateAPIView):
    serializer_class = BudgetPlannerSerializer
    permission_classes = [IsAuthenticated, CasePermission]
    lookup_field = "alias"

    def get_object(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return get_object_or_404(BudgetPlanner, case=case, alias=alias)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class FeesInListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = FeesSerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        case = self.get_case()
        return Fees.objects.filter(case=case, fees_type=FeesChoices.FEES_IN)

    def perform_create(self, serializer):
        case = self.get_case()
        serializer.save(
            case=case, fees_type=FeesChoices.FEES_IN, created_by=self.request.user
        )


class FeesOutListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = FeesSerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        case = self.get_case()
        return Fees.objects.filter(case=case, fees_type=FeesChoices.FEES_OUT)

    def perform_create(self, serializer):
        case = self.get_case()
        serializer.save(
            case=case, fees_type=FeesChoices.FEES_OUT, created_by=self.request.user
        )


class FeesRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateAPIView):
    serializer_class = FeesSerializer
    permission_classes = [IsAuthenticated, CasePermission]
    lookup_field = "alias"

    def get_object(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return get_object_or_404(Fees, case=case, alias=alias)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class DipHistoryListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = DipHistorySerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        case = self.get_case()
        return DipHistory.objects.filter(case=case)

    def perform_create(self, serializer):
        case = self.get_case()
        serializer.save(case=case, created_by=self.request.user)


class DipHistoryRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateAPIView):
    serializer_class = DipHistorySerializer
    permission_classes = [IsAuthenticated, CasePermission]
    lookup_field = "alias"

    def get_object(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return get_object_or_404(DipHistory, case=case, alias=alias)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class CreditCommitmentsListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = CreditCommitmentsSerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        case = self.get_case()
        return CreditCommitments.objects.filter(case=case)

    def perform_create(self, serializer):
        case = self.get_case()
        applicant = serializer.validated_data["applicant"]

        # Check if the applicant is the case lead
        if applicant == case.lead:
            return self._save_credit_commitment(serializer, case)

        # Check if the applicant is a joint user for this case
        if JointUser.objects.filter(case=case, joint_user=applicant).exists():
            return self._save_credit_commitment(serializer, case)

        # If applicant is neither lead nor joint user, raise validation error
        raise ValidationError("Applicant is not a valid user for this case.")

    def _save_credit_commitment(self, serializer, case):
        serializer.save(
            case=case,
            applicant=serializer.validated_data["applicant"],
            created_by=self.request.user,
            updated_by=self.request.user,
        )


class CreditCommitmentsRetrieveUpdateDestroyApiView(
    CaseRelatedViewMixin, RetrieveUpdateDestroyAPIView
):
    serializer_class = CreditCommitmentsSerializer
    permission_classes = [IsAuthenticated, CasePermission]
    lookup_field = "alias"

    def get_object(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return get_object_or_404(CreditCommitments, case=case, alias=alias)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()


class SuitabilityRetrieveUpdateApiView(
    CaseRelatedViewMixin, RetrieveUpdateDestroyAPIView
):
    serializer_class = SuitabilitySerializer
    permission_classes = [IsAuthenticated, CasePermission]

    def get_object(self):
        case = self.get_case()
        return get_object_or_404(Suitability, case=case)

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.updated_by = request.user
        instance.save()
        return super().update(request, *args, **kwargs)


class ExtraAnswerListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = ExtraAnswerSerializers
    permission_classes = [IsAuthenticated, CasePermission]

    def get_queryset(self):
        case = self.get_case()
        return ExtraAnswer.objects.filter(case=case)

    def perform_create(self, serializer):
        case = self.get_case()
        serializer.save(case=case, created_by=self.request.user)


class ComplianceRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateAPIView):
    serializer_class = ComplianceSerializers
    permission_classes = [IsAuthenticated, CasePermission]

    def get_object(self):
        case = self.get_case()
        return get_object_or_404(Compliance, case=case)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class MortgageNeedsRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateAPIView):
    serializer_class = MortgageNeedsSerializers
    permission_classes = [IsAuthenticated, CasePermission]

    def get_object(self):
        case = self.get_case()
        return get_object_or_404(MortgageNeeds, case=case)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class CasePDFReportAPIView(CaseAuthenticationMixin, APIView):
    """Generate PDF report for a specific case"""

    permission_classes = [IsAuthenticated]

    def get(self, request, case_alias):
        # Get the case
        case = get_object_or_404(Case, alias=case_alias)

        # Check user permissions for this case
        user_association = self.get_user_association()
        case_queryset = self.get_case_queryset()

        if not case_queryset.filter(alias=case_alias).exists():
            return Response(
                {"error": "You don't have permission to access this case"}, status=403
            )

        # Get firm name based on user association
        if user_association["type"] == "organization":
            firm_name = user_association["organization"].name
        else:  # network user
            firm_name = user_association["network"].name

        # Get case details
        loan_details = case.loan_details

        # Get adviser name (case creator)
        adviser_name = (
            f"{case.created_by.first_name} {case.created_by.last_name}"
            if case.created_by
            else "N/A"
        )

        # Get client name (lead user)
        client_name = (
            f"{case.lead.first_name} {case.lead.last_name}" if case.lead else "N/A"
        )

        # Create PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )

        # Container for the 'Flowable' objects
        elements = []

        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
        )

        heading_style = ParagraphStyle(
            "CustomHeading",
            parent=styles["Heading2"],
            fontSize=14,
            spaceAfter=12,
            alignment=TA_LEFT,
        )

        normal_style = styles["Normal"]

        # Add title
        title = Paragraph("Case Report", title_style)
        elements.append(title)
        elements.append(Spacer(1, 12))

        # Create data table
        data = [
            ["Field", "Value"],
            ["Firm:", firm_name],
            ["Adviser:", adviser_name],
            ["Client Name:", client_name],
            [
                "Submitted Date:",
                case.created_at.strftime("%d/%m/%Y") if case.created_at else "N/A",
            ],
            [
                "Reference:",
                str(case.alias)[:6].upper(),
            ],  # First 6 chars of UUID as reference
            [
                "Current Stage:",
                case.get_case_stage_display() if case.case_stage else "N/A",
            ],
        ]

        # Add loan details if available
        if loan_details:
            data.extend(
                [
                    [
                        "Loan Type:",
                        (
                            loan_details.get_mortgage_type_display()
                            if loan_details.mortgage_type
                            else "N/A"
                        ),
                    ],
                    [
                        "Purpose:",
                        (
                            loan_details.get_loan_purpose_display()
                            if loan_details.loan_purpose
                            else "N/A"
                        ),
                    ],
                    [
                        "Lead Source:",
                        (
                            loan_details.get_lead_source_display()
                            if loan_details.lead_source
                            else "N/A"
                        ),
                    ],
                    ["Lender:", loan_details.lender or "N/A"],
                    [
                        "Loan Amount:",
                        (
                            f"£{loan_details.loan_amount:,.2f}"
                            if loan_details.loan_amount
                            else "N/A"
                        ),
                    ],
                    [
                        "LTV (%):",
                        f"{loan_details.ltv:.2f}" if loan_details.ltv else "N/A",
                    ],
                ]
            )

        # Get net income (you might need to calculate this from income/expenses models)
        # For now, using placeholder
        data.append(
            ["Net Income:", "£252.68"]
        )  # This should be calculated from actual data

        # Create table
        table = Table(data, colWidths=[2.5 * inch, 4 * inch])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 14),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    (
                        "FONTNAME",
                        (0, 1),
                        (0, -1),
                        "Helvetica-Bold",
                    ),  # Make first column bold
                ]
            )
        )

        elements.append(table)
        elements.append(Spacer(1, 12))

        # Add footer with generation date
        footer_text = (
            f"Report generated on {datetime.now().strftime('%d/%m/%Y at %H:%M')}"
        )
        footer = Paragraph(footer_text, normal_style)
        elements.append(Spacer(1, 20))
        elements.append(footer)

        # Build PDF
        doc.build(elements)

        # Get the value of the BytesIO buffer and write it to the response
        pdf = buffer.getvalue()
        buffer.close()

        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="case_report_{case.alias}.pdf"'
        )
        response.write(pdf)

        return response

# Client survey Lise create api views.
class ClientSurveyListCreateAPIViews(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = ClientSurveySerializers
    permission_classes = [IsAuthenticated, CasePermissionForClintUpdate]

    def get_queryset(self):
        case = self.get_case()
        return ClientSurvey.objects.filter(case=case)

    def perform_create(self, serializer):
        case = self.get_case()
        serializer.save(case=case, created_by=self.request.user)


class ClientSurveyRetrieveUpdateApiView(CaseRelatedViewMixin ,RetrieveUpdateAPIView):
    serializer_class = ClientSurveySerializers
    permission_classes = [IsAuthenticated, CasePermissionForClintUpdate]
    lookup_field = "alias"

    def get_object(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return get_object_or_404(ClientSurvey, case=case, alias=alias)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

