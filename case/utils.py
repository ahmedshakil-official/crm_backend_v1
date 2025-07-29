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

# Lenders pie chart.
from collections import Counter
from case.enums import LenderChoices

LENDERS_TO_SHOW = [
     "BARCLAYS",
    "HALIFAX",
    "NATWEST",
    "NATIONWIDE",
    "AMICUS PLC",
    "SANTANDER",
    "ATOM_BANK",
    "ACCORD MORTGAGES",
]
def get_lender_pie_chart_data(queryset):
    lender_list = list(queryset.values_list('lender', flat=True))
    lender_counter = Counter(lender_list)

    result = []
    others_count = 0

    for lender, count in lender_counter.items():
        if lender in LENDERS_TO_SHOW:
            result.append({"lender": lender, "count": float(count)})
        else:
            others_count += count

    for lender in LENDERS_TO_SHOW:
        if lender not in [r["lender"] for r in result]:
            result.append({"lender": lender, "count": 0.0})

    if others_count > 0:
        result.append({"lender": "Others", "count": float(others_count)})

    def sort_key(x):
        if x["lender"] == "Others":
            return len(LENDERS_TO_SHOW) + 1
        return LENDERS_TO_SHOW.index(x["lender"])

    result.sort(key=sort_key)
    return result