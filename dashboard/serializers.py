from rest_framework import serializers
from django.utils import timezone
from datetime import timedelta

from case.models import Case
from common.enums import ProductCategoryChoices, CaseStageChoices


class MortgageEnquirySerializer(serializers.ModelSerializer):
    count_30_days = serializers.SerializerMethodField()
    count_6_months = serializers.SerializerMethodField()
    count_1_year = serializers.SerializerMethodField()

    class Meta:
        model = Case
        fields = [
            'count_30_days',
            'count_6_months',
            'count_1_year'
        ]

    def get_counts(self, networks, current_days, label):
        today = timezone.now()
        start_current = today - timedelta(days=current_days)
        start_previous = today - timedelta(days=current_days * 2)
        end_previous = start_current

        current = Case.objects.filter(
            network__in=networks,
            case_category=ProductCategoryChoices.MORTGAGE,
            case_stage=CaseStageChoices.ENQUIRY,
            created_at__gte=start_current
        ).count()

        previous = Case.objects.filter(
            network__in=networks,
            case_category=ProductCategoryChoices.MORTGAGE,
            case_stage=CaseStageChoices.ENQUIRY,
            created_at__gte=start_previous,
            created_at__lt=end_previous
        ).count()

        if previous == 0:
            percentage_change = 100.0 if current > 0 else 0.0
        else:
            percentage_change = ((current - previous) / previous) * 100.0

        return {
            "label": label,
            "count": current,
            "percentage_change": round(percentage_change, 2),
            "trend": "up" if percentage_change >= 0 else "down"
        }

    def get_count_30_days(self, obj):
        filter_param = self.context.get('filter')
        if filter_param not in ["30_days", "all"]:
            return None
        networks = self.context.get('networks', [])
        return self.get_counts(networks, 30, "New Mortgage Enquiries (30 days)")

    def get_count_6_months(self, obj):
        filter_param = self.context.get('filter')
        if filter_param not in ["6_months", "all"]:
            return None
        networks = self.context.get('networks', [])
        return self.get_counts(networks, 180, "New Mortgage Enquiries (6 months)")

    def get_count_1_year(self, obj):
        filter_param = self.context.get('filter')
        if filter_param not in ["1_year", "all"]:
            return None
        networks = self.context.get('networks', [])
        return self.get_counts(networks, 365, "New Mortgage Enquiries (1 year)")
