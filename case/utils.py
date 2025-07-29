from collections import defaultdict

from celery import group
from django.db.models.expressions import result
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count
from gprof2dot import labels



def upload_to_case_files(instance, filename):
    """
    Generates a dynamic upload path for files.
    The path is formatted as: case_files/%Y/%m/%d/case_<case_name>
    """
    case_name = instance.case.name or "unknown_case"
    sanitized_case_name = "".join(
        c if c.isalnum() or c in (" ", "_") else "" for c in case_name
    ).replace(" ", "_")
    return f"case_files/{instance.created_at:%Y/%m/%d}/case_{sanitized_case_name}/{filename}"


import secrets
import string


def get_random_string(length=12, allowed_chars=None):
    """
    Return a securely generated random string of specified length.
    By default, uses uppercase/lowercase letters and digits.
    """
    if allowed_chars is None:
        allowed_chars = string.ascii_letters + string.digits
    return "".join(secrets.choice(allowed_chars) for _ in range(length))


# This is for Mortgage Type (pie chart)
DURATION_MAP = {
    "one_month": timedelta(days=30),
    "six_month": timedelta(days=180),
    "one_year": timedelta(days=365),
}
COMMON_MORTGAGE_TYPES = {
    "PURCHASE": "Purchase",
    "REMORTGAGE": "Remortgage",
    "SECURED_LOAN": "Secure Loan",
    "FURTHER_ADVANCE": "Further Advance",
    "PRODUCT_TRANSFER": "Product Transfer",
    "UNSECURED": "Unsecured",
    "INVOICE_DISCOUNTING": "Invoice Discounting",
    "ASSET_FINANCE": "Asset Finance",
}

def get_mortgage_type_distribution_for_user(user, duration):
    from case.models import LoanDetails
    from organization.models import OrganizationUser
    from django.utils import timezone

    filter_date = timezone.now() - DURATION_MAP.get(duration, timedelta(days=365))

    # Get all network ids where user belongs through OrganizationUser
    network_ids = OrganizationUser.objects.filter(user=user).values_list("organization__network_id", flat=True).distinct()

    queryset = LoanDetails.objects.filter(
        case__organization__network_id__in=network_ids,
        case__created_at__gte=filter_date,
    ).exclude(mortgage_type__isnull=True)

    grouped = queryset.values("mortgage_type").annotate(count=Count("id"))

    result = {label: 0 for label in COMMON_MORTGAGE_TYPES.values()}
    others_count = 0

    for item in grouped:
        code = item["mortgage_type"]
        label = COMMON_MORTGAGE_TYPES.get(code)
        if label:
            result[label] += item["count"]
        else:
            others_count += item["count"]

    final_result = [{"label": label, "count": int(count)} for label, count in result.items()]
    final_result.append({"label": "Others", "count": int(others_count)})
    return final_result