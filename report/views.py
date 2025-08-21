from __future__ import annotations
import io
import zipfile
from datetime import datetime
from typing import List, Dict

from django.http import HttpResponse
from django.db.models import Q
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from case.models import Case
from case.views import CaseAuthenticationMixin
from organization.models import Organization, Network
from .filters import build_date_filter_q
from .rendering import ReportRendererMixin

class BaseReportGeneratorMixin(ReportRendererMixin):
    """
    Common helpers for all report views.
    """

    # ---------- data assembly ---------- #

    def _standard_row(self, case: Case) -> Dict[str, str]:
        loan = getattr(case, "loan_details", None)

        adviser_name = (
            f"{case.created_by.first_name} {case.created_by.last_name}".strip()
            if case.created_by else "N/A"
        )

        mortgage_type = (
            loan.get_mortgage_type_display() if loan and loan.mortgage_type else "N/A"
        )

        ltv = f"{float(loan.ltv):.2f}%" if loan and loan.ltv is not None else "N/A"

        lender_name = (
            loan.get_lender_display() if loan and loan.lender else "N/A"
        )

        # Prefer the human-readable case name (e.g., ENQ-00000042)
        case_number = case.name or str(case.alias).upper()[:8]

        return {
            "case_number": case_number,
            "adviser_name": adviser_name,
            "mortgage_type": mortgage_type,
            "ltv": ltv,
            "current_stage": case.get_case_stage_display() if case.case_stage else "N/A",
            "lender_name": lender_name,
        }

    def _format_dt(self, dt_obj) -> str:
        if not dt_obj:
            return "N/A"
        local = timezone.localtime(dt_obj)
        return local.strftime("%d %b %Y, %H:%M")

    def _build_rows(self, cases, report_type: str) -> List[Dict[str, str]]:
        rows = []
        for c in cases:
            base = self._standard_row(c)

            if report_type == "submitted":
                base["extra_col"] = self._format_dt(c.submitted_date)
            elif report_type == "completed":
                base["extra_col"] = self._format_dt(c.completed_date)

            rows.append(base)
        return rows

    def _headers_for(self, report_type: str) -> List[Dict[str, str]]:
        headers = [
            {"key": "case_number", "label": "Case Number"},
            {"key": "adviser_name", "label": "Adviser Name"},
            {"key": "mortgage_type", "label": "Type of Mortgage/Insurance"},
            {"key": "ltv", "label": "LTV (%)"},
            {"key": "current_stage", "label": "Current Stage"},
            {"key": "lender_name", "label": "Lender Name"},
        ]
        if report_type == "submitted":
            headers.append({"key": "extra_col", "label": "Submission Date"})
        elif report_type == "completed":
            headers.append({"key": "extra_col", "label": "Completion Date"})
        return headers

    # ---------- shared apply filters ---------- #

    def _apply_common_filters(self, request, queryset):
        # Optional status/stage filters (kept from your previous version)
        case_status = request.GET.get("case_status")
        case_stage = request.GET.get("case_stage")

        if case_status:
            queryset = queryset.filter(case_status=case_status)
        if case_stage:
            queryset = queryset.filter(case_stage=case_stage)

        return queryset

    # ---------- main entry point ---------- #

    def _build_and_render(
        self,
        request,
        report_title: str,
        base_queryset,
        report_type: str,
        filename: str,
    ) -> HttpResponse:
        # The unified date filter
        q, date_label = build_date_filter_q(request.GET, report_type)
        qs = base_queryset.filter(q)
        qs = self._apply_common_filters(request, qs).select_related(
            "created_by", "loan_details", "organization", "network"
        )

        context = {
            "title": report_title,
            "date_label": date_label,
            "report_type": report_type,
            "generated_at": timezone.localtime().strftime("%d %b %Y, %H:%M"),
            "headers": self._headers_for(report_type),
            "rows": self._build_rows(qs, report_type),
        }
        return self.render_pdf(request, context, filename)


class NetworkReportView(CaseAuthenticationMixin, BaseReportGeneratorMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        assoc = self.get_user_association()
        if assoc["type"] != "network":
            return Response({"error": "Access denied. Network portal access required."}, status=403)

        network: Network = assoc["network"]

        cases = Case.objects.filter(Q(network=network) | Q(organization__network=network))
        report_type = request.GET.get("report_type", "standard").lower()

        title = f"Network Report — {network.name}"
        filename = f"network_report_{network.slug}"
        return self._build_and_render(request, title, cases, report_type, filename)


class OrganizationReportView(CaseAuthenticationMixin, BaseReportGeneratorMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        assoc = self.get_user_association()
        if assoc["type"] != "organization":
            return Response({"error": "Access denied. Organization portal access required."}, status=403)

        organization: Organization = assoc["organization"]

        cases = Case.objects.filter(organization=organization)
        report_type = request.GET.get("report_type", "standard").lower()

        title = f"Organization Report — {organization.name}"
        filename = f"organization_report_{organization.slug}"
        return self._build_and_render(request, title, cases, report_type, filename)


class AdviserReportView(CaseAuthenticationMixin, BaseReportGeneratorMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        cases = Case.objects.filter(created_by=request.user)
        report_type = request.GET.get("report_type", "standard").lower()

        adviser_name = f"{request.user.first_name} {request.user.last_name}".strip() or request.user.email
        title = f"Adviser Report — {adviser_name}"
        filename = f"adviser_report_{request.user.id}"
        return self._build_and_render(request, title, cases, report_type, filename)


class AdminReportView(BaseReportGeneratorMixin, APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not (request.user.is_staff or request.user.is_superuser):
            return Response({"error": "Access denied. Admin access required."}, status=403)

        cases = Case.objects.all()

        # Optional scoping
        network_id = request.GET.get("network_id")
        organization_id = request.GET.get("organization_id")
        if network_id:
            cases = cases.filter(Q(network_id=network_id) | Q(organization__network_id=network_id))
        if organization_id:
            cases = cases.filter(organization_id=organization_id)

        report_type = request.GET.get("report_type", "standard").lower()

        title = "Admin Report — All Cases"
        filename = "admin_report_all_cases"
        return self._build_and_render(request, title, cases, report_type, filename)


class BulkReportView(BaseReportGeneratorMixin, APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Request body example:
        {
          "reports": [
            {
              "type": "network" | "organization" | "adviser" | "admin",
              "report_type": "standard" | "submitted" | "completed",
              "filters": {
                  "date_filter": "today|this_week|this_month|this_year|range",
                  "from_date": "2025-08-01",
                  "to_date": "2025-08-22",
                  "month": "August",
                  "year": "2025",
                  "case_status": "NEW_LEAD",
                  "case_stage": "ENQUIRY",
                  "network_id": "...",
                  "organization_id": "..."
              }
            }
          ]
        }
        """
        configs = request.data.get("reports", [])
        if not configs:
            return Response({"error": "No report configurations provided"}, status=400)

        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for cfg in configs:
                scope_type = (cfg.get("type") or "").lower()
                report_type = (cfg.get("report_type") or "standard").lower()
                f = cfg.get("filters", {}) or {}

                # Base queryset by scope
                qs = Case.objects.all()
                if scope_type == "adviser":
                    qs = qs.filter(created_by=request.user)
                    title = f"Adviser Report — {request.user.get_full_name() or request.user.email}"
                    filename = f"adviser_report_{request.user.id}"
                elif scope_type == "organization":
                    org_id = f.get("organization_id")
                    if org_id:
                        qs = qs.filter(organization_id=org_id)
                    title = "Organization Report"
                    filename = f"organization_report_{timezone.now().strftime('%Y%m%d_%H%M%S')}"
                elif scope_type == "network":
                    net_id = f.get("network_id")
                    if net_id:
                        qs = qs.filter(Q(network_id=net_id) | Q(organization__network_id=net_id))
                    title = "Network Report"
                    filename = f"network_report_{timezone.now().strftime('%Y%m%d_%H%M%S')}"
                else:
                    # admin / default
                    if f.get("network_id"):
                        qs = qs.filter(Q(network_id=f["network_id"]) | Q(organization__network_id=f["network_id"]))
                    if f.get("organization_id"):
                        qs = qs.filter(organization_id=f["organization_id"])
                    title = "Admin Report — All Cases"
                    filename = f"admin_report_{timezone.now().strftime('%Y%m%d_%H%M%S')}"

                # Date Q + labels using the same engine, but with dict params
                q, date_label = build_date_filter_q(f, report_type)
                # Extra filters
                if f.get("case_status"):
                    qs = qs.filter(case_status=f["case_status"])
                if f.get("case_stage"):
                    qs = qs.filter(case_stage=f["case_stage"])

                qs = qs.filter(q).select_related("created_by", "loan_details", "organization", "network")

                context = {
                    "title": title,
                    "date_label": date_label,
                    "report_type": report_type,
                    "generated_at": timezone.localtime().strftime("%d %b %Y, %H:%M"),
                    "headers": self._headers_for(report_type),
                    "rows": self._build_rows(qs, report_type),
                }

                # Render one PDF per config and write into ZIP
                pdf_resp = self.render_pdf(request, context, filename)
                zf.writestr(f"{filename}.pdf", pdf_resp.content)

        resp = HttpResponse(content_type="application/zip")
        resp["Content-Disposition"] = f'attachment; filename="bulk_reports_{timezone.now().strftime("%Y%m%d_%H%M%S")}.zip"'  # noqa: E501
        resp.write(zip_buffer.getvalue())
        return resp
