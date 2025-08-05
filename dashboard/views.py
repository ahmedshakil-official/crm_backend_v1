from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count

from case.models import (
    Case, LoanDetails, ProductCategoryChoices, CaseStatusChoices, CaseStageChoices,
    MortgageTypeChoices, LenderChoices
)
from case.views import CaseAuthenticationMixin

class OrganizationNetworkDashboardListView(CaseAuthenticationMixin, ListAPIView):
    """
    Dashboard API for both network and organization users.
    Returns summary and pie chart data for associated cases and loan details.
    """
    permission_classes = [IsAuthenticated]
    queryset = Case.objects.none()  # Not directly returning objects

    def list(self, request, *args, **kwargs):
        user_association = self.get_user_association()
        cases = self.get_case_queryset()
        case_ids = list(cases.values_list('id', flat=True))
        total_cases = len(case_ids)

        category_qs = cases.values('case_category').annotate(count=Count('id'))
        category_counts = {choice[0]: 0 for choice in ProductCategoryChoices.choices}
        category_counts.update({row['case_category']: row['count'] for row in category_qs})

        # Case Status Counts
        status_qs = cases.values('case_status').annotate(count=Count('id'))
        status_counts = {choice[0]: 0 for choice in CaseStatusChoices.choices}
        status_counts.update({row['case_status']: row['count'] for row in status_qs})

        # Case Stage Counts
        stage_qs = cases.values('case_stage').annotate(count=Count('id'))
        stage_counts = {choice[0]: 0 for choice in CaseStageChoices.choices}
        stage_counts.update({row['case_stage']: row['count'] for row in stage_qs})

        # LoanDetails queries (for pie charts)
        loan_details = LoanDetails.objects.filter(case_id__in=case_ids)

        # Mortgage Type Counts
        mortgage_type_qs = loan_details.values('mortgage_type').annotate(count=Count('id'))
        mortgage_type_counts = {choice[0]: 0 for choice in MortgageTypeChoices.choices}
        mortgage_type_counts.update({row['mortgage_type']: row['count'] for row in mortgage_type_qs})
        # mortgage_type_counts['NOT_FILLED'] = total_cases - loan_details.count()
        mortgage_type_counts = {k: v for k, v in mortgage_type_counts.items() if k not in (None, '')}
        mortgage_type_counts = dict(sorted(mortgage_type_counts.items(), key=lambda item: item[1], reverse=True))

        # Lender Counts
        lender_qs = loan_details.values('lender').annotate(count=Count('id'))
        lender_counts = {choice[0]: 0 for choice in LenderChoices.choices}
        lender_counts.update({row['lender']: row['count'] for row in lender_qs})
        # lender_counts['NOT_FILLED'] = total_cases - loan_details.count()
        lender_counts = {k: v for k, v in lender_counts.items() if k not in (None, '')}
        lender_counts = dict(sorted(lender_counts.items(), key=lambda item: item[1], reverse=True))

        # Summary cards
        data = {
            "total_cases": total_cases,
            "category_counts": category_counts,
            "status_counts": status_counts,
            "stage_counts": stage_counts,
            "mortgage_type_counts": mortgage_type_counts,
            "lender_counts": lender_counts,
            "summary_cards": {
                "new_mortgage_enquiry": stage_counts.get(CaseStageChoices.ENQUIRY, 0),
                "mortgage_cases_submitted": category_counts.get(ProductCategoryChoices.MORTGAGE, 0),
                "mortgage_cases_completed": stage_counts.get(CaseStageChoices.COMPLETION, 0),
                "insurance_cases_submitted": category_counts.get(ProductCategoryChoices.GENERAL_INSURANCE, 0),
            }
        }
        return Response(data)
