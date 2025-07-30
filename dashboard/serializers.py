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

    def get_count_in_period(self, networks, days):
        today = timezone.now().date()
        start = today - timedelta(days=days)
        return Case.objects.filter(
            network__in=networks,
            case_category=ProductCategoryChoices.MORTGAGE,
            case_stage=CaseStageChoices.ENQUIRY,
            created_at__gte=start
        ).count()

    def get_count_30_days(self, obj):
        filter_param = self.context.get('filter')
        if filter_param not in ["30_days", "all"]:
            return None
        networks = self.context.get('networks', [])
        return self.get_count_in_period(networks, 30)

    def get_count_6_months(self, obj):
        filter_param = self.context.get('filter')
        if filter_param not in ["6_months", "all"]:
            return None
        networks = self.context.get('networks', [])
        return self.get_count_in_period(networks, 180)

    def get_count_1_year(self, obj):
        filter_param = self.context.get('filter')
        if filter_param not in ["1_year", "all"]:
            return None
        networks = self.context.get('networks', [])
        return self.get_count_in_period(networks, 365)
