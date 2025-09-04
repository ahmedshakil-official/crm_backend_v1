from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
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
    permission_classes = [IsAuthenticated]
    queryset = Case.objects.none()

    def get_meta_and_user_counts(self, request, user_association):
        """
        Returns meta and user_counts for either organization or network context.
        """
        if user_association["type"] == "organization":
            org = user_association["organization"]
            meta = {
                "type": "organization",
                "name": org.name,
                "slug": org.slug,
                "description": getattr(org, "description", ""),
                "email": org.email,
                "logo": request.build_absolute_uri(org.logo.url) if org.logo else None,
                "profile_image": request.build_absolute_uri(org.profile_image.url) if org.profile_image else None,
                "hero_image": request.build_absolute_uri(org.hero_image.url) if org.hero_image else None,
                "primary_mobile": org.primary_mobile,
                "other_contact": org.other_contact,
                "contact_person": org.contact_person,
                "website": org.website,
                "network": org.network.name if org.network else None,
            }
            org_users = OrganizationUser.objects.filter(organization=org)
            adviser_roles = [
                OrganizationRoleChoices.ADVISOR,
                OrganizationRoleChoices.ORGANIZATION_PRINCIPAL_ADVISER,
                OrganizationRoleChoices.ORGANIZATION_ADVISER,
            ]
            user_counts = {
                "total_advisers": org_users.filter(role__in=adviser_roles).count(),
                "total_clients": org_users.filter(role=OrganizationRoleChoices.CLIENT).count(),
                "total_leads": org_users.filter(role=OrganizationRoleChoices.LEAD).count(),
                "total_introducers": org_users.filter(role=OrganizationRoleChoices.INTRODUCER).count(),
                "adviser_user_ids": list(org_users.filter(role__in=adviser_roles).values_list('user_id', flat=True))
            }
        else:
            net = user_association["network"]
            meta = {
                "type": "network",
                "name": net.name,
                "slug": net.slug,
                "description": getattr(net, "description", ""),
                "email": net.email,
                "logo": request.build_absolute_uri(net.logo.url) if net.logo else None,
                "profile_image": request.build_absolute_uri(net.profile_image.url) if net.profile_image else None,
                "hero_image": request.build_absolute_uri(net.hero_image.url) if net.hero_image else None,
                "primary_mobile": net.primary_mobile,
                "other_contact": net.other_contact,
                "contact_person": net.contact_person,
                "website": net.website,
            }
            net_users = NetworkUser.objects.filter(network=net)
            adviser_roles = [
                NetworkRoleChoices.ADVISOR,
                NetworkRoleChoices.NETWORK_PRINCIPAL_ADVISER,
                NetworkRoleChoices.NETWORK_ADVISER,
            ]
            user_counts = {
                "total_advisers": net_users.filter(role__in=adviser_roles).count(),
                "total_clients": net_users.filter(role=NetworkRoleChoices.CLIENT).count(),
                "total_leads": net_users.filter(role=NetworkRoleChoices.LEAD).count(),
                "total_introducers": net_users.filter(role=NetworkRoleChoices.INTRODUCER).count(),
                "adviser_user_ids": list(net_users.filter(role__in=adviser_roles).values_list('user_id', flat=True))
            }
        return meta, user_counts

    def list(self, request, *args, **kwargs):
        user_association = self.get_user_association()
        meta, user_counts = self.get_meta_and_user_counts(request, user_association)
        cases = self.get_case_queryset()  # This will use org/network context and skip org cases for network!
        case_ids = list(cases.values_list('id', flat=True))
        total_cases = len(case_ids)

        # Count dictionaries (always include all choices)
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

        # Top Performing Advisers
        adviser_user_ids = user_counts.pop("adviser_user_ids", [])
        completed_cases = (
            cases.filter(case_stage=CaseStageChoices.COMPLETION)
            .exclude(assigned_to=None)
            .filter(assigned_to__in=adviser_user_ids)
            .values('assigned_to')
            .annotate(
                cases_completed=Count('id'),
                total_loan_amount=Sum('loan_details__loan_amount')
            )
            .order_by('-cases_completed')
        )
        adviser_users = User.objects.filter(id__in=[row['assigned_to'] for row in completed_cases])
        adviser_id_map = {user.id: user for user in adviser_users}
        top_advisers = []
        for i, stat in enumerate(completed_cases, start=1):
            adviser_id = stat['assigned_to']
            user = adviser_id_map.get(adviser_id)
            if not user:
                continue
            top_advisers.append({
                "rank": i,
                "full_name": f"{user.first_name} {user.last_name}".strip(),
                "profile_image": user.profile_image.url if user.profile_image else None,
                "cases_completed": stat['cases_completed'],
                "total_loan_amount": stat['total_loan_amount'] or 0,
            })

        user_counts['total_cases'] = total_cases

        data = {
            "meta": meta,
            "counters": user_counts,
            "category_counts": category_counts,
            "status_counts": status_counts,
            "stage_counts": stage_counts,
            "mortgage_type_counts": mortgage_type_counts,
            "lender_counts": lender_counts,
            "summary_cards": summary_cards,
            "top_performing_advisers": top_advisers,
        }
        return Response(data)



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
            "logo": request.build_absolute_uri(organization.logo.url) if organization.logo else None,
            "profile_image": request.build_absolute_uri(organization.profile_image.url) if organization.profile_image else None,
            "hero_image": request.build_absolute_uri(organization.hero_image.url) if organization.hero_image else None,
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


# Pagination class
class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

# This dashboard used for organisation user lead, client, and Cases Overview and adviser.
class OrganisationStatusView(ListAPIView):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    pagination_class = StandardResultsSetPagination

    #section
    def get_section(self):
        return (self.request.query_params.get("section", "people") or "").strip().lower()

    def get_filter_backends(self):
        return self.filter_backends if self.get_section() == "cases" else []

    #querysets
    def get_queryset(self):
        org_slug = self.kwargs["org_slug"]
        if self.get_section() == "cases":
            case_category = self.request.query_params.get("case_category")
            case_stage = self.request.query_params.get("case_stage")


            cases =  (
                Case.objects
                .select_related(
                    "lead", "assigned_to", "created_by", "updated_by",
                    "organization", "network"
                )
                .filter(organization__slug=org_slug)
                .order_by("-created_at")
            )

            filters = {}
            if case_category:
                filters["case_category"] = case_category
            if case_stage:
                filters["case_stage"] = case_stage

            cases = cases.filter(**filters)

            return cases
        return (
            OrganizationUser.objects
            .select_related("user", "created_by", "organization")
            .filter(organization__slug=org_slug)
            .order_by("-created_at")
        )

    #list
    def list(self, request, *args, **kwargs):
        if self.get_section() == "cases":
            qs = self.filter_queryset(self.get_queryset())  # apply CaseFilter
            page = self.paginate_queryset(qs)
            data = [self.case_row(c) for c in (page if page is not None else qs)]
            return self.get_paginated_response(data) if page is not None else Response(data)

        # people: no CaseFilter, no pagination
        qs = self.get_queryset()
        data = [self.client_leads_adviser_row(m) for m in qs]
        return Response(data)

    #helpers
    @staticmethod
    def get_iso_formate(data):
        if not data:
            return None
        s = data.isoformat()
        return s.replace("+00:00", "Z") if s.endswith("+00:00") else s

    @staticmethod
    def get_url(f):
        try:
            return f.url if f else None
        except Exception:
            return None

    @staticmethod
    def get_user_data(user: User):
        if not user:
            return None
        return {
            "id": user.id,
            "alias": str(getattr(user, "alias", "")),
            "email": user.email,
            "title": user.title,
            "first_name": user.first_name,
            "middle_name": getattr(user, "middle_name", ""),
            "last_name": user.last_name,
            "phone": user.phone,
            "user_type": user.user_type,
        }

    @staticmethod
    def get_org_data(org):
        if not org:
            return None
        return {
            "alias": str(getattr(org, "alias", "")),
            "email": org.email,
            "name": org.name,
            "logo": OrganisationStatusView.get_url(getattr(org, "logo", None)),
            "profile_image": OrganisationStatusView.get_url(getattr(org, "profile_image", None)),
            "hero_image": OrganisationStatusView.get_url(getattr(org, "hero_image", None)),
        }

    @staticmethod
    def get_network_data(data):
        if not data:
            return None
        return {
            "alias": str(getattr(data, "alias", "")),
            "slug": getattr(data, "slug", None),
            "name": getattr(data, "name", None),
            "email": getattr(data, "email", None),
            "logo": OrganisationStatusView.get_url(getattr(data, "logo", None)),
            "profile_image": OrganisationStatusView.get_url(getattr(data, "profile_image", None)),
            "hero_image": OrganisationStatusView.get_url(getattr(data, "hero_image", None)),
            "primary_mobile": getattr(data, "primary_mobile", None),
        }

    @staticmethod
    def get_to_basic_role(org_role_value: str) -> str:
        adviser_set = {
            OrganizationRoleChoices.ADVISOR,
            OrganizationRoleChoices.ORGANIZATION_ADVISER,
            OrganizationRoleChoices.ORGANIZATION_PRINCIPAL_ADVISER,
        }
        if org_role_value in adviser_set:
            return NetworkRoleChoices.ADVISOR
        if org_role_value == OrganizationRoleChoices.CLIENT:
            return NetworkRoleChoices.CLIENT
        return NetworkRoleChoices.LEAD

    def client_leads_adviser_row(self, organization_user: OrganizationUser):
        return {
            "alias": str(getattr(organization_user, "alias", organization_user.id)),
            "user": self.get_user_data(organization_user.user),
            "role": self.get_to_basic_role(organization_user.role),
            "dob": getattr(organization_user, "dob", None),
            "gender": getattr(organization_user, "gender", None),
            "created_by": self.get_user_data(organization_user.created_by),
            "created_at": self.get_iso_formate(organization_user.created_at),
        }

    def case_row(self, case: Case):
        return {
            "alias": str(getattr(case, "alias", case.id)),
            "name": case.name,
            "lead_user": self.get_user_data(case.lead),
            "assigned_user": self.get_user_data(case.assigned_to),
            "organization": self.get_org_data(case.organization),
            "network": self.get_network_data(case.network),
            "case_category": case.case_category,
            "case_stage": case.case_stage,
            "notes": case.notes or "",
            "is_removed": bool(case.is_removed),
            "created_by": self.get_user_data(case.created_by),
            "updated_by": self.get_user_data(case.updated_by),
            "created_at": self.get_iso_formate(case.created_at),
            "updated_at": self.get_iso_formate(case.updated_at),
        }