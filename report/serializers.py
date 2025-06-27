from rest_framework import serializers
from .models import Case


class ReportFilterSerializer(serializers.Serializer):
    """Serializer for report filter parameters"""

    start_date = serializers.DateField(required=False)
    end_date = serializers.DateField(required=False)
    case_status = serializers.CharField(required=False)
    case_stage = serializers.CharField(required=False)
    report_type = serializers.ChoiceField(
        choices=["standard", "submitted", "completed"], default="standard"
    )
    network_id = serializers.IntegerField(required=False)  # For admin reports
    organization_id = serializers.IntegerField(required=False)  # For admin reports


class BulkReportConfigSerializer(serializers.Serializer):
    """Serializer for bulk report configuration"""

    type = serializers.ChoiceField(
        choices=["network", "organization", "adviser", "admin"]
    )
    filters = ReportFilterSerializer(required=False)


class BulkReportRequestSerializer(serializers.Serializer):
    """Serializer for bulk report request"""

    reports = BulkReportConfigSerializer(many=True)


class ReportMetadataSerializer(serializers.Serializer):
    """Serializer for report metadata"""

    total_cases = serializers.IntegerField()
    date_range = serializers.CharField()
    generated_by = serializers.CharField()
    generated_at = serializers.DateTimeField()
    portal_type = serializers.CharField()
