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
from common.enums import OrganizationRoleChoices, NetworkRoleChoices
from organization.models import OrganizationUser, Organization, NetworkUser


class OrganizationNetworkDashboardListView(CaseAuthenticationMixin, ListAPIView):
    """
    Dashboard API for both network and organization users.
    """
    permission_classes = [IsAuthenticated]
    queryset = Case.objects.none()

    def list(self, request, *args, **kwargs):
        # Get association info (no duplication)
        user_association = self.get_user_association()
        association_type = user_association["type"]
        association_instance = (
            user_association["organization"] if association_type == "organization"
            else user_association["network"]
        )

        # Meta and user role counters
        if association_type == "organization":
            meta = {
                "type": "organization",
                "name": association_instance.name,
                "slug": association_instance.slug,
                "description": getattr(association_instance, "description", ""),
                "email": association_instance.email,
                "logo": association_instance.logo.url if association_instance.logo else None,
                "profile_image": association_instance.profile_image.url if association_instance.profile_image else None,
                "hero_image": association_instance.hero_image.url if association_instance.hero_image else None,
                "primary_mobile": association_instance.primary_mobile,
                "other_contact": association_instance.other_contact,
                "contact_person": association_instance.contact_person,
                "website": association_instance.website,
                "network": association_instance.network.name if association_instance.network else None,
            }
            org_users = OrganizationUser.objects.filter(organization=association_instance)
            adviser_roles = [
                OrganizationRoleChoices.ADVISOR,
                OrganizationRoleChoices.ORGANIZATION_PRINCIPAL_ADVISER,
                OrganizationRoleChoices.ORGANIZATION_ADVISER,
            ]
            adviser_user_ids = list(org_users.filter(role__in=adviser_roles).values_list('user_id', flat=True))
            counters = {
                "total_advisers": len(adviser_user_ids),
                "total_clients": org_users.filter(role=OrganizationRoleChoices.CLIENT).count(),
                "total_leads": org_users.filter(role=OrganizationRoleChoices.LEAD).count(),
                "total_introducers": org_users.filter(role=OrganizationRoleChoices.INTRODUCER).count(),
            }
        else:
            meta = {
                "type": "network",
                "name": association_instance.name,
                "slug": association_instance.slug,
                "description": getattr(association_instance, "description", ""),
                "email": association_instance.email,
                "logo": association_instance.logo.url if association_instance.logo else None,
                "profile_image": association_instance.profile_image.url if association_instance.profile_image else None,
                "hero_image": association_instance.hero_image.url if association_instance.hero_image else None,
                "primary_mobile": association_instance.primary_mobile,
                "other_contact": association_instance.other_contact,
                "contact_person": association_instance.contact_person,
                "website": association_instance.website,
            }
            net_users = NetworkUser.objects.filter(network=association_instance)
            adviser_roles = [
                NetworkRoleChoices.ADVISOR,
                NetworkRoleChoices.NETWORK_PRINCIPAL_ADVISER,
                NetworkRoleChoices.NETWORK_ADVISER,
            ]
            adviser_user_ids = list(net_users.filter(role__in=adviser_roles).values_list('user_id', flat=True))
            counters = {
                "total_advisers": len(adviser_user_ids),
                "total_clients": net_users.filter(role=NetworkRoleChoices.CLIENT).count(),
                "total_leads": net_users.filter(role=NetworkRoleChoices.LEAD).count(),
                "total_introducers": net_users.filter(role=NetworkRoleChoices.INTRODUCER).count(),
            }

        # Use the unified, already-filtered cases
        cases = self.get_case_queryset()
        case_ids = list(cases.values_list('id', flat=True))
        total_cases = len(case_ids)
        counters["total_cases"] = total_cases

        # Pie and summary counts (always with all keys)
        def make_count_dict(qs, field, choices):
            result = {choice[0]: 0 for choice in choices}
            result.update({row[field]: row['count'] for row in qs.values(field).annotate(count=Count('id'))})
            return result

        category_counts = make_count_dict(cases, 'case_category', ProductCategoryChoices.choices)
        status_counts = make_count_dict(cases, 'case_status', CaseStatusChoices.choices)
        stage_counts = make_count_dict(cases, 'case_stage', CaseStageChoices.choices)

        loan_details = LoanDetails.objects.filter(case_id__in=case_ids)
        mortgage_type_counts = make_count_dict(loan_details, 'mortgage_type', MortgageTypeChoices.choices)
        mortgage_type_counts = {k: v for k, v in mortgage_type_counts.items() if k not in (None, '')}
        mortgage_type_counts = dict(sorted(mortgage_type_counts.items(), key=lambda item: item[1], reverse=True))

        lender_counts = make_count_dict(loan_details, 'lender', LenderChoices.choices)
        lender_counts = {k: v for k, v in lender_counts.items() if k not in (None, '')}
        lender_counts = dict(sorted(lender_counts.items(), key=lambda item: item[1], reverse=True))

        summary_cards = {
            "new_mortgage_enquiry": stage_counts.get(CaseStageChoices.ENQUIRY, 0),
            "mortgage_cases_submitted": category_counts.get(ProductCategoryChoices.MORTGAGE, 0),
            "mortgage_cases_completed": stage_counts.get(CaseStageChoices.COMPLETION, 0),
            "insurance_cases_submitted": category_counts.get(ProductCategoryChoices.GENERAL_INSURANCE, 0),
        }

        # Top Performing Advisers (by completed cases, sorted)
        completed_cases = (
            cases.filter(case_stage=CaseStageChoices.COMPLETION)
            .exclude(assigned_to=None)
            .values('assigned_to')
            .annotate(
                cases_completed=Count('id'),
                total_loan_amount=Sum('loan_details__loan_amount')
            )
            .order_by('-cases_completed')
        )
        adviser_ids_with_cases = [row['assigned_to'] for row in completed_cases if row['assigned_to'] in adviser_user_ids]
        adviser_users = User.objects.filter(id__in=adviser_ids_with_cases)
        adviser_id_map = {user.id: user for user in adviser_users}
        top_advisers = []
        for i, stat in enumerate(completed_cases, start=1):
            adviser_id = stat['assigned_to']
            if adviser_id not in adviser_id_map:
                continue
            user = adviser_id_map[adviser_id]
            top_advisers.append({
                "rank": i,
                "full_name": f"{user.first_name} {user.last_name}".strip(),
                "profile_image": user.profile_image.url if user.profile_image else None,
                "cases_completed": stat['cases_completed'],
                "total_loan_amount": stat['total_loan_amount'] or 0,
            })

        return Response({
            "meta": meta,
            "counters": counters,
            "category_counts": category_counts,
            "status_counts": status_counts,
            "stage_counts": stage_counts,
            "mortgage_type_counts": mortgage_type_counts,
            "lender_counts": lender_counts,
            "summary_cards": summary_cards,
            "top_performing_advisers": top_advisers,
        })



class OrganizationDashboardListView(ListAPIView):
    queryset = Organization.objects.none()  # Not used

    def list(self, request, *args, **kwargs):
        slug = self.kwargs.get("slug")
        organization = get_object_or_404(Organization, slug=slug)

        # Organization Details
        org_details = {
            "name": organization.name,
            "slug": organization.slug,
            "description": getattr(organization, "description", ""),
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
        adviser_roles = [
            OrganizationRoleChoices.ADVISOR,
            OrganizationRoleChoices.ORGANIZATION_PRINCIPAL_ADVISER,
            OrganizationRoleChoices.ORGANIZATION_ADVISER,
        ]
        adviser_count = org_users.filter(role__in=adviser_roles).count()
        client_count = org_users.filter(role=OrganizationRoleChoices.CLIENT).count()
        lead_count = org_users.filter(role=OrganizationRoleChoices.LEAD).count()
        introducer_count = org_users.filter(role=OrganizationRoleChoices.INTRODUCER).count()

        # Cases in organization
        cases = Case.objects.filter(organization=organization)
        case_ids = list(cases.values_list('id', flat=True))
        total_cases = cases.count()

        # All counts as in your network dashboard (always show all keys)
        # 1. Product Category Counts
        category_qs = cases.values('case_category').annotate(count=Count('id'))
        category_counts = {choice[0]: 0 for choice in ProductCategoryChoices.choices}
        category_counts.update({row['case_category']: row['count'] for row in category_qs})

        # 2. Case Status Counts
        status_qs = cases.values('case_status').annotate(count=Count('id'))
        status_counts = {choice[0]: 0 for choice in CaseStatusChoices.choices}
        status_counts.update({row['case_status']: row['count'] for row in status_qs})

        # 3. Case Stage Counts
        stage_qs = cases.values('case_stage').annotate(count=Count('id'))
        stage_counts = {choice[0]: 0 for choice in CaseStageChoices.choices}
        stage_counts.update({row['case_stage']: row['count'] for row in stage_qs})

        # 4. Mortgage Type Counts (Pie Chart)
        loan_details = LoanDetails.objects.filter(case_id__in=case_ids)
        mortgage_type_qs = loan_details.values('mortgage_type').annotate(count=Count('id'))
        mortgage_type_counts = {choice[0]: 0 for choice in MortgageTypeChoices.choices}
        mortgage_type_counts.update({row['mortgage_type']: row['count'] for row in mortgage_type_qs})
        # Remove null/empty, then sort descending
        mortgage_type_counts = {k: v for k, v in mortgage_type_counts.items() if k not in (None, '')}
        mortgage_type_counts = dict(sorted(mortgage_type_counts.items(), key=lambda item: item[1], reverse=True))

        # 5. Lender Counts (Pie Chart)
        lender_qs = loan_details.values('lender').annotate(count=Count('id'))
        lender_counts = {choice[0]: 0 for choice in LenderChoices.choices}
        lender_counts.update({row['lender']: row['count'] for row in lender_qs})
        lender_counts = {k: v for k, v in lender_counts.items() if k not in (None, '')}
        lender_counts = dict(sorted(lender_counts.items(), key=lambda item: item[1], reverse=True))

        # 6. Summary cards (as in your design)
        summary_cards = {
            "new_mortgage_enquiry": stage_counts.get(CaseStageChoices.ENQUIRY, 0),
            "mortgage_cases_submitted": category_counts.get(ProductCategoryChoices.MORTGAGE, 0),
            "mortgage_cases_completed": stage_counts.get(CaseStageChoices.COMPLETION, 0),
            "insurance_cases_submitted": category_counts.get(ProductCategoryChoices.GENERAL_INSURANCE, 0),
        }

        # 7. Top Performing Advisers (assigned_to, COMPLETION stage, sorted by case count)
        # Advisor user_ids (must be assigned_to and have correct org_user role)
        adviser_user_ids = set(
            org_users.filter(role__in=adviser_roles).values_list('user_id', flat=True)
        )
        completed_cases = (
            cases.filter(case_stage=CaseStageChoices.COMPLETION)
            .exclude(assigned_to=None)
            .values('assigned_to')
            .annotate(
                cases_completed=Count('id'),
                total_loan_amount=Sum('loan_details__loan_amount')
            )
            .order_by('-cases_completed')
        )
        # Map adviser ID to User
        adviser_ids_with_cases = [row['assigned_to'] for row in completed_cases if row['assigned_to'] in adviser_user_ids]
        adviser_users = User.objects.filter(id__in=adviser_ids_with_cases)
        adviser_id_map = {user.id: user for user in adviser_users}

        top_advisers = []
        for i, stat in enumerate(completed_cases, start=1):
            adviser_id = stat['assigned_to']
            if adviser_id not in adviser_id_map:
                continue
            user = adviser_id_map[adviser_id]
            top_advisers.append({
                "rank": i,
                "full_name": f"{user.first_name} {user.last_name}".strip(),
                "profile_image": user.profile_image.url if user.profile_image else None,
                "cases_completed": stat['cases_completed'],
                "total_loan_amount": stat['total_loan_amount'] or 0,
            })

        data = {
            "organization": org_details,
            "counters": {
                "total_advisers": adviser_count,
                "total_clients": client_count,
                "total_leads": lead_count,
                "total_introducers": introducer_count,
                "total_cases": total_cases,
            },
            "category_counts": category_counts,
            "status_counts": status_counts,
            "stage_counts": stage_counts,
            "mortgage_type_counts": mortgage_type_counts,
            "lender_counts": lender_counts,
            "summary_cards": summary_cards,
            "top_performing_advisers": top_advisers,
        }
        return Response(data)