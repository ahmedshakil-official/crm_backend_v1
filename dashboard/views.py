from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Count, Q, Sum

from authentication.models import User
from case.models import (
    Case, LoanDetails, ProductCategoryChoices, CaseStatusChoices, CaseStageChoices,
    MortgageTypeChoices, LenderChoices
)
from case.views import CaseAuthenticationMixin
from common.enums import OrganizationRoleChoices
from organization.models import OrganizationUser, Organization


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



class OrganizationDashboardListView(ListAPIView):
    queryset = Organization.objects.none()

    def list(self, request, *args, **kwargs):
        slug = self.kwargs.get("slug")
        organization = get_object_or_404(Organization, slug=slug)

        # Organization Details
        org_details = {
            "name": organization.name,
            "slug": organization.slug,
            "description": organization.description,
            "email": organization.email,
            "logo": organization.logo.url if organization.logo else None,
            "profile_image": organization.profile_image.url if organization.profile_image else None,
            "hero_image": organization.hero_image.url if organization.hero_image else None,
            "primary_mobile": organization.primary_mobile,
            "other_contact": organization.other_contact,
            "contact_person": organization.contact_person,
            "website": organization.website,
            "network": organization.network.name if organization.network else None,
        }

        # OrganizationUser role counts
        org_users = OrganizationUser.objects.filter(organization=organization)
        adviser_count = org_users.filter(
            role__in=[
                OrganizationRoleChoices.ADVISOR,
                OrganizationRoleChoices.ORGANIZATION_PRINCIPAL_ADVISER,
                OrganizationRoleChoices.ORGANIZATION_ADVISER,
            ]
        ).count()
        client_count = org_users.filter(role=OrganizationRoleChoices.CLIENT).count()
        lead_count = org_users.filter(role=OrganizationRoleChoices.LEAD).count()
        introducer_count = org_users.filter(role=OrganizationRoleChoices.INTRODUCER).count()

        # Cases in organization
        cases = Case.objects.filter(organization=organization)

        # Top Performing Advisers: assigned_to, case_status=COMPLETION, case count, total amount
        # 1. All adviser users
        adviser_user_ids = list(
            org_users.filter(
                role__in=[
                    OrganizationRoleChoices.ADVISOR,
                    OrganizationRoleChoices.ORGANIZATION_PRINCIPAL_ADVISER,
                    OrganizationRoleChoices.ORGANIZATION_ADVISER,
                ]
            ).values_list('user_id', flat=True)
        )
        # 2. Count cases completed for each adviser and sum total loan_amount (if LoanDetails exists)
        advisers_stats = (
            Case.objects
            .filter(organization=organization, assigned_to_id__in=adviser_user_ids, case_status=CaseStageChoices.COMPLETION)
            .values('assigned_to')
            .annotate(
                num_cases=Count('id'),
                total_loan_amount=Sum('loan_details__loan_amount')
            )
            .order_by('-num_cases')
        )
        # 3. Get adviser details
        adviser_users = User.objects.filter(id__in=[a['assigned_to'] for a in advisers_stats])
        adviser_id_map = {user.id: user for user in adviser_users}
        top_advisers = []
        for i, stat in enumerate(advisers_stats, start=1):
            user = adviser_id_map[stat['assigned_to']]
            top_advisers.append({
                "rank": i,
                "full_name": f"{user.first_name} {user.last_name}".strip(),
                "profile_image": user.profile_image.url if user.profile_image else None,
                "cases_completed": stat['num_cases'],
                "total_loan_amount": stat['total_loan_amount'] or 0,
            })

        data = {
            "organization": org_details,
            "counters": {
                "total_advisers": adviser_count,
                "total_clients": client_count,
                "total_leads": lead_count,
                "total_introducers": introducer_count,
            },
            "top_performing_advisers": top_advisers,
        }
        return Response(data)