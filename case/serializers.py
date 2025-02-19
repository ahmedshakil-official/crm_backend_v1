from django_countries.serializer_fields import CountryField
from rest_framework import serializers

from common.enums import UserTypeChoices, RoleChoices
from organization.models import Organization, OrganizationUser
from .models import (
    Case,
    Files,
    JointUser,
    LoanDetails,
    ApplicantDetails,
    CompanyInfo,
    Dependant,
    DirectorShareholder,
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
            "applicant_type",
            "case_status",
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
            "applicant_type",
            "case_status",
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


class ApplicantDetailsSerializer(serializers.ModelSerializer):
    company = CompanyInfoSerializer(read_only=True)
    nationality = CountryField(required=False, allow_blank=True, allow_null=True)
    applicant = CommonUserWithIdSerializer(read_only=True)

    class Meta:
        model = ApplicantDetails
        fields = [
            "alias",
            "case",
            "is_company_application",
            "company",
            "applicant",
            "title",
            "maiden_name",
            "date_of_birth",
            "anticipated_retirement_age",
            "state_retirement_age",
            "is_smoker",
            "gender",
            "nationality",
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
            "company",
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
            "applicant_details",
            "name",
            "date_of_birth",
        ]


class DirectorShareholderSerializer(serializers.ModelSerializer):
    class Meta:
        model = DirectorShareholder
        fields = [
            "company",
            "full_name",
            "percentage_share",
            "role",
        ]
