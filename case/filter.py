from django_filters import rest_framework as filters

from common.enums import ProductCategoryChoices, ApplicantTypeChoices, CaseStatusChoices, CaseStageChoices
from .models import Case


class CaseFilter(filters.FilterSet):
    employee = filters.CharFilter(method="filter_by_employee", label="Employee")
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
            "employee",
            "case_category",
            "applicant_type",
            "case_status",
            "case_stage",
            "is_removed",
        ]

    def filter_by_employee(self, queryset, name, value):
        # Only filter by employees within the user's organization
        if self.request:
            organization = self.request.user.organization_users.first().organization
            return queryset.filter(created_by__email=value, organization=organization)
        return queryset.none()
