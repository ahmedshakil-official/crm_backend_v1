from django_filters import rest_framework as filters

from authentication.models import User
from common.enums import ProductCategoryChoices, ApplicantTypeChoices, CaseStatusChoices, CaseStageChoices, RoleChoices
from .models import Case


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
        if hasattr(self, 'request') and self.request is not None:
            organization = (
                self.request.user.organization_users.first().organization
            )
            # Filter Users based on the Organization and Role
            self.filters['created_by'].queryset = User.objects.filter(
                organization_users__organization=organization,
                organization_users__role=RoleChoices.ADVISOR,
            )

