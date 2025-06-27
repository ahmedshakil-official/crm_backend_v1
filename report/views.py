import io
import zipfile
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT

from case.models import Case
from case.views import CaseAuthenticationMixin
from organization.models import Organization, Network, OrganizationUser, NetworkUser


class BaseReportGeneratorMixin:
    """Base mixin for report generation functionality"""

    def get_standard_fields_data(self, case):
        """Get standard fields that appear in all reports"""
        loan_details = getattr(case, "loan_details", None)

        # Get adviser name (case creator)
        adviser_name = (
            f"{case.created_by.first_name} {case.created_by.last_name}"
            if case.created_by
            else "N/A"
        )

        # Get mortgage/insurance type
        mortgage_type = "N/A"
        if loan_details and loan_details.mortgage_type:
            mortgage_type = loan_details.get_mortgage_type_display()

        # Get LTV
        ltv = "N/A"
        if loan_details and loan_details.ltv:
            ltv = f"{loan_details.ltv:.2f}%"

        # Get lender name
        lender_name = "N/A"
        if loan_details and loan_details.lender:
            lender_name = loan_details.lender

        return {
            "case_number": str(case.alias)[:8].upper(),
            "adviser_name": adviser_name,
            "mortgage_type": mortgage_type,
            "ltv": ltv,
            "current_stage": (
                case.get_case_stage_display() if case.case_stage else "N/A"
            ),
            "lender_name": lender_name,
            "report_generation_date": datetime.now().strftime("%d/%m/%Y at %H:%M"),
        }

    def create_pdf_report(self, cases, report_title, additional_columns=None):
        """Create PDF report for given cases"""
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18,
        )
        elements = []

        # Define styles
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            "CustomTitle",
            parent=styles["Heading1"],
            fontSize=18,
            spaceAfter=30,
            alignment=TA_CENTER,
        )

        # Add title
        title = Paragraph(report_title, title_style)
        elements.append(title)
        elements.append(Spacer(1, 12))

        # Create table headers
        headers = [
            "Case Number",
            "Adviser Name",
            "Type of Mortgage/Insurance",
            "LTV (%)",
            "Current Stage",
            "Lender Name",
        ]

        # Add additional columns if specified
        if additional_columns:
            headers.extend(additional_columns)

        # Create data rows
        data = [headers]

        for case in cases:
            standard_data = self.get_standard_fields_data(case)
            row = [
                standard_data["case_number"],
                standard_data["adviser_name"],
                standard_data["mortgage_type"],
                standard_data["ltv"],
                standard_data["current_stage"],
                standard_data["lender_name"],
            ]

            # Add additional column data if specified
            if additional_columns:
                for col in additional_columns:
                    if col == "Submission Date":
                        row.append(
                            case.created_at.strftime("%d/%m/%Y")
                            if case.created_at
                            else "N/A"
                        )
                    elif col == "Completion Date":
                        # You would need to add completion date logic based on your case stages
                        row.append("N/A")  # Placeholder
                    else:
                        row.append("N/A")

            data.append(row)

        # Create table
        table = Table(data, colWidths=[1.2 * inch] * len(headers))
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "LEFT"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (0, 0), (-1, 0), 10),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("FONTSIZE", (0, 1), (-1, -1), 8),
                ]
            )
        )

        elements.append(table)
        elements.append(Spacer(1, 20))

        # Add footer with generation date
        footer_text = (
            f"Report generated on: {datetime.now().strftime('%d %B %Y, %H:%M')}"
        )
        footer = Paragraph(footer_text, styles["Normal"])
        elements.append(footer)

        # Build PDF
        doc.build(elements)

        pdf_content = buffer.getvalue()
        buffer.close()

        return pdf_content


class NetworkReportView(CaseAuthenticationMixin, BaseReportGeneratorMixin, APIView):
    """Generate reports for Network portal users"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_association = self.get_user_association()

        # Check if user has network access
        if user_association["type"] != "network":
            return Response(
                {"error": "Access denied. Network portal access required."}, status=403
            )

        network = user_association["network"]

        # Get all cases within the network (all organizations under this network)
        cases = Case.objects.filter(
            Q(network=network) | Q(organization__network=network)
        ).select_related("created_by", "loan_details", "organization", "network")

        # Apply filters
        cases = self.apply_filters(request, cases)

        # Generate report
        report_title = f"Network Report - {network.name}"
        pdf_content = self.create_pdf_report(
            cases, report_title, self.get_additional_columns(request)
        )

        # Return response
        return self.create_pdf_response(pdf_content, f"network_report_{network.slug}")

    def apply_filters(self, request, queryset):
        """Apply filters based on request parameters"""
        # Date range filter
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        # Case status filter
        case_status = request.GET.get("case_status")
        if case_status:
            queryset = queryset.filter(case_status=case_status)

        # Case stage filter
        case_stage = request.GET.get("case_stage")
        if case_stage:
            queryset = queryset.filter(case_stage=case_stage)

        return queryset

    def get_additional_columns(self, request):
        """Get additional columns based on report type"""
        report_type = request.GET.get("report_type", "standard")

        if report_type == "submitted":
            return ["Submission Date"]
        elif report_type == "completed":
            return ["Completion Date"]

        return None

    def create_pdf_response(self, pdf_content, filename):
        """Create HTTP response with PDF content"""
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}.pdf"'
        response.write(pdf_content)
        return response


class OrganizationReportView(
    CaseAuthenticationMixin, BaseReportGeneratorMixin, APIView
):
    """Generate reports for Organization portal users"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_association = self.get_user_association()

        # Check if user has organization access
        if user_association["type"] != "organization":
            return Response(
                {"error": "Access denied. Organization portal access required."},
                status=403,
            )

        organization = user_association["organization"]

        # Get all cases for this organization and its advisers
        cases = Case.objects.filter(organization=organization).select_related(
            "created_by", "loan_details", "organization"
        )

        # Apply filters
        cases = self.apply_filters(request, cases)

        # Generate report
        report_title = f"Organization Report - {organization.name}"
        pdf_content = self.create_pdf_report(
            cases, report_title, self.get_additional_columns(request)
        )

        # Return response
        return self.create_pdf_response(
            pdf_content, f"organization_report_{organization.slug}"
        )

    def apply_filters(self, request, queryset):
        """Apply filters based on request parameters"""
        # Date range filter
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        # Case status filter
        case_status = request.GET.get("case_status")
        if case_status:
            queryset = queryset.filter(case_status=case_status)

        # Case stage filter
        case_stage = request.GET.get("case_stage")
        if case_stage:
            queryset = queryset.filter(case_stage=case_stage)

        return queryset

    def get_additional_columns(self, request):
        """Get additional columns based on report type"""
        report_type = request.GET.get("report_type", "standard")

        if report_type == "submitted":
            return ["Submission Date"]
        elif report_type == "completed":
            return ["Completion Date"]

        return None

    def create_pdf_response(self, pdf_content, filename):
        """Create HTTP response with PDF content"""
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}.pdf"'
        response.write(pdf_content)
        return response


class AdviserReportView(CaseAuthenticationMixin, BaseReportGeneratorMixin, APIView):
    """Generate reports for Adviser portal users"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get cases only for the current user (adviser)
        cases = Case.objects.filter(created_by=request.user).select_related(
            "created_by", "loan_details", "organization"
        )

        # Apply filters
        cases = self.apply_filters(request, cases)

        # Generate report
        adviser_name = f"{request.user.first_name} {request.user.last_name}"
        report_title = f"Adviser Report - {adviser_name}"
        pdf_content = self.create_pdf_report(
            cases, report_title, self.get_additional_columns(request)
        )

        # Return response
        return self.create_pdf_response(
            pdf_content, f"adviser_report_{request.user.id}"
        )

    def apply_filters(self, request, queryset):
        """Apply filters based on request parameters"""
        # Date range filter
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        # Case status filter
        case_status = request.GET.get("case_status")
        if case_status:
            queryset = queryset.filter(case_status=case_status)

        # Case stage filter
        case_stage = request.GET.get("case_stage")
        if case_stage:
            queryset = queryset.filter(case_stage=case_stage)

        return queryset

    def get_additional_columns(self, request):
        """Get additional columns based on report type"""
        report_type = request.GET.get("report_type", "standard")

        if report_type == "submitted":
            return ["Submission Date"]
        elif report_type == "completed":
            return ["Completion Date"]

        return None

    def create_pdf_response(self, pdf_content, filename):
        """Create HTTP response with PDF content"""
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}.pdf"'
        response.write(pdf_content)
        return response


class AdminReportView(BaseReportGeneratorMixin, APIView):
    """Generate reports for Admin portal users"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Check if user is admin/staff
        if not (request.user.is_staff or request.user.is_superuser):
            return Response(
                {"error": "Access denied. Admin access required."}, status=403
            )

        # Get all cases across all users and portals
        cases = Case.objects.all().select_related(
            "created_by", "loan_details", "organization", "network"
        )

        # Apply filters
        cases = self.apply_filters(request, cases)

        # Generate report
        report_title = "Admin Report - All Cases"
        pdf_content = self.create_pdf_report(
            cases, report_title, self.get_additional_columns(request)
        )

        # Return response
        return self.create_pdf_response(pdf_content, "admin_report_all_cases")

    def apply_filters(self, request, queryset):
        """Apply filters based on request parameters"""
        # Date range filter
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")

        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        # Case status filter
        case_status = request.GET.get("case_status")
        if case_status:
            queryset = queryset.filter(case_status=case_status)

        # Case stage filter
        case_stage = request.GET.get("case_stage")
        if case_stage:
            queryset = queryset.filter(case_stage=case_stage)

        # Network filter
        network_id = request.GET.get("network_id")
        if network_id:
            queryset = queryset.filter(
                Q(network_id=network_id) | Q(organization__network_id=network_id)
            )

        # Organization filter
        organization_id = request.GET.get("organization_id")
        if organization_id:
            queryset = queryset.filter(organization_id=organization_id)

        return queryset

    def get_additional_columns(self, request):
        """Get additional columns based on report type"""
        report_type = request.GET.get("report_type", "standard")

        if report_type == "submitted":
            return ["Submission Date"]
        elif report_type == "completed":
            return ["Completion Date"]

        return None

    def create_pdf_response(self, pdf_content, filename):
        """Create HTTP response with PDF content"""
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}.pdf"'
        response.write(pdf_content)
        return response


class BulkReportView(BaseReportGeneratorMixin, APIView):
    """Generate bulk reports (ZIP file containing multiple PDFs)"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Generate multiple reports and return as ZIP file"""
        report_configs = request.data.get("reports", [])

        if not report_configs:
            return Response({"error": "No report configurations provided"}, status=400)

        # Create ZIP file in memory
        zip_buffer = io.BytesIO()

        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for config in report_configs:
                report_type = config.get("type")
                filters = config.get("filters", {})

                # Generate PDF based on report type
                if report_type == "network":
                    pdf_content = self.generate_network_report(request, filters)
                    filename = (
                        f"network_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    )
                elif report_type == "organization":
                    pdf_content = self.generate_organization_report(request, filters)
                    filename = f"organization_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                elif report_type == "adviser":
                    pdf_content = self.generate_adviser_report(request, filters)
                    filename = (
                        f"adviser_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                    )
                else:
                    continue

                # Add PDF to ZIP
                zip_file.writestr(filename, pdf_content)

        # Prepare response
        zip_content = zip_buffer.getvalue()
        zip_buffer.close()

        response = HttpResponse(content_type="application/zip")
        response["Content-Disposition"] = (
            f'attachment; filename="bulk_reports_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip"'
        )
        response.write(zip_content)

        return response

    def generate_network_report(self, request, filters):
        """Generate network report with given filters"""
        # Implementation similar to NetworkReportView
        # This is a simplified version
        cases = Case.objects.all()  # Apply appropriate filters
        return self.create_pdf_report(cases, "Network Report", None)

    def generate_organization_report(self, request, filters):
        """Generate organization report with given filters"""
        # Implementation similar to OrganizationReportView
        cases = Case.objects.all()  # Apply appropriate filters
        return self.create_pdf_report(cases, "Organization Report", None)

    def generate_adviser_report(self, request, filters):
        """Generate adviser report with given filters"""
        # Implementation similar to AdviserReportView
        cases = Case.objects.filter(created_by=request.user)
        return self.create_pdf_report(cases, "Adviser Report", None)
