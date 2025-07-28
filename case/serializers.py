from django.db import transaction
from django.db.models import Q
from django_countries.serializer_fields import CountryField
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from common.enums import UserTypeChoices, OrganizationRoleChoices, NetworkRoleChoices
from case.enums import (
    UserTypeChoices as SolicitorTypeChoices,
    IncomeTypeChoices,
    DebtRepaymentTypeChoices,
    PriorityDebtTypeChoices,
    UnsecuredBorrowingTypeChoices,
    LivingCostsTypeChoices,
    InsuranceTypeChoices,
    SubTotalsTypeChoices,
)
from organization.models import Organization, OrganizationUser, NetworkUser
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
from .models import (
    Case,
    Files,
    JointUser,
    LoanDetails,
    ApplicantDetails,
    CompanyInfo,
    Dependant,
    DirectorShareholder,
    EmploymentDetails,
    Adverse,
    Property,
    SolicitorAccountant,
    CaseSolicitor,
    CaseAccountant,
    ExistingProtection,
    Notes,
    PropertyDetails,
    OtherOccupants,
    Product,
    DebtRepayments,
    PriorityDebt,
    UnsecuredBorrowing,
    LivingCosts,
    Insurances,
    SubTotals,
    BudgetPlanner,
    Income,
    Fees,
    DipHistory,
    CreditCommitments,
    Suitability,
    ExtraQuestion,
    CircumstancesObjectives,
    BudgetAffordability,
    NewMortgageDetails,
    RecommendingRepaymentMethod,
    RecommendingMortgageType,
    RecommendingTerm,
    RecommendingMortgageLender,
    RecommendingMortgageAmount,
    CostsFees,
    Protection,
    CostAdvice,
    DisadvantageRisks,
    BuildingsInsurance,
    Wills,
    ExtraAnswer,
    Compliance,
    MortgageNeeds,
)
from authentication.models import User
from common.serializers import (
    CommonUserSerializer,
    CommonOrganizationSerializer,
    CommonUserWithPasswordSerializer,
    CommonCaseSerializer,
    CommonUserWithIdSerializer,
    CommonNetworkSerializer,
)


class CaseListCreateSerializer(serializers.ModelSerializer):
    organization = CommonOrganizationSerializer(read_only=True)
    network = CommonNetworkSerializer(read_only=True)
    lead_user = CommonUserWithIdSerializer(read_only=True, source="lead")
    lead = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.none(),
        write_only=True,
        required=True,
    )
    created_by = CommonUserSerializer(read_only=True)
    updated_by = CommonUserSerializer(read_only=True)

    class Meta:
        model = Case
        fields = [
            "alias",
            "name",
            "lead",
            "lead_user",
            "organization",
            "network",
            "case_category",
            "case_stage",
            "notes",
            "is_removed",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "alias",
            "name",
            "lead_user",
            "case_stage",
            "organization",
            "network",
            "created_by",
            "is_removed",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        write_only_fields = ["lead"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            self._set_lead_queryset(request.user)

    def _set_lead_queryset(self, user):
        """Set the lead queryset based on whether user is from organization or network"""
        # Check if user is associated with an organization
        organization_user = OrganizationUser.objects.filter(user=user).first()
        if organization_user:
            # For organization users: only leads from the same organization
            self.fields["lead"].queryset = User.objects.filter(
                user_type="LEAD",
                organization_users__organization=organization_user.organization,
            )
            return

        # Check if user is associated with a network
        network_user = NetworkUser.objects.filter(user=user).first()
        if network_user:
            # For network users: leads from all organizations in the network + direct network leads
            self.fields["lead"].queryset = User.objects.filter(
                Q(
                    user_type="LEAD",
                    organization_users__organization__network=network_user.network,
                )
                | Q(user_type="LEAD", network_users__network=network_user.network)
            ).distinct()
            return

        # If neither, empty queryset
        self.fields["lead"].queryset = User.objects.none()

    def create(self, validated_data):
        """Create case with proper organization/network assignment"""
        request = self.context.get("request")
        user = request.user

        # Check if user is from organization
        organization_user = OrganizationUser.objects.filter(user=user).first()
        if organization_user:
            validated_data["organization"] = organization_user.organization
            validated_data["network"] = organization_user.organization.network
        else:
            # Check if user is from network
            network_user = NetworkUser.objects.filter(user=user).first()
            if network_user:
                validated_data["network"] = network_user.network
                # Organization will be None for network-level cases
                validated_data["organization"] = None
            else:
                raise serializers.ValidationError(
                    "User must be associated with an organization or network to create cases."
                )

        validated_data["created_by"] = user
        validated_data["updated_by"] = user

        case = super().create(validated_data)

        # If case was created with a lead, update the lead user's user_type and role to CLIENT
        if case.lead:
            case.lead.user_type = UserTypeChoices.CLIENT
            case.lead.save()

            # Update the role in OrganizationUser or NetworkUser
            lead_org_user = OrganizationUser.objects.filter(user=case.lead).first()
            if lead_org_user:
                lead_org_user.role = OrganizationRoleChoices.CLIENT
                lead_org_user.save()
            else:
                lead_network_user = NetworkUser.objects.filter(user=case.lead).first()
                if lead_network_user:
                    lead_network_user.role = NetworkRoleChoices.CLIENT
                    lead_network_user.save()

        return case


class CaseRetrieveUpdateDeleteSerializer(serializers.ModelSerializer):
    organization = CommonOrganizationSerializer(read_only=True)
    network = CommonNetworkSerializer(read_only=True)
    lead_user = CommonUserWithIdSerializer(read_only=True, source="lead")
    lead = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.none(),
        write_only=True,
        required=False,
    )
    created_by = CommonUserSerializer(read_only=True)
    updated_by = CommonUserSerializer(read_only=True)

    class Meta:
        model = Case
        fields = [
            "alias",
            "name",
            "lead",
            "lead_user",
            "organization",
            "network",
            "case_category",
            "case_stage",
            "notes",
            "is_removed",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "alias",
            "name",
            "lead_user",
            "organization",
            "network",
            "created_by",
            "is_removed",
            "updated_by",
            "created_at",
            "updated_at",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            self._set_lead_queryset(request.user)

    def _set_lead_queryset(self, user):
        """Set the lead queryset based on whether user is from organization or network"""
        # Check if user is associated with an organization
        organization_user = OrganizationUser.objects.filter(user=user).first()
        if organization_user:
            # For organization users: only leads from the same organization
            self.fields["lead"].queryset = User.objects.filter(
                user_type="LEAD",
                organization_users__organization=organization_user.organization,
            )
            return

        # Check if user is associated with a network
        network_user = NetworkUser.objects.filter(user=user).first()
        if network_user:
            # For network users: leads from all organizations in the network + direct network leads
            self.fields["lead"].queryset = User.objects.filter(
                Q(
                    user_type="LEAD",
                    organization_users__organization__network=network_user.network,
                )
                | Q(user_type="LEAD", network_users__network=network_user.network)
            ).distinct()
            return

        # If neither, empty queryset
        self.fields["lead"].queryset = User.objects.none()

    def update(self, instance, validated_data):
        """Update case with proper user tracking"""
        request = self.context.get("request")
        validated_data["updated_by"] = request.user
        return super().update(instance, validated_data)


class FileSerializer(serializers.ModelSerializer):
    file_owner_info = CommonUserSerializer(read_only=True, source="file_owner")
    created_by = CommonUserSerializer(read_only=True)
    updated_by = CommonUserSerializer(read_only=True)
    file_owner = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.none(), write_only=True
    )

    class Meta:
        model = Files
        fields = [
            "alias",
            "file",
            "file_type",
            "file_owner",
            "file_owner_info",
            "name",
            "description",
            "special_notes",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "alias",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        write_only_fields = ["file_owner"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Get the case from the context and limit the queryset for file_owner
        case = self.context.get("case")
        if case:
            lead = case.lead
            joint_users = case.joint_users.values_list("joint_user", flat=True)
            self.fields["file_owner"].queryset = User.objects.filter(
                pk__in=[lead.pk, *joint_users]
            )

    def validate_file_owner(self, value):
        # Ensure file_owner is either the lead or one of the joint users of the case
        case = self.context.get("case")
        if not case:
            raise serializers.ValidationError("Case context is not provided.")

        # Fetch the lead and joint users as user objects
        valid_owners = [case.lead] + list(
            User.objects.filter(
                pk__in=case.joint_users.values_list("joint_user", flat=True)
            )
        )

        if value not in valid_owners:
            raise serializers.ValidationError(
                "File owner must be the lead or a joint user of this case."
            )
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        if not user or not user.is_authenticated:
            raise serializers.ValidationError(
                "User must be authenticated to create files."
            )

        validated_data["case"] = self.context["case"]
        validated_data["created_by"] = user
        validated_data["user_ip"] = self.context["request"].META.get(
            "REMOTE_ADDR", None
        )
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data["updated_by"] = self.context["request"].user
        validated_data["user_ip"] = self.context["request"].META.get(
            "REMOTE_ADDR", None
        )
        return super().update(instance, validated_data)


class JointUserSerializer(serializers.ModelSerializer):
    joint_user = CommonUserWithPasswordSerializer(write_only=True)
    joint_user_details = CommonUserWithIdSerializer(read_only=True, source="joint_user")
    created_by = CommonUserSerializer(read_only=True)
    updated_by = CommonUserSerializer(read_only=True)
    case = CommonCaseSerializer(read_only=True)

    class Meta:
        model = JointUser
        fields = [
            "alias",
            "case",
            "joint_user",
            "joint_user_details",
            "relationship",
            "notes",
            "is_removed",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "case",
            "is_removed",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]

    def create(self, validated_data):
        joint_user_data = validated_data.pop("joint_user")
        joint_user_data["user_type"] = UserTypeChoices.JOINT_USER
        joint_user = CommonUserWithPasswordSerializer().create(joint_user_data)

        case = validated_data["case"]
        organization = case.organization

        OrganizationUser.objects.create(
            user=joint_user,
            organization=organization,
            role=UserTypeChoices.JOINT_USER,
            official_email=joint_user_data.get("email"),
            official_phone=joint_user_data.get("phone"),
        )

        validated_data["joint_user"] = joint_user
        validated_data["created_by"] = self.context["request"].user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        joint_user_data = validated_data.pop("joint_user", None)
        if joint_user_data:
            joint_user_data["user_type"] = UserTypeChoices.JOINT_USER
            joint_user_serializer = CommonUserWithPasswordSerializer(
                instance.joint_user, data=joint_user_data, partial=True
            )
            joint_user_serializer.is_valid(raise_exception=True)
            joint_user_serializer.save()

            # Update OrganizationUser information
            organization_user = OrganizationUser.objects.filter(
                user=instance.joint_user, organization=instance.case.organization
            ).first()
            if organization_user:
                organization_user.official_email = instance.joint_user.email
                organization_user.official_phone = joint_user_data.get(
                    "phone", organization_user.official_phone
                )
                organization_user.save()

        validated_data["updated_by"] = self.context["request"].user
        return super().update(instance, validated_data)


class CaseUserListSerializer(serializers.ModelSerializer):
    joint_user = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = JointUser
        fields = ["joint_user", "relationship", "notes", "is_removed"]


class LoanDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanDetails
        fields = [
            "alias",
            "case",
            "application_type",
            "mortgage_type",
            "loan_purpose",
            "lender",
            "lenders_reference",
            "borrower_type",
            "repayment_method",
            "repayment_vehicle",
            "interest_rate_type",
            "product_term",
            "property_valuation",
            "purchase_price",
            "loan_amount",
            "estimated_value",
            "ltv",
            "term_years",
            "term_months",
            "outstanding_balance",
            "current_monthly_payment",
            "current_lender",
            "interest_only_amount",
            "original_purchase_price",
            "date_of_purchase",
            "deposit_amount",
            "deposit_source",
            "advice_level",
            "dip_accept_date",
            "dip_expiry_date",
            "expected_completion_date",
            "product_expiry_date",
            "introduction_type",
            "introducer_payment_terms",
            "introducer_fee",
            "lead_source",
            "sale_type",
            "reasons_for_capital_raising",
            "case_summary",
            "accepted_or_declined_by_lender",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "case",
        ]


class CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CompanyInfo
        fields = [
            "applicant_details",
            "company_name",
            "company_registration_number",
            "date_of_incorporation",
            "company_type",
            "trade_business_type",
            "sic_code",
            "is_spv",
            "postcode",
            "house_number_or_name",
            "address_line1",
            "city",
            "county",
            "country",
        ]
        read_only_fields = [
            "applicant_details",
        ]


class ApplicantDetailsSerializer(serializers.ModelSerializer):

    nationality = CountryField(required=False, allow_blank=True, allow_null=True)
    applicant = CommonUserWithIdSerializer(read_only=True)
    dual_nationality = CountryField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = ApplicantDetails
        fields = [
            "alias",
            "case",
            "is_company_application",
            "applicant",
            "title",
            "maiden_name",
            "date_of_birth",
            "anticipated_retirement_age",
            "state_retirement_age",
            "is_smoker",
            "gender",
            "nationality",
            "is_dual_nationality",
            "dual_nationality",
            "marital_status",
            "ni_number",
            "country_of_birth",
            "bank_name",
            "home_phone",
            "mobile_phone",
            "work_phone",
            "email",
            "marketing_preferences",
            "has_dependants",
            "number_of_dependants",
            "date_of_arrival_uk",
            "indefinite_right_to_reside",
            "visa_details",
            "visa_expiry_date",
            "postcode",
            "house_number_or_name",
            "address_line1",
            "city",
            "county",
            "country",
            "effective_from",
            "time_at_address_years",
            "time_at_address_months",
            "residential_status",
            "current_mortgage_balance",
            "property_value",
            "owner_monthly_payment",
            "lender",
            "mortgage_start_date",
            "mortgage_type",
            "current_interest_rate",
            "remaining_term",
            "repayment_type",
            "current_interest_type",
            "early_repayment_charge_applies",
            "erc_expiry_date",
            "erc_amount",
            "erc_being_paid",
            "mortgage_account_number",
            "being_redeemed",
            "is_mortgage_portable",
            "is_mortgage_being_ported",
            "mortgage_not_to_complete_until_erc_ended",
            "mortgage_charter_scheme",
            "property_type",
            "bedrooms",
            "tenure",
            "year_built",
            "notes",
            "updated_at",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "applicant",
            "updated_at",
            "created_by",
            "updated_by",
            "case",
            "applicant",
        ]


class DependantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dependant
        fields = [
            "id",
            "applicant_details",
            "name",
            "date_of_birth",
        ]
        read_only_fields = [
            "applicant_details",
        ]


class DirectorShareholderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorShareholder
        fields = [
            "id",
            "company",
            "full_name",
            "percentage_share",
            "role",
        ]


class EmploymentDetailsSerializer(serializers.ModelSerializer):
    user = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = EmploymentDetails

        fields = [
            "alias",
            "user",
            "employment_status",
            "employment_type",
            "occupation",
            "industry",
            "employer_name",
            "employer_telephone",
            "employer_email_for_reference",
            "employer_postcode",
            "employer_house_name_or_number",
            "employer_address_line_1",
            "employer_address_line_2",
            "employer_city",
            "employer_county",
            "employer_country",
            "employment_commenced",
            "employment_ended",
            "gross_annual_income",
            "net_annual_income",
            "is_probationary_period",
            "is_income_in_foreign_currency",
            "bonus",
            "is_bonus_guaranteed",
            "bonus_frequency",
            "overtime",
            "is_overtime_guaranteed",
            "overtime_frequency",
            "allowance",
            "is_allowance_guaranteed",
            "allowance_frequency",
            "employment_time_year",
            "employment_time_month",
            "business_name",
            "business_telephone",
            "business_house_name_or_number",
            "business_postcode",
            "business_address_line_1",
            "business_address_line_2",
            "business_city",
            "business_county",
            "business_country",
            "job_title",
            "company_type",
            "percentage_of_business_owned",
            "is_accounts_available",
            "year1",
            "year1_net_profit",
            "year2",
            "year2_net_profit",
            "year3",
            "year3_net_profit",
            "accountant_name",
            "accountant_qualifications",
            "salary",
            "dividends",
            "turnover",
            "further_details",
            "income_source",
            "other_income",
            "other_income_source",
            "other_income_start_date",
            "contractor_industry",
            "current_contract_start",
            "current_contract_end",
            "time_contracting",
            "day_rate",
            "hourly_rate",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "case",
        ]

        read_only_fields = [
            "alias",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "case",
            "user",
        ]


class AdverseSerializer(serializers.ModelSerializer):
    user = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = Adverse
        fields = [
            "alias",
            "user",
            "has_any_defaults_registered_in_the_last_six_years",
            "has_any_ccj_registered_in_the_last_six_years",
            "missed_any_payments_on_commitments_in_the_last_five_years",
            "is_a_property_repossessed",
            "has_ever_been_made_bankrupt",
            "have_you_ever_entered_into_an_individual_voluntary_arrangement",
            "is_ever_enter_into_a_debt_management_plan_or_debt_relief_order",
            "is_ever_taken_out_a_pay_day_loan",
            "is_exceeded_your_overdraft_in_the_last_three_months",
            "is_direct_debit_returned_in_the_last_three_months",
            "why_did_the_adverse_occur",
        ]

        read_only_fields = [
            "alias",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "user",
        ]


# Serializer for RegisterLoan..
class RegisterLoanSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = RegisterLoan
        fields = [
            "alias",
            "adverse",
            "amount",
            "loan_company_name",
            "date_registered",
            "has_satisfied",
            "date_satisfied",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "adverse",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


class CCJSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = CCJ
        fields = [
            "alias",
            "adverse",
            "amount",
            "loan_company_name",
            "date_registered",
            "has_satisfied",
            "date_satisfied",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "adverse",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


# Serializer for PaymentCommitment.
class PaymentCommitmentSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = PaymentCommitment
        fields = [
            "alias",
            "adverse",
            "commitment_type",
            "loan_company_name",
            "date_cleared",
            "missed_payments_in_the_last_three_months",
            "missed_payments_in_the_last_twelve_months",
            "missed_payments_in_the_last_twenty_four_months",
            "missed_payments_in_the_last_thirty_six_months",
            "missed_payments_in_the_last_sixty_months",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "adverse",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


# Serializer for PropertyRepossessed
class PropertyRepossessedSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = PropertyRepossessed
        fields = [
            "alias",
            "adverse",
            "lender",
            "date_of_registration",
            "date_of_satisfaction",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "adverse",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


class BankruptSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = Bankrupt
        fields = [
            "alias",
            "adverse",
            "date_discharged",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "adverse",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


class IndividualVoluntarySerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = IndividualVoluntary
        fields = [
            "alias",
            "adverse",
            "date_registered",
            "outstanding_balance",
            "satisfied",
            "date_satisfied",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "adverse",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


class DebtManagementPlanSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = DebtManagementPlan
        fields = [
            "alias",
            "adverse",
            "plan",
            "loan_company_name",
            "date_registered",
            "outstanding_balance",
            "satisfied",
            "date_satisfied",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "adverse",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


class PayDayLoanSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = PayDayLoan
        fields = [
            "alias",
            "adverse",
            "loan_amount",
            "loan_date",
            "has_the_pay_day_loan_been_repaid",
            "date_repaid",
            "lender_name",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "adverse",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


class PropertySerializer(serializers.ModelSerializer):
    """Serializer for Property model."""

    case = CommonCaseSerializer(read_only=True)
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    # Read-only: Shows applicant details
    applicant = CommonUserWithIdSerializer(many=True, read_only=True)

    # Write-only: Accepts list of applicant IDs
    applicant_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), many=True, write_only=True, source="applicant"
    )

    class Meta:
        model = Property
        fields = [
            "alias",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "case",
            "applicant",
            "applicant_ids",
            "is_property_owner",
            "postcode",
            "house_name_or_number",
            "address_1",
            "address_2",
            "city",
            "county",
            "country",
            "property_value",
            "current_mortgage_balance",
            "monthly_rental_income",
            "monthly_mortgage_payment",
            "value_at_purchase",
            "date_purchased",
            "is_hmo",
            "is_mufb",
            "mortgage_lender",
            "repayment_type",
            "to_be_repaid",
            "current_rate",
            "rate_type",
            "current_rate_end_date",
            "erc_end_date",
            "account_number",
            "property_type",
            "ownership",
            "leasehold",
            "year_built",
            "number_of_bedrooms",
            "remaining_mortgage_term",
            "is_limited_company",
            "epc_rating",
        ]
        read_only_fields = ["alias", "case", "created_at", "updated_at"]

    def validate_applicant_ids(self, value):
        """Ensure applicants are only lead or joint users from the case"""

        # Ensure that value is a list of integers, not a list of User objects
        if any(isinstance(user, User) for user in value):
            value = [user.id for user in value]  # Convert Users to IDs

        case_alias = self.context["view"].kwargs.get("case_alias")
        case = Case.objects.filter(alias=case_alias).first()

        if not case:
            raise serializers.ValidationError("Invalid case alias provided.")

        # Get valid applicants (lead + joint users) as a set of IDs
        valid_applicants = {case.lead.id}  # Lead user ID
        valid_applicants.update(
            JointUser.objects.filter(case=case).values_list("joint_user_id", flat=True)
        )  # Joint user IDs

        # Convert values to integer IDs (if necessary)
        try:
            input_applicant_ids = {
                int(user_id) for user_id in value
            }  # Ensure all IDs are integers
        except (ValueError, TypeError):
            raise serializers.ValidationError("Applicant IDs must be valid integers.")

        # Check if all submitted IDs are valid
        invalid_applicants = input_applicant_ids - valid_applicants

        if invalid_applicants:
            raise serializers.ValidationError(
                f"Invalid applicant IDs: {list(invalid_applicants)}. "
                f"Valid applicant IDs: {list(valid_applicants)}"
            )

        return value  # Return validated IDs

    def create(self, validated_data):
        """Ensure applicants are only lead or joint users from the case"""
        applicant_ids = validated_data.pop("applicant", [])  # Source is "applicant"
        property_instance = super().create(validated_data)
        property_instance.applicant.set(
            applicant_ids
        )  # Correctly setting Many-to-Many field
        return property_instance

    def update(self, instance, validated_data):
        """Allow updating applicant list if needed"""
        applicant_ids = validated_data.pop("applicant", None)
        instance = super().update(instance, validated_data)
        if applicant_ids is not None:
            instance.applicant.set(applicant_ids)
        return instance


class SolicitorAccountantSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = SolicitorAccountant
        fields = [
            "id",
            "alias",
            "name",
            "company_name",
            "user_type",
            "sra_number",
            "postcode",
            "building_name_or_number",
            "street",
            "city",
            "county",
            "country",
            "phone_number",
            "fax_number",
            "dx_number",
            "contact_name",
            "email_address",
            "number_of_partners_in_firm",
            "qualifications",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "user_type",
        ]


class CommonSolicitorAccountantSerializer(serializers.ModelSerializer):

    class Meta:
        model = SolicitorAccountant
        fields = [
            "id",
            "alias",
            "name",
            "user_type",
        ]
        read_only_fields = [
            "id",
            "alias",
            "name",
            "user_type",
        ]


class CaseSolicitorSerializer(serializers.ModelSerializer):
    case = CommonCaseSerializer(read_only=True)

    solicitor_details = CommonSolicitorAccountantSerializer(
        read_only=True, source="solicitor"
    )
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = CaseSolicitor
        fields = [
            "alias",
            "case",
            "solicitor",
            "solicitor_details",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        write_only_fields = [
            "solicitor",
        ]

    def validate_solicitor(self, value):
        if value.user_type != SolicitorTypeChoices.SOLICITOR:
            raise serializers.ValidationError(
                "The solicitor must have user_type='solicitor'."
            )
        return value


class CaseAccountantSerializer(serializers.ModelSerializer):
    case = CommonCaseSerializer(read_only=True)

    accountant_details = CommonSolicitorAccountantSerializer(
        read_only=True, source="accountant"
    )
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = CaseAccountant
        fields = [
            "alias",
            "case",
            "accountant",
            "accountant_details",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        write_only_fields = [
            "accountant",
        ]

    def validate_accountant(self, value):
        if value.user_type != SolicitorTypeChoices.ACCOUNTANT:
            raise serializers.ValidationError(
                "The accountant must have user_type='ACCOUNTANT'."
            )
        return value


class ExistingProtectionSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)
    user = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = ExistingProtection
        fields = [
            "alias",
            "case",
            "user",
            "have_any_existing_Protection_policies_in_place",
            "policy_type",
            "policy_provider",
            "insurers_reference",
            "sum_assured",
            "premium",
            "premium_payment_type",
            "person_assured",
            "in_trust",
            "guaranteed_reviewable",
            "remaining_policy_term",
            "cancelled_lapsed_date",
            "renewal_date",
            "date_policy_started",
            "waiver_of_premium",
            "indexation",
            "death_in_service_provision",
            "have_non_standard_terms_been_issued",
            "copy_and_paste_non_standard_terms_from_lender",
            "will_this_policy_be_cancelled",
            "reason_for_policy_cancellation",
            "policy_cancellation_notes",
            "why_did_you_take_out_this_policy",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "case",
            "user",
            "alias",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


class NotesSerializer(serializers.ModelSerializer):
    case = CommonCaseSerializer(read_only=True)
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = Notes
        fields = [
            "alias",
            "case",
            "note_task",
            "note_visible_to_introducer",
            "note_visible_to_client",
            "category",
            "task_priority",
            "due_date",
            "assigned_to",
            "note",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "case",
            "alias",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


class PropertyDetailsSerializer(serializers.ModelSerializer):
    case = CommonCaseSerializer(read_only=True)
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = PropertyDetails
        fields = [
            "alias",
            "case",
            "property_purchase_price",
            "property_estimated_valuation",
            "have_you_found_a_property_yet",
            "notes",
            "postcode",
            "house_name_or_number",
            "address_one",
            "address_two",
            "city",
            "county",
            "region",
            "country",
            "property_type",
            "house_type",
            "flat_type",
            "construction_of_walls",
            "construction_of_roof",
            "bedrooms",
            "bathrooms",
            "reception_rooms",
            "kitchens",
            "garages",
            "parking_spaces",
            "charge_type",
            "epc_rating",
            "floor",
            "flats",
            "number_of_storeys_in_the_building",
            "year_built",
            "lift_access",
            "tenure",
            "property_lease_term",
            "service_charge_per_month",
            "ground_rent_per_annum",
            "residential",
            "commercial",
            "is_the_property_a_listed_building",
            "number_of_units",
            "listed_status_of_the_building",
            "listed_building_notes",
            "do_you_or_will_you_own_part_or_all_of_the_freehold",
            "is_the_property_part_of_a_help_to_buy_shared_ownership_scheme",
            "is_the_property_above_or_near_commercial_premises",
            "is_the_property_a_new_build",
            "new_build_warranty_provider",
            "other_new_build_warranty_rovider",
            "is_the_property_a_right_to_buy",
            "date_of_purchase",
            "discounted_price",
            "is_the_property_ex_local_authority",
            "is_this_property_being_purchased_from_the_council_with_this_application",
            "is_there_an_annexe_within_the_property",
            "will_the_property_be_owner_occupied",
            "please_provide_further_details",
            "is_the_property_on_the_market",
            "is_the_property_rented_out_to_be_rented_out",
            "is_the_property_standard_construction",
            "comments_details",
            "does_the_property_have_solar_panels",
            "do_you_own_the_solar_panels",
            "is_the_property_used_purely_for_residential_purposes",
            "valuation_type",
            "select_applicant_list",
            "contact_for_access",
            "contacts_name",
            "contacts_daytime_telephone",
            "contacts_mobile_telephone",
            "contacts_email_address",
            "estimated_value",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "case",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


class OtherOccupantsSerializer(serializers.ModelSerializer):
    case = CommonCaseSerializer(read_only=True)
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = OtherOccupants
        fields = [
            "alias",
            "case",
            "full_name",
            "date_of_birth",
            "relationship",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "case",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


class ProductSerializer(serializers.ModelSerializer):
    case = CommonCaseSerializer(read_only=True)
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = Product
        fields = [
            "alias",
            "case",
            "product_description",
            "initial_rate",
            "initial_rate_type",
            "initial_rate_period_type",
            "reversion_rate",
            "initial_rate_period",
            "initial_rate_date_period",
            "max_ltv",
            "annual_percentage_rate",
            "product_class",
            "early_repayment_charge",
            "early_repayment_charge_end_date",
            "initial_monthly_payment",
            "initial_monthly_payment_including_fees",
            "monthly_payment_after_initial_Period",
            "true_cost_over_initial_period",
            "true_cost_over_term",
            "true_cost_without_fees",
            "loan_required_including_fees",
            "arrangement_fee",
            "arrangement_fee_added_to_loan",
            "valuation_fee",
            "booking_fee",
            "booking_fee_added_to_loan",
            "procuration_fee",
            "processing_consent",
            "processing_consent_description",
            "application_review",
            "application_review_description",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "alias",
            "case",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]


class IncomeSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = Income
        fields = [
            "alias",
            # domain-specific fields:
            "income_type",
            "applicant_one_net_monthly_income",
            "applicant_two_net_monthly_income",
            "rental_income",
            "part_time_income",
            "jobseekers_allowance",
            "child_benefit",
            "tax_credits",
            "working_tax_credits",
            "maintenance",
            "pension",
            "other_benefits",
            "total_income",
            # base fields:
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "income_type",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


class DebtRepaymentsSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = DebtRepayments
        fields = [
            "alias",
            "repayment_type",
            "mortgage_rent",
            "second_mortgage",
            "shared_ownership_rental",
            "total_debt_repayment",
            # base fields:
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "repayment_type",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


class PriorityDebtSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = PriorityDebt
        fields = [
            "alias",
            "debt_type",
            "mortgage_arrears",
            "gas_arrears",
            "maintenance_arrears",
            "defaults",
            "ccjs",
            "debt_management_plans",
            "magistrate_court_fines",
            "council_tax_arrears",
            "total_priority_debt",
            # base fields:
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "debt_type",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


class UnsecuredBorrowingSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = UnsecuredBorrowing
        fields = [
            "alias",
            "borrowing_type",
            "credit_cards",
            "loans",
            "car_finance",
            "overdraft",
            "store_cards",
            "student_loans",
            "other_borrowing",
            "total_unsecured_borrowing",
            # base fields:
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "borrowing_type",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


class LivingCostsSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = LivingCosts
        fields = [
            "alias",
            "cost_type",
            "electricity",
            "gas",
            "water",
            "landline_mobile_phone",
            "tv_license",
            "council_tax",
            "ground_rent_service_charges",
            "buildings_contents",
            "mortgage_payment_protection",
            "endowment",
            "pension_contribution",
            "childcare",
            "maintenance",
            "food",
            "car_maintenance",
            "fuel",
            "public_transport",
            "tv_broadband",
            "recreation_holidays",
            "clothing",
            "medical_expenses",
            "education",
            "other_living_costs",
            "total_living_expenses",
            # base fields:
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "cost_type",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


class InsurancesSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = Insurances
        fields = [
            "alias",
            "insurance_type",
            "motor_insurance",
            "health_insurance",
            "payment_protection",
            "life_insurance",
            "dental_insurance",
            "other_insurance",
            "total_insurance_expenses",
            # base fields:
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "insurance_type",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


class SubTotalsSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = SubTotals
        fields = [
            "subtotal_type",
            "total_income",
            "total_debt_repayment",
            "total_living_expenses",
            "available_income",
            # base fields:
            "alias",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "subtotal_type",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


class BudgetPlannerSerializer(serializers.ModelSerializer):
    # Nested sub-model serializers
    current_income = IncomeSerializer(required=False)
    post_income = IncomeSerializer(required=False)
    current_debt_repayments = DebtRepaymentsSerializer(required=False)
    post_debt_repayments = DebtRepaymentsSerializer(required=False)
    current_priority_debt = PriorityDebtSerializer(required=False)
    post_priority_debt = PriorityDebtSerializer(required=False)
    current_unsecured_borrowing = UnsecuredBorrowingSerializer(required=False)
    post_unsecured_borrowing = UnsecuredBorrowingSerializer(required=False)
    current_living_cost = LivingCostsSerializer(required=False)
    post_living_cost = LivingCostsSerializer(required=False)
    current_insurance = InsurancesSerializer(required=False)
    post_insurance = InsurancesSerializer(required=False)
    current_sub_total = SubTotalsSerializer(required=False)
    post_sub_total = SubTotalsSerializer(required=False)
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)
    case = CommonCaseSerializer(read_only=True)

    class Meta:
        model = BudgetPlanner
        fields = [
            "alias",
            "case",
            "current_income",
            "post_income",
            "current_debt_repayments",
            "post_debt_repayments",
            "current_priority_debt",
            "post_priority_debt",
            "current_unsecured_borrowing",
            "post_unsecured_borrowing",
            "current_living_cost",
            "post_living_cost",
            "current_insurance",
            "post_insurance",
            "current_sub_total",
            "post_sub_total",
            "disclaimer",
            "disclaimer_details",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "case",  # we’ll assign the case automatically
        ]

    def create(self, validated_data):
        """
        Create the BudgetPlanner along with its related models, in a single transaction,
        setting created_by and updated_by to request.user.
        """
        request_user = self.context["request"].user

        # Pop nested data for sub-model creation
        current_income_data = validated_data.pop("current_income", None)
        post_income_data = validated_data.pop("post_income", None)
        current_debt_repayment_data = validated_data.pop(
            "current_debt_repayments", None
        )
        post_debt_repayment_data = validated_data.pop("post_debt_repayments", None)
        current_priority_debt_data = validated_data.pop("current_priority_debt", None)
        post_priority_debt_data = validated_data.pop("post_priority_debt", None)
        current_unsecured_borrowing_data = validated_data.pop(
            "current_unsecured_borrowing", None
        )
        post_unsecured_borrowing_data = validated_data.pop(
            "post_unsecured_borrowing", None
        )
        current_living_cost_data = validated_data.pop("current_living_cost", None)
        post_living_cost_data = validated_data.pop("post_living_cost", None)
        current_insurance_data = validated_data.pop("current_insurance", None)
        post_insurance_data = validated_data.pop("post_insurance", None)
        current_sub_total_data = validated_data.pop("current_sub_total", None)
        post_sub_total_data = validated_data.pop("post_sub_total", None)

        with transaction.atomic():
            # Create sub-objects if data is present
            current_income = (
                Income.objects.create(
                    created_by=request_user,
                    updated_by=request_user,
                    **current_income_data,
                )
                if current_income_data
                else None
            )

            post_income = (
                Income.objects.create(
                    created_by=request_user,
                    updated_by=request_user,
                    income_type=IncomeTypeChoices.POST_COMPLETION_INCOME,
                    **post_income_data,
                )
                if post_income_data
                else None
            )

            current_debt_repayments = (
                DebtRepayments.objects.create(
                    created_by=request_user,
                    updated_by=request_user,
                    **current_debt_repayment_data,
                )
                if current_debt_repayment_data
                else None
            )

            post_debt_repayments = (
                DebtRepayments.objects.create(
                    created_by=request_user,
                    updated_by=request_user,
                    repayment_type=DebtRepaymentTypeChoices.POST_COMPLETION_DEBT_REPAYMENTS,
                    **post_debt_repayment_data,
                )
                if post_debt_repayment_data
                else None
            )

            current_priority_debt = (
                PriorityDebt.objects.create(
                    created_by=request_user,
                    updated_by=request_user,
                    **current_priority_debt_data,
                )
                if current_priority_debt_data
                else None
            )

            post_priority_debt = (
                PriorityDebt.objects.create(
                    created_by=request_user,
                    updated_by=request_user,
                    debt_type=PriorityDebtTypeChoices.POST_COMPLETION_PRIORITY_DEBT,
                    **post_priority_debt_data,
                )
                if post_priority_debt_data
                else None
            )

            current_unsecured_borrowing = (
                UnsecuredBorrowing.objects.create(
                    created_by=request_user,
                    updated_by=request_user,
                    **current_unsecured_borrowing_data,
                )
                if current_unsecured_borrowing_data
                else None
            )

            post_unsecured_borrowing = (
                UnsecuredBorrowing.objects.create(
                    created_by=request_user,
                    updated_by=request_user,
                    borrowing_type=UnsecuredBorrowingTypeChoices.POST_COMPLETION_UNSECURED_BORROWING,
                    **post_unsecured_borrowing_data,
                )
                if post_unsecured_borrowing_data
                else None
            )

            current_living_cost = (
                LivingCosts.objects.create(
                    created_by=request_user,
                    updated_by=request_user,
                    **current_living_cost_data,
                )
                if current_living_cost_data
                else None
            )

            post_living_cost = (
                LivingCosts.objects.create(
                    created_by=request_user,
                    updated_by=request_user,
                    cost_type=LivingCostsTypeChoices.POST_COMPLETION_LIVING_COSTS,
                    **post_living_cost_data,
                )
                if post_living_cost_data
                else None
            )

            current_insurance = (
                Insurances.objects.create(
                    created_by=request_user,
                    updated_by=request_user,
                    **current_insurance_data,
                )
                if current_insurance_data
                else None
            )

            post_insurance = (
                Insurances.objects.create(
                    created_by=request_user,
                    updated_by=request_user,
                    insurance_type=InsuranceTypeChoices.POST_COMPLETION_INSURANCES,
                    **post_insurance_data,
                )
                if post_insurance_data
                else None
            )

            current_sub_total = (
                SubTotals.objects.create(
                    created_by=request_user,
                    updated_by=request_user,
                    **current_sub_total_data,
                )
                if current_sub_total_data
                else None
            )

            post_sub_total = (
                SubTotals.objects.create(
                    created_by=request_user,
                    updated_by=request_user,
                    subtotal_type=SubTotalsTypeChoices.POST_COMPLETION_SUB_TOTALS,
                    **post_sub_total_data,
                )
                if post_sub_total_data
                else None
            )

            # Now create the BudgetPlanner
            budget_planner = BudgetPlanner.objects.create(
                **validated_data,
                current_income=current_income,
                post_income=post_income,
                current_debt_repayments=current_debt_repayments,
                post_debt_repayments=post_debt_repayments,
                current_priority_debt=current_priority_debt,
                post_priority_debt=post_priority_debt,
                current_unsecured_borrowing=current_unsecured_borrowing,
                post_unsecured_borrowing=post_unsecured_borrowing,
                current_living_cost=current_living_cost,
                post_living_cost=post_living_cost,
                current_insurance=current_insurance,
                post_insurance=post_insurance,
                current_sub_total=current_sub_total,
                post_sub_total=post_sub_total,
                created_by=request_user,
                updated_by=request_user,
            )

        return budget_planner

    def update(self, instance, validated_data):
        request_user = self.context["request"].user
        instance.updated_by = request_user

        instance.disclaimer = validated_data.get("disclaimer", instance.disclaimer)
        instance.disclaimer_details = validated_data.get(
            "disclaimer_details", instance.disclaimer_details
        )
        nested_fields = [
            "current_income",
            "post_income",
            "current_debt_repayments",
            "post_debt_repayments",
            "current_priority_debt",
            "post_priority_debt",
            "current_unsecured_borrowing",
            "post_unsecured_borrowing",
            "current_living_cost",
            "post_living_cost",
            "current_insurance",
            "post_insurance",
            "current_sub_total",
            "post_sub_total",
        ]

        for field in nested_fields:
            nested_data = validated_data.get(field, None)
            related_instance = getattr(instance, field, None)

            if nested_data:
                if related_instance:
                    for attr, value in nested_data.items():
                        setattr(related_instance, attr, value)
                    related_instance.updated_by = request_user
                    related_instance.save()
                else:
                    model_class = self.fields[field].Meta.model
                    new_instance = model_class.objects.create(
                        **nested_data,
                        created_by=request_user,
                        updated_by=request_user,
                    )
                    setattr(instance, field, new_instance)

        instance.save()
        return instance


class FeesSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)
    case = CommonCaseSerializer(read_only=True)

    class Meta:
        model = Fees
        fields = [
            "alias",
            "case",
            "fees_type",
            "amount",
            "fee_in_type",
            "fee_out_type",
            "method",
            "notes",
            "date_received",
            "date_paid_out",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "case",
            "fees_type",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


class DipHistorySerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)
    case = CommonCaseSerializer(read_only=True)

    class Meta:
        model = DipHistory
        fields = [
            "alias",
            "case",
            "is_this_application_had_a_decision_in_principle",
            "notes",
            "lender",
            "dip_date",
            "dip_decision",
            "dip_reference_number",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "case",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


class CreditCommitmentsSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)
    applicant_details = CommonUserWithIdSerializer(source="applicant", read_only=True)

    class Meta:
        model = CreditCommitments
        fields = [
            "alias",
            "case",
            "applicant",
            "applicant_details",
            "joint",
            "type",
            "company",
            "account_no",
            "os_balance",
            "settlement_balance",
            "monthly_repayment",
            "interest_rate",
            "card_limit",
            "term_remaining",
            "balloon_payment",
            "court_ordered",
            "cost_of_credit",
            "paid_on_completion",
            "source",
            "has_the_unsecured_credit_mounted_up",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "case",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        write_only_fields = ["applicant"]


class ExtraQuestionSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = ExtraQuestion
        fields = [
            "alias",
            "answer",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]

    def create(self, validated_data):
        user = self.context["request"].user  # Get user from context
        validated_data["created_by"] = user
        validated_data["updated_by"] = user
        return ExtraQuestion.objects.create(**validated_data)

    def update(self, instance, validated_data):
        user = self.context["request"].user
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.updated_by = user
        instance.save()
        return instance


class CircumstancesObjectivesSerializer(serializers.ModelSerializer):

    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = CircumstancesObjectives
        fields = [
            "alias",
            "question_one",
            "question_one_answer",
            "question_one_sharia",
            "question_two",
            "question_two_answer",
            "question_two_sharia",
            "question_three",
            "question_three_answer",
            "circumstances_type",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        user = self.context["request"].user

        validated_data["created_by"] = user
        validated_data["updated_by"] = user

        instance = CircumstancesObjectives.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        user = self.context["request"].user

        # Handle updated_by field
        instance.updated_by = user

        # Update NewMortgageDetails instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class BudgetAffordabilitySerializer(serializers.ModelSerializer):

    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = BudgetAffordability
        fields = [
            "alias",
            "question_one",
            "question_one_answer",
            "question_one_sharia",
            "question_two",
            "question_two_answer",
            "question_two_sharia",
            "budget_affordability_type",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "alias",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        user = self.context["request"].user

        validated_data["created_by"] = user
        validated_data["updated_by"] = user
        return BudgetAffordability.objects.create(**validated_data)

    def update(self, instance, validated_data):
        user = self.context["request"].user

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.updated_by = user
        instance.save()
        return instance


class NewMortgageDetailsSerializer(serializers.ModelSerializer):

    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = NewMortgageDetails
        fields = [
            "alias",
            "question_one",
            "question_one_answer",
            "question_one_sharia",
            "question_two",
            "question_two_answer",
            "question_two_sharia",
            "new_mortgage_details_type",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "alias",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]

    def create(self, validated_data):
        user = self.context["request"].user

        validated_data["created_by"] = user
        validated_data["updated_by"] = user

        instance = NewMortgageDetails.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        user = self.context["request"].user

        instance.updated_by = user

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class RecommendingRepaymentMethodSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = RecommendingRepaymentMethod
        fields = [
            "alias",
            "question_one",
            "question_one_answer",
            "question_one_sharia",
            "question_two",
            "question_two_answer",
            "question_two_sharia",
            "question_three",
            "question_three_answer",
            "question_four",
            "question_four_answer",
            "question_five",
            "question_five_answer",
            "recommending_repayment_method_type",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "alias",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        user = self.context["request"].user

        validated_data["created_by"] = user
        validated_data["updated_by"] = user

        instance = RecommendingRepaymentMethod.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        user = self.context["request"].user

        instance.updated_by = user

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class RecommendingMortgageTypeSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = RecommendingMortgageType
        fields = [
            "alias",
            "question_one",
            "question_one_answer",
            "question_one_sharia",
            "question_two",
            "question_two_answer",
            "question_two_sharia",
            "question_three",
            "question_three_answer",
            "question_four",
            "question_four_answer",
            "recommending_mortgage_type",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "alias",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        validated_data["updated_by"] = user

        instance = RecommendingMortgageType.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        user = self.context["request"].user
        instance.updated_by = user

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class RecommendingTermSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = RecommendingTerm
        fields = [
            "alias",
            "question_one",
            "question_one_answer",
            "recommending_term",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "alias",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        user = self.context["request"].user

        validated_data["created_by"] = user
        validated_data["updated_by"] = user

        instance = RecommendingTerm.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        user = self.context["request"].user
        instance.updated_by = user

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class RecommendingMortgageLenderSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = RecommendingMortgageLender
        fields = [
            "alias",
            "question_one",
            "question_one_answer",
            "question_one_sharia",
            "question_two",
            "question_two_answer",
            "question_three",
            "question_three_answer",
            "recommending_mortgage_lender_type",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "alias",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        # Set created_by and updated_by fields
        validated_data["created_by"] = user
        validated_data["updated_by"] = user

        instance = RecommendingMortgageLender.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        user = self.context["request"].user
        instance.updated_by = user

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class RecommendingMortgageAmountSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = RecommendingMortgageAmount
        fields = [
            "alias",
            "question_one",
            "question_one_answer",
            "question_one_sharia",
            "question_two",
            "question_two_answer",
            "question_three",
            "question_three_answer",
            "recommending_mortgage_amount",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "alias",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        validated_data["updated_by"] = user

        instance = RecommendingMortgageAmount.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        user = self.context["request"].user

        instance.updated_by = user

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class CostsFeesSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = CostsFees
        fields = [
            "alias",
            "question_one",
            "question_one_answer",
            "question_one_sharia",
            "question_two",
            "question_two_answer",
            "question_three",
            "question_three_answer",
            "costs_fees",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "alias",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        user = self.context["request"].user

        validated_data["created_by"] = user
        validated_data["updated_by"] = user

        instance = CostsFees.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        user = self.context["request"].user

        instance.updated_by = user

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class DisadvantageRisksSerializer(serializers.ModelSerializer):

    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = DisadvantageRisks
        fields = [
            "alias",
            "question_one",
            "question_one_answer",
            "question_one_sharia",
            "question_two",
            "question_two_answer",
            "question_three",
            "question_three_answer",
            "question_four",
            "question_four_answer",
            "question_five",
            "question_five_answer",
            "question_six",
            "question_six_answer",
            "question_seven",
            "question_seven_answer",
            "question_eight",
            "question_eight_answer",
            "question_nine",
            "question_nine_answer",
            "disadvantage_risks",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "alias",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        validated_data["updated_by"] = user

        instance = DisadvantageRisks.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        user = self.context["request"].user

        instance.updated_by = user

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class CostAdviceSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = CostAdvice
        fields = [
            "alias",
            "question_one",
            "question_one_answer",
            "question_one_sharia",
            "question_two",
            "question_two_answer",
            "question_two_sharia",
            "cost_advice",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "alias",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        validated_data["updated_by"] = user

        instance = CostAdvice.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        user = self.context["request"].user

        instance.updated_by = user

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ProtectionSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = Protection
        fields = [
            "alias",
            "question_one",
            "question_one_answer",
            "question_one_sharia",
            "question_two",
            "question_two_answer",
            "question_three",
            "question_three_answer",
            "question_three_sharia",
            "question_four",
            "question_four_answer",
            "question_four_sharia",
            "protection",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "alias",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        user = self.context["request"].user

        validated_data["created_by"] = user
        validated_data["updated_by"] = user

        instance = Protection.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        user = self.context["request"].user
        instance.updated_by = user

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class BuildingsInsuranceSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = BuildingsInsurance
        fields = [
            "alias",
            "question_one",
            "question_one_answer",
            "question_two",
            "question_two_answer",
            "question_three",
            "question_three_answer",
            "question_three_sharia",
            "question_four",
            "question_four_answer",
            "question_five_sharia",
            "buildings_insurance",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "alias",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        user = self.context["request"].user

        validated_data["created_by"] = user
        validated_data["updated_by"] = user

        instance = BuildingsInsurance.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        user = self.context["request"].user

        instance.updated_by = user

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class WillsSerializer(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = Wills
        fields = [
            "alias",
            "question_one",
            "question_one_answer",
            "question_two",
            "question_two_answer",
            "question_three",
            "question_three_answer",
            "wills",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "alias",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["created_by"] = user
        validated_data["updated_by"] = user

        instance = Wills.objects.create(**validated_data)
        return instance

    def update(self, instance, validated_data):
        user = self.context["request"].user
        instance.updated_by = user

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class SuitabilitySerializer(serializers.ModelSerializer):
    circumstances_objectives = CircumstancesObjectivesSerializer(required=False)
    budget_affordability = BudgetAffordabilitySerializer(required=False)
    new_mortgage_details = NewMortgageDetailsSerializer(required=False)
    recommending_repayment_method = RecommendingRepaymentMethodSerializer(
        required=False
    )
    recommending_mortgage_type = RecommendingMortgageTypeSerializer(required=False)
    recommending_term = RecommendingTermSerializer(required=False)
    recommending_mortgage_lender = RecommendingMortgageLenderSerializer(required=False)
    recommending_mortgage_amount = RecommendingMortgageAmountSerializer(required=False)
    costs_fees = CostsFeesSerializer(required=False)
    disadvantage_risks = DisadvantageRisksSerializer(required=False)
    cost_advice = CostAdviceSerializer(required=False)
    protection = ProtectionSerializer(required=False)
    buildings_insurance = BuildingsInsuranceSerializer(required=False)
    wills = WillsSerializer(required=False)

    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)
    case = CommonCaseSerializer(read_only=True)

    class Meta:
        model = Suitability
        fields = [
            "alias",
            "case",
            "circumstances_objectives",
            "budget_affordability",
            "new_mortgage_details",
            "recommending_repayment_method",
            "recommending_mortgage_type",
            "recommending_term",
            "recommending_mortgage_lender",
            "recommending_mortgage_amount",
            "costs_fees",
            "disadvantage_risks",
            "cost_advice",
            "protection",
            "buildings_insurance",
            "wills",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "case",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]

    def create(self, validated_data):
        nested_instances = {}
        nested_serializers = {
            "circumstances_objectives": CircumstancesObjectivesSerializer,
            "budget_affordability": BudgetAffordabilitySerializer,
            "new_mortgage_details": NewMortgageDetailsSerializer,
            "recommending_repayment_method": RecommendingRepaymentMethodSerializer,
            "recommending_mortgage_type": RecommendingMortgageTypeSerializer,
            "recommending_term": RecommendingTermSerializer,
            "recommending_mortgage_lender": RecommendingMortgageLenderSerializer,
            "recommending_mortgage_amount": RecommendingMortgageAmountSerializer,
            "costs_fees": CostsFeesSerializer,
            "disadvantage_risks": DisadvantageRisksSerializer,
            "cost_advice": CostAdviceSerializer,
            "protection": ProtectionSerializer,
            "buildings_insurance": BuildingsInsuranceSerializer,
            "wills": WillsSerializer,
        }

        for field_name, serializer_class in nested_serializers.items():
            nested_data = validated_data.pop(field_name, None)
            if nested_data:
                serializer = serializer_class(data=nested_data, context=self.context)
                serializer.is_valid(raise_exception=True)
                nested_instances[field_name] = serializer.save()

        suitability = Suitability.objects.create(**validated_data)

        for field_name, instance in nested_instances.items():
            setattr(suitability, field_name, instance)

        suitability.save()
        return suitability

    def update(self, instance, validated_data):
        nested_serializers = {
            "circumstances_objectives": CircumstancesObjectivesSerializer,
            "budget_affordability": BudgetAffordabilitySerializer,
            "new_mortgage_details": NewMortgageDetailsSerializer,
            "recommending_repayment_method": RecommendingRepaymentMethodSerializer,
            "recommending_mortgage_type": RecommendingMortgageTypeSerializer,
            "recommending_term": RecommendingTermSerializer,
            "recommending_mortgage_lender": RecommendingMortgageLenderSerializer,
            "recommending_mortgage_amount": RecommendingMortgageAmountSerializer,
            "costs_fees": CostsFeesSerializer,
            "disadvantage_risks": DisadvantageRisksSerializer,
            "cost_advice": CostAdviceSerializer,
            "protection": ProtectionSerializer,
            "buildings_insurance": BuildingsInsuranceSerializer,
            "wills": WillsSerializer,
        }

        for field_name, serializer_class in nested_serializers.items():
            nested_data = validated_data.pop(field_name, None)
            if nested_data:
                nested_instance = getattr(instance, field_name, None)
                if nested_instance:
                    serializer = serializer_class(
                        instance=nested_instance,
                        data=nested_data,
                        context=self.context,
                        partial=True,
                    )
                    serializer.is_valid(raise_exception=True)
                    serializer.save()
                else:
                    serializer = serializer_class(
                        data=nested_data, context=self.context
                    )
                    serializer.is_valid(raise_exception=True)
                    nested_instance = serializer.save()
                    setattr(instance, field_name, nested_instance)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance


class ExtraAnswerSerializers(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)
    case = CommonCaseSerializer(read_only=True)

    class Meta:
        model = ExtraAnswer
        fields = [
            "alias",
            "case",
            "section_choices",
            "answer",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]
        read_only_fields = [
            "alias",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
        ]


class ComplianceSerializers(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)
    case = CommonCaseSerializer(read_only=True)

    class Meta:
        model = Compliance
        fields = [
            "alias",
            "case",
            "date_file_checked",
            "date_file_rechecked",
            "file_checked",
            "remedial_actions_required",
            "remedial_actions_complete",
            "comments",
            "rating_a",
            "rating_b",
            "rating_c",
            "terms_of_business",
            "terms_of_business_text",
            "privacy_notice",
            "privacy_notice_text",
            "fee_agreement",
            "fee_agreement_text",
            "factfind_filled",
            "factfind_filled_text",
            "nivo_idv_check",
            "nivo_idv_check_text",
            "financial_sanctions_checked",
            "financial_sanctions_checked_text",
            "proof_of_id",
            "proof_of_id_text",
            "proof_of_address",
            "proof_of_address_text",
            "proof_of_income",
            "proof_of_income_text",
            "proof_of_deposit",
            "proof_of_deposit_text",
            "bank_statements",
            "bank_statements_text",
            "credit_reports",
            "credit_reports_text",
            "affordability_calculator",
            "affordability_calculator_text",
            "evidence_of_research",
            "evidence_of_research_text",
            "agreement_in_principle",
            "agreement_in_principle_text",
            "signed_application",
            "signed_application_text",
            "suitability_letter",
            "suitability_letter_text",
            "mortgage_offer",
            "mortgage_offer_text",
            "debt_consolidation_calculator",
            "debt_consolidation_calculator_text",
            "shared_equity_documentation",
            "shared_equity_documentation_text",
            "proof_of_lending",
            "proof_of_lending_text",
            "proof_of_repayment",
            "proof_of_repayment_text",
            "loan_details_fully_completed",
            "loan_details_fully_completed_text",
            "has_source_of_lead_been_recorded",
            "has_source_of_lead_been_recorded_text",
            "realistic_proximity_to_the_advisor",
            "realistic_proximity_to_the_advisor_text",
            "personal_details",
            "personal_details_text",
            "retirement_age",
            "retirement_age_text",
            "does_the_occupation_compared",
            "does_the_occupation_compared_text",
            "employment_details",
            "employment_details_text",
            "has_due_diligence_been_completed",
            "has_due_diligence_been_completed_text",
            "does_the_stated_income",
            "does_the_stated_income_text",
            "does_the_stated_net_income",
            "does_the_stated_net_income_text",
            "is_the_client_in_an_occupation",
            "is_the_client_in_an_occupation_text",
            "has_property_portfolio_fully_completed",
            "has_property_portfolio_fully_completed_text",
            "has_proposed_property_details_fully_completed",
            "has_proposed_property_details_fully_completed_text",
            "has_your_needs_fully_completed",
            "has_your_needs_fully_completed_text",
            "has_repayment_vehicle_recorded",
            "has_repayment_vehicle_recorded_text",
            "have_figures_been_input",
            "have_figures_been_input_text",
            "is_deposit_come_from_sale_of_property",
            "is_deposit_come_from_sale_of_property_text",
            "has_adviser_completed_calculator",
            "has_adviser_completed_calculator_text",
            "has_accountant_solicitor_details_confirmed",
            "has_accountant_solicitor_details_confirmed_text",
            "has_credit_commitments_fully_completed",
            "has_credit_commitments_fully_completed_text",
            "is_any_credit_commitments",
            "is_any_credit_commitments_text",
            "has_client_adverse_credit",
            "has_client_adverse_credit_text",
            "has_budget_planner_been_completed",
            "has_budget_planner_been_completed_text",
            "has_all_direct_debits_been_recorded",
            "has_all_direct_debits_been_recorded_text",
            "has_adviser_sourced_mortgage_requirements",
            "has_adviser_sourced_mortgage_requirement_text",
            "does_figures_stated_in_mortgage_requirements",
            "does_figures_stated_in_mortgage_requirements_text",
            "are_results_stored_in_order_of_client_preference",
            "are_results_stored_in_order_of_client_preference_text",
            "is_recommended_product_showing_evidence_research",
            "is_recommended_product_showing_evidence_research_text",
            "is_the_address_on_the_kfi_correct",
            "is_the_address_on_the_kfi_correct_text",
            "does_figures_features_mortgage_requirements",
            "does_figures_features_mortgage_requirement_text",
            "does_monthly_payment_fit_within_disposable_income",
            "does_monthly_payment_fit_within_disposable_income_text",
            "are_fees_disclosed_correctly",
            "are_fees_disclosed_correctly_text",
            "lender_fees_added",
            "lender_fees_added_text",
            "has_illustration_been_produced",
            "has_illustration_been_produced_text",
            "interest_only",
            "interest_only_text",
            "has_product_been_fully_completed",
            "has_product_been_fully_completed_text",
            "personal_details_match_the_factfind",
            "personal_details_match_the_factfind_text",
            "does_employment_and_income_details_match",
            "does_employment_and_income_details_match_text",
            "does_property_loan_details_match",
            "does_property_loan_details_match_text",
            "does_mortgage_application_confirm",
            "does_mortgage_application_confirm_text",
            "has_suitability_letter_been_generated",
            "has_suitability_letter_been_generated_text",
            "post_application_changes",
            "post_application_changes_text",
            "is_applicants_live_at_separate_addresses",
            "is_applicants_live_at_separate_addresses_text",
            "is_replacement_suitability_letter",
            "is_replacement_suitability_letter_text",
            "has_reasons_for_mortgage_been_personalised",
            "has_reasons_for_mortgage_been_personalised_text",
            "has_meeting_discussion_been_personalised",
            "has_meeting_discussion_been_personalised_text",
            "has_circumstances_objectives_personalised",
            "has_circumstances_objectives_personalised_text",
            "has_budget_affordability_been_personalised",
            "has_budget_affordability_been_personalised_text",
            "has_new_mortgage_details_been_completed",
            "has_new_mortgage_details_been_complete_text",
            "has_mortgage_section_one_personalised",
            "has_mortgage_section_one_personalised_text",
            "has_mortgage_section_two_personalised",
            "has_mortgage_section_two_personalised_text",
            "are_we_recommending_repayment_method",
            "are_we_recommending_repayment_method_text",
            "are_we_recommending_mortgage_type",
            "are_we_recommending_mortgage_type_text",
            "are_we_recommending_mortgage_term",
            "are_we_recommending_mortgage_term_text",
            "are_we_recommending_mortgage_lender",
            "are_we_recommending_mortgage_lender_text",
            "are_we_recommending_mortgage_amount",
            "are_we_recommending_mortgage_amount_text",
            "are_cost_and_fees_been_completed",
            "are_cost_and_fees_been_complete_text",
            "are_disadvantages_risks_been_selected",
            "are_disadvantages_risks_been_selected_text",
            "has_adviser_personalised",
            "has_adviser_personalised_text",
            "has_adviser_included",
            "has_adviser_included_text",
            "has_protection_section_personalised",
            "has_protection_section_personalised_text",
            "has_b_and_c_section_personalised",
            "has_b_and_c_section_personalised_text",
            "has_wills_section_personalised",
            "has_wills_section_personalised_text",
            "does_recommended_product_match_your_needs_section",
            "does_recommended_product_match_your_needs_section_text",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "alias",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]


class MortgageNeedsSerializers(serializers.ModelSerializer):
    created_by = CommonUserWithIdSerializer(read_only=True)
    updated_by = CommonUserWithIdSerializer(read_only=True)
    case = CommonCaseSerializer(read_only=True)

    class Meta:
        model = MortgageNeeds
        fields = [
            "alias",
            "case",
            "repayment_method",
            "monthly_mortgage_payments",
            "specific_mortgage_deal",
            "referred_monthly_budget",
            "retirement_age",
            "what_suitable_mortgage_features_are_important",
            "front_costs",
            "is_ability_to_make_overpayments",
            "is_early_repayment_charges",
            "is_minimise_any_lender_arrangement_costs",
            "is_ability_to_add_fees_to_the_mortgage",
            "is_ability_to_add_fees_mortgage_extra_interest_will_be_payable",
            "note_one",
            "cashback",
            "portability",
            "guarantor_jbsp",
            "offset_mortgage",
            "scheme_specific",
            "speed_of_completion",
            "sharia_compliant_mortgages",
            "ltd_company_btl",
            "any_incentives",
            "note_two",
            "considering_debt_consolidation",
            "anticipate_any_changes",
            "anticipate_any_changes_notes",
            "app_one_life_cover",
            "app_one_critical_illness",
            "app_one_income_protection",
            "app_one_asu",
            "app_one_pmi",
            "app_one_family_income_benefit",
            "app_one_buildings_and_contents",
            "app_two_life_cover",
            "app_two_critical_illness",
            "app_two_income_protection",
            "app_two_asu",
            "app_two_pmi",
            "app_two_family_income_benefit",
            "app_two_buildings_and_contents",
            "buildings",
            "contents",
            "accidental_damage",
            "landlords_cover",
            "home_emergency_cover",
            "personal_possessions_cover",
            "personal_possessions_confirm",
            "have_you_a_will_in_place",
            "have_you_a_will_in_place_note",
            "mortgage_requirements_note",
            "mortgage_requirements",
            "note_three",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "alias",
            "created_by",
            "updated_by",
            "created_at",
            "updated_at",
        ]

class InsuranceCasesSubmittedSerializer(serializers.Serializer):
    label = serializers.CharField()
    count = serializers.IntegerField()
    percentage_change = serializers.IntegerField()
    trend = serializers.ChoiceField(choices=["up", "down", "no_change"])