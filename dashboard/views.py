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
    queryset = Organization.objects.none()
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        org_slug = kwargs["org_slug"]
        section_raw = request.query_params.get("section")
        section = (section_raw.strip().lower() if section_raw and section_raw.strip() else "people")
        org_user = (kwargs.get("org_user") or "").lower()

        role_map = {
            "leads": [OrganizationRoleChoices.LEAD],
            "clients": [OrganizationRoleChoices.CLIENT],
            "advisers": [
                OrganizationRoleChoices.ADVISOR,
                OrganizationRoleChoices.ORGANIZATION_ADVISER,
                OrganizationRoleChoices.ORGANIZATION_PRINCIPAL_ADVISER,
            ],
        }
        if org_user not in role_map:
            return Response({"detail": "use one of: leads | clients | advisers"}, status=400)

        if section == "cases":
            case_category = request.query_params.get("case_category")
            case_stage = request.query_params.get("case_stage")

            qs = (
                Case.objects
                .select_related("lead", "assigned_to", "created_by", "updated_by", "organization", "network")
                .filter(organization__slug=org_slug)
                .order_by("-created_at")
            )
            if case_category:
                qs = qs.filter(case_category=case_category)
            if case_stage:
                qs = qs.filter(case_stage=case_stage)

            page = self.paginate_queryset(qs)
            items = page if page is not None else qs
            data = []
            for case in items:
                lead_user = None
                if case.lead:
                    lead_user = {
                        "id": case.lead.id,
                        "alias": str(getattr(case.lead, "alias", "")),
                        "email": case.lead.email,
                        "title": case.lead.title,
                        "first_name": case.lead.first_name,
                        "middle_name": getattr(case.lead, "middle_name", ""),
                        "last_name": case.lead.last_name,
                        "phone": case.lead.phone,
                        "user_type": case.lead.user_type,
                    }

                assigned_user = None
                if case.assigned_to:
                    assigned_user = {
                        "id": case.assigned_to.id,
                        "alias": str(getattr(case.assigned_to, "alias", "")),
                        "email": case.assigned_to.email,
                        "title": case.assigned_to.title,
                        "first_name": case.assigned_to.first_name,
                        "middle_name": getattr(case.assigned_to, "middle_name", ""),
                        "last_name": case.assigned_to.last_name,
                        "phone": case.assigned_to.phone,
                        "user_type": case.assigned_to.user_type,
                    }

                created_by = None
                if case.created_by:
                    created_by = {
                        "id": case.created_by.id,
                        "alias": str(getattr(case.created_by, "alias", "")),
                        "email": case.created_by.email,
                        "title": case.created_by.title,
                        "first_name": case.created_by.first_name,
                        "middle_name": getattr(case.created_by, "middle_name", ""),
                        "last_name": case.created_by.last_name,
                        "phone": case.created_by.phone,
                        "user_type": case.created_by.user_type,
                    }

                updated_by = None
                if case.updated_by:
                    updated_by = {
                        "id": case.updated_by.id,
                        "alias": str(getattr(case.updated_by, "alias", "")),
                        "email": case.updated_by.email,
                        "title": case.updated_by.title,
                        "first_name": case.updated_by.first_name,
                        "middle_name": getattr(case.updated_by, "middle_name", ""),
                        "last_name": case.updated_by.last_name,
                        "phone": case.updated_by.phone,
                        "user_type": case.updated_by.user_type,
                    }

                org_obj = None
                if case.organization:
                    org_obj = {
                        "alias": str(getattr(case.organization, "alias", "")),
                        "email": case.organization.email,
                        "name": case.organization.name,
                        "logo": request.build_absolute_uri(case.organization.logo.url) if getattr(case.organization, "logo", None) else None,
                        "profile_image": request.build_absolute_uri(case.organization.profile_image.url) if getattr(case.organization, "profile_image", None) else None,
                        "hero_image": request.build_absolute_uri(case.organization.hero_image.url) if getattr(case.organization, "hero_image", None) else None,
                    }

                network_obj = None
                if case.network:
                    network_obj = {
                        "alias": str(getattr(case.network, "alias", "")),
                        "slug": getattr(case.network, "slug", None),
                        "name": getattr(case.network, "name", None),
                        "email": getattr(case.network, "email", None),
                        "logo": request.build_absolute_uri(case.network.logo.url) if getattr(case.network, "logo", None) else None,
                        "profile_image": request.build_absolute_uri(case.network.profile_image.url) if getattr(case.network, "profile_image", None) else None,
                        "hero_image": request.build_absolute_uri(case.network.hero_image.url) if getattr(case.network, "hero_image", None) else None,
                        "primary_mobile": getattr(case.network, "primary_mobile", None),
                    }

                data.append({
                    "alias": str(getattr(case, "alias", case.id)),
                    "name": case.name,
                    "lead_user": lead_user,
                    "assigned_user": assigned_user,
                    "organization": org_obj,
                    "network": network_obj,
                    "case_category": case.case_category,
                    "case_stage": case.case_stage,
                    "notes": case.notes or "",
                    "is_removed": bool(case.is_removed),
                    "created_by": created_by,
                    "updated_by": updated_by,
                    "created_at": case.created_at.isoformat().replace("+00:00", "Z") if case.created_at else None,
                    "updated_at": case.updated_at.isoformat().replace("+00:00", "Z") if case.updated_at else None,
                })

            return self.get_paginated_response(data) if page is not None else Response(data)

        # people section
        queryset = (
            OrganizationUser.objects
            .select_related("user", "created_by", "organization")
            .filter(organization__slug=org_slug, role__in=role_map[org_user])
            .order_by("-created_at")
        )

        data = []
        for organization_user in queryset:
            if organization_user.role in {
                OrganizationRoleChoices.ADVISOR,
                OrganizationRoleChoices.ORGANIZATION_ADVISER,
                OrganizationRoleChoices.ORGANIZATION_PRINCIPAL_ADVISER,
            }:
                basic_role = NetworkRoleChoices.ADVISOR
            elif organization_user.role == OrganizationRoleChoices.CLIENT:
                basic_role = NetworkRoleChoices.CLIENT
            else:
                basic_role = NetworkRoleChoices.LEAD

            user = organization_user.user
            created_by_user = organization_user.created_by

            data.append({
                "alias": str(getattr(organization_user, "alias", organization_user.id)),
                "user": {
                    "id": user.id,
                    "alias": str(getattr(user, "alias", "")),
                    "email": user.email,
                    "title": user.title,
                    "first_name": user.first_name,
                    "middle_name": getattr(user, "middle_name", ""),
                    "last_name": user.last_name,
                    "phone": user.phone,
                    "user_type": user.user_type,
                } if user else None,
                "role": basic_role,
                "organization_slug": (
                    organization_user.organization.slug if organization_user.organization_id else org_slug
                ),
                "dob": organization_user.dob.isoformat() if getattr(organization_user, "dob", None) else None,
                "gender": getattr(organization_user, "gender", None),
                "created_by": {
                    "id": created_by_user.id,
                    "alias": str(getattr(created_by_user, "alias", "")),
                    "email": created_by_user.email,
                    "title": created_by_user.title,
                    "first_name": created_by_user.first_name,
                    "middle_name": getattr(created_by_user, "middle_name", ""),
                    "last_name": created_by_user.last_name,
                    "phone": created_by_user.phone,
                    "user_type": created_by_user.user_type,
                } if created_by_user else None,
                "created_at": organization_user.created_at.isoformat().replace("+00:00", "Z") if organization_user.created_at else None,
            })

        return Response(data)