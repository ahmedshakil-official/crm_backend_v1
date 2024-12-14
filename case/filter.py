import datetime

from django.db.models import Q
from django.utils import timezone
from django_filters import rest_framework as filters

from authentication.models import User
from common.enums import (
    ProductCategoryChoices,
    ApplicantTypeChoices,
    CaseStatusChoices,
    CaseStageChoices,
    RoleChoices,
    FileTypeChoices,
)
from .models import Case, Files


class CaseFilter(filters.FilterSet):
    created_by = filters.ModelChoiceFilter(
        queryset=User.objects.none(),
        label="Employee",
    )
    case_category = filters.ChoiceFilter(
        choices=ProductCategoryChoices.choices, field_name="case_category"
    )
    applicant_type = filters.ChoiceFilter(
        choices=ApplicantTypeChoices.choices, field_name="applicant_type"
    )
    case_status = filters.ChoiceFilter(
        choices=CaseStatusChoices.choices, field_name="case_status"
    )
    case_stage = filters.ChoiceFilter(
        choices=CaseStageChoices.choices, field_name="case_stage"
    )
    is_removed = filters.BooleanFilter(field_name="is_removed")

    class Meta:
        model = Case
        fields = [
            "created_by",
            "case_category",
            "applicant_type",
            "case_status",
            "case_stage",
            "is_removed",
        ]

    def __init__(self, *args, **kwargs):
        # Call the superclass initializer
        super().__init__(*args, **kwargs)
        # Dynamically set the queryset for the created_by field
        if hasattr(self, "request") and self.request is not None:
            organization = self.request.user.organization_users.first().organization
            # Filter Users based on the Organization and Role
            self.filters["created_by"].queryset = User.objects.filter(
                organization_users__organization=organization,
                organization_users__role=RoleChoices.ADVISOR,
            )


class FileFilter(filters.FilterSet):
    created_by = filters.ModelChoiceFilter(
        queryset=User.objects.none(),  # Dynamically set based on request
        label="Created By (Advisor)",
    )
    file_type = filters.ChoiceFilter(
        choices=FileTypeChoices,
        label="File Type",
    )
    file_owner = filters.ModelChoiceFilter(
        queryset=User.objects.none(),  # Dynamically set based on the case
        label="File Owner",
    )
    created_at = filters.DateFromToRangeFilter(label="Created Date Range")

    class Meta:
        model = Files
        fields = ["created_by", "file_type", "file_owner", "created_at"]

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)

        if self.request:
            # Limit `created_by` to advisors in the user's organization
            user_organization = self.request.user.organization
            self.filters["created_by"].queryset = User.objects.filter(
                organization=user_organization, role="advisor"
            )

            # Limit `file_owner` to valid owners based on the provided case
            case = kwargs.get("alias", None)
            print("=" * 20)
            print(case)
            print("=" * 20)
            if case:
                lead = case.lead
                joint_users = case.joint_users.values_list("joint_user", flat=True)
                self.filters["file_owner"].queryset = User.objects.filter(
                    pk__in=[lead.pk, *joint_users]
                )
