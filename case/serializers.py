from django.db import transaction
from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from common.enums import UserTypeChoices, RoleChoices
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
from organization.models import Organization, OrganizationUser
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
)
from authentication.models import User
from common.serializers import (
    CommonUserSerializer,
    CommonOrganizationSerializer,
    CommonUserWithPasswordSerializer,
    CommonCaseSerializer,
    CommonUserWithIdSerializer,
)


class CaseListCreateSerializer(serializers.ModelSerializer):
    organization = CommonOrganizationSerializer(read_only=True)
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
            "case_category",
            # "applicant_type",
            # "case_status",
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
            "created_by",
            "is_removed",
            "updated_by",
            "created_at",
            "updated_at",
        ]
        write_only_fields = ["lead"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically adjust the queryset for the 'lead' field based on the organization of the current user
        organization = Organization.objects.filter(
            organization_users__user=self.context["request"].user
        ).first()
        if organization:
            # Only allow users who are Leads and belong to the same organization as the current user

            self.fields["lead"].queryset = User.objects.filter(
                user_type="LEAD", organization_users__organization=organization
            )


class CaseRetrieveUpdateDeleteSerializer(serializers.ModelSerializer):
    organization = CommonOrganizationSerializer(read_only=True)
    lead_user = CommonUserWithIdSerializer(read_only=True, source="lead")
    created_by = CommonUserSerializer(read_only=True)
    updated_by = CommonUserSerializer(read_only=True)

    class Meta:
        model = Case
        fields = [
            "alias",
            "name",
            "lead_user",
            "organization",
            "case_category",
            # "applicant_type",
            # "case_status",
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
            "created_by",
            "is_removed",
            "updated_by",
            "created_at",
            "updated_at",
        ]


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
            role=RoleChoices.JOINT_USER,
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
        instance.disclaimer_details = validated_data.get("disclaimer_details", instance.disclaimer_details)
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

