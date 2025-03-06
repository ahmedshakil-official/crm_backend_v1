from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from common.enums import UserTypeChoices, RoleChoices
from organization.models import Organization, OrganizationUser
from .common import RegisterLoan, PaymentCommitment, PropertyRepossessed, Bankrupt
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
    lead_user = CommonUserSerializer(read_only=True, source="lead")
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
    lead_user = CommonUserSerializer(read_only=True, source="lead")
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
    joint_user_details = CommonUserSerializer(read_only=True, source="joint_user")
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
    created_at = CommonUserWithIdSerializer(read_only=True)
    updated_at = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = RegisterLoan
        fields =[
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
            "user_ip",
        ]
        read_only_fields = [
            "alias",
            "adverse",
            "created_at",
            "updated_at",
            "created_by",
            "updated_by",
            "user_ip",
        ]


