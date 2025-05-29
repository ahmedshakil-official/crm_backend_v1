from django.db import transaction
from django.db.models.functions import Lead
from django_filters.rest_framework.backends import DjangoFilterBackend
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
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.models import User
from common.serializers import CommonUserSerializer, CommonUserWithIdSerializer
from organization.models import Organization
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
    MortgageNeeds, MortgageFeatures,
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
    MortgageNeedsSerializers,
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
        if not hasattr(self, '_cached_case'):
            case_alias = self.kwargs.get('case_alias')
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
        if 'case_alias' in self.kwargs:
            context['case'] = self.get_case()
        return context


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
        user = self.request.user
        organization = get_object_or_404(
            Organization, organization_users__user=self.request.user
        )
        queryset = Case.objects.select_related("organization", "lead", "created_by").filter(
            organization=organization,
            is_removed=False
        )
        if hasattr(user, "user_type") and user.user_type.upper() == "LEAD":
            return queryset.filter(lead=user)
        return queryset

    def perform_create(self, serializer):
        organization = get_object_or_404(
            Organization, organization_users__user=self.request.user
        )
        serializer.save(
            organization=organization,
            created_by=self.request.user,
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context


class CaseRetrieveUpdateDeleteApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = CaseRetrieveUpdateDeleteSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_queryset(self):
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


class FileListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = FileFilter

    def get_filterset_kwargs(self):
        kwargs = super().get_filterset_kwargs()
        kwargs["request"] = self.request
        kwargs["case"] = self.get_case()
        return kwargs

    def get_queryset(self):
        return Files.objects.filter(case=self.get_case())


class FileRetrieveUpdateDeleteApiView(CaseRelatedViewMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]
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
        serializer.save(case=self.get_case())


class JointUserRetrieveUpdateDeleteApiView(CaseRelatedViewMixin, RetrieveUpdateDestroyAPIView):
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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return LoanDetails.objects.filter(case=self.get_case())

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, case=self.get_case())


class LoanDetailsRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateAPIView):
    serializer_class = LoanDetailsSerializer
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ApplicantDetails.objects.filter(case=self.get_case())


class ApplicantDetailsRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateAPIView):
    queryset = ApplicantDetails.objects.all()
    serializer_class = ApplicantDetailsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_object(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return get_object_or_404(ApplicantDetails, case=case, alias=alias)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class DependantListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = DependantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return Dependant.objects.filter(
            applicant_details__case=case, applicant_details__alias=alias
        )

    def perform_create(self, serializer):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        applicant_details = get_object_or_404(
            ApplicantDetails, case=case, alias=alias
        )
        serializer.save(applicant_details=applicant_details)


class CompanyInfoListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = CompanyInfoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        case = self.get_case()
        alias = self.kwargs["alias"]
        return CompanyInfo.objects.filter(
            applicant_details__case=case, applicant_details__alias=alias
        )

    def perform_create(self, serializer):
        case = self.get_case()
        alias = self.kwargs["alias"]
        applicant_details = get_object_or_404(
            ApplicantDetails, case=case, alias=alias
        )
        serializer.save(applicant_details=applicant_details)


class DirectorShareholderListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = DirectorShareholderSerializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return EmploymentDetails.objects.filter(case=self.get_case())


class EmploymentDetailsCreateApiView(CaseRelatedViewMixin, CreateAPIView):
    serializer_class = EmploymentDetailsSerializer
    permission_classes = [IsAuthenticated]

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


class EmploymentDetailsRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateAPIView):
    serializer_class = EmploymentDetailsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_queryset(self):
        return EmploymentDetails.objects.filter(case=self.get_case())

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class AdverseListApiView(CaseRelatedViewMixin, ListAPIView):
    serializer_class = AdverseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Adverse.objects.filter(case=self.get_case())


class AdverseRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateAPIView):
    serializer_class = AdverseSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_queryset(self):
        return Adverse.objects.filter(case=self.get_case())

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class RegisterLoanListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = RegisterLoanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return RegisterLoan.objects.filter(
            adverse__case=case, adverse__alias=alias
        )

    def perform_create(self, serializer):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        adverse = get_object_or_404(Adverse, case=case, alias=alias)
        serializer.save(adverse=adverse)


class CCJListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = CCJSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return CCJ.objects.filter(
            adverse__case=case, adverse__alias=alias
        )

    def perform_create(self, serializer):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        adverse = get_object_or_404(Adverse, case=case, alias=alias)
        serializer.save(adverse=adverse)


class PaymentCommitmentListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = PaymentCommitmentSerializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return Bankrupt.objects.filter(
            adverse__case=case, adverse__alias=alias
        )

    def perform_create(self, serializer):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        adverse = get_object_or_404(Adverse, case=case, alias=alias)
        serializer.save(adverse=adverse)


class IndividualVoluntaryListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = IndividualVoluntarySerializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return PayDayLoan.objects.filter(
            adverse__case=case, adverse__alias=alias
        )

    def perform_create(self, serializer):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        adverse = get_object_or_404(Adverse, case=case, alias=alias)
        serializer.save(adverse=adverse)


class PropertyListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = PropertySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Property.objects.filter(case=self.get_case())

    def perform_create(self, serializer):
        case = self.get_case()
        serializer.save(case=case, created_by=self.request.user)


class SolicitorListCreateApiView(ListCreateAPIView):
    serializer_class = SolicitorAccountantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SolicitorAccountant.objects.filter(user_type='SOLICITOR')

    def perform_create(self, serializer):
        serializer.save(user_type='SOLICITOR', created_by=self.request.user)


class AccountantListCreateApiView(ListCreateAPIView):
    serializer_class = SolicitorAccountantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SolicitorAccountant.objects.filter(user_type='ACCOUNTANT')

    def perform_create(self, serializer):
        serializer.save(user_type='ACCOUNTANT', created_by=self.request.user)


class CaseAccountantsApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = CaseAccountantSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CaseAccountant.objects.filter(case=self.get_case())

    def perform_create(self, serializer):
        case = self.get_case()
        serializer.save(case=case, created_by=self.request.user)


class CaseSolicitorApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = CaseSolicitorSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CaseSolicitor.objects.filter(case=self.get_case())

    def perform_create(self, serializer):
        case = self.get_case()
        serializer.save(case=case, created_by=self.request.user)


class SolicitorRetrieveUpdateApiView(RetrieveUpdateAPIView):
    serializer_class = SolicitorAccountantSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_queryset(self):
        return SolicitorAccountant.objects.filter(user_type='SOLICITOR')

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class AccountantRetrieveUpdateApiView(RetrieveUpdateAPIView):
    serializer_class = SolicitorAccountantSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_queryset(self):
        return SolicitorAccountant.objects.filter(user_type='ACCOUNTANT')

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class ExistingProtectionListApiView(CaseRelatedViewMixin, ListAPIView):
    serializer_class = ExistingProtectionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ExistingProtection.objects.filter(case=self.get_case())


class ExistingProtectionCreateApiView(CaseRelatedViewMixin, CreateAPIView):
    serializer_class = ExistingProtectionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        case = self.get_case()
        user_obj = get_object_or_404(User, pk=self.kwargs["pk"])
        serializer.save(case=case, user=user_obj, created_by=self.request.user)


class ExistingProtectionRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateAPIView):
    serializer_class = ExistingProtectionSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_object(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return get_object_or_404(ExistingProtection, case=case, alias=alias)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class NoteListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = NotesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notes.objects.filter(case=self.get_case())

    def perform_create(self, serializer):
        case = self.get_case()
        serializer.save(case=case, created_by=self.request.user)


class NoteRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateAPIView):
    serializer_class = NotesSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_object(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return get_object_or_404(Notes, case=case, alias=alias)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class PropertyDetailsListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = PropertyDetailsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PropertyDetails.objects.filter(case=self.get_case())

    def perform_create(self, serializer):
        case = self.get_case()
        serializer.save(case=case, created_by=self.request.user)


class PropertyDetailsRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateAPIView):
    serializer_class = PropertyDetailsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_object(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return get_object_or_404(PropertyDetails, case=case, alias=alias)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class OtherOccupantsListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = OtherOccupantsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return OtherOccupants.objects.filter(case=self.get_case())

    def perform_create(self, serializer):
        case = self.get_case()
        serializer.save(case=case, created_by=self.request.user)


class OtherOccupantsRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateAPIView):
    serializer_class = OtherOccupantsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_object(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return get_object_or_404(OtherOccupants, case=case, alias=alias)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class ProductListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(case=self.get_case())

    def perform_create(self, serializer):
        case = self.get_case()
        serializer.save(case=case, created_by=self.request.user)


class ProductRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_object(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return get_object_or_404(Product, case=case, alias=alias)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class BudgetPlannerListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = BudgetPlannerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BudgetPlanner.objects.filter(case=self.get_case())

    def perform_create(self, serializer):
        case = self.get_case()
        serializer.save(case=case, created_by=self.request.user)


class BudgetPlannerRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateAPIView):
    serializer_class = BudgetPlannerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_object(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return get_object_or_404(BudgetPlanner, case=case, alias=alias)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class FeesInListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = FeesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        case = self.get_case()
        return Fees.objects.filter(case=case, fee_type=FeesChoices.FEES_IN)

    def perform_create(self, serializer):
        case = self.get_case()
        serializer.save(case=case, fee_type=FeesChoices.FEES_IN, created_by=self.request.user)


class FeesOutListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = FeesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        case = self.get_case()
        return Fees.objects.filter(case=case, fee_type=FeesChoices.FEES_OUT)

    def perform_create(self, serializer):
        case = self.get_case()
        serializer.save(case=case, fee_type=FeesChoices.FEES_OUT, created_by=self.request.user)


class FeesRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateAPIView):
    serializer_class = FeesSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_object(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return get_object_or_404(Fees, case=case, alias=alias)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)



class DipHistoryListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = DipHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        case = self.get_case()
        return DipHistory.objects.filter(case=case)

    def perform_create(self, serializer):
        case = self.get_case()
        serializer.save(case=case, created_by=self.request.user)



class DipHistoryRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateAPIView):
    serializer_class = DipHistorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_object(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return get_object_or_404(DipHistory, case=case, alias=alias)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class CreditCommitmentsListCreateApiView(CaseRelatedViewMixin, ListCreateAPIView):
    serializer_class = CreditCommitmentsSerializer
    permission_classes = [IsAuthenticated]

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


class CreditCommitmentsRetrieveUpdateDestroyApiView(CaseRelatedViewMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = CreditCommitmentsSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_object(self):
        case = self.get_case()
        alias = self.kwargs.get("alias")
        return get_object_or_404(CreditCommitments, case=case, alias=alias)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.delete()


class SuitabilityRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateDestroyAPIView):
    serializer_class = SuitabilitySerializer
    permission_classes = [IsAuthenticated]

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
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        case = self.get_case()
        return ExtraAnswer.objects.filter(case=case)

    def perform_create(self, serializer):
        case = self.get_case()
        serializer.save(case=case, created_by=self.request.user)


class ComplianceRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateAPIView):
    serializer_class = ComplianceSerializers
    permission_classes = [IsAuthenticated]

    def get_object(self):
        case = self.get_case()
        return get_object_or_404(Compliance, case=case)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


class MortgageNeedsRetrieveUpdateApiView(CaseRelatedViewMixin, RetrieveUpdateAPIView):
    serializer_class = MortgageNeedsSerializers
    permission_classes = [IsAuthenticated]

    def get_object(self):
        case = self.get_case()
        return get_object_or_404(MortgageNeeds, case=case)

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)


