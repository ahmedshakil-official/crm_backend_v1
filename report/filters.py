# reports/filters.py
from __future__ import annotations
import calendar
import datetime as dt
from typing import Mapping, Tuple, Optional

import pytz
from django.db.models import Q
from django.utils import timezone

DHAKA_TZ = pytz.timezone("Asia/Dhaka")

DATE_FIELD_MAP = {
    "standard": "created_at",
    "submitted": "submitted_date",
    "completed": "completed_date",
}

# Public API
def build_date_filter_q(
    params: Mapping[str, str],
    report_type: str,
    tz: Optional[dt.tzinfo] = DHAKA_TZ,
) -> Tuple[Q, str]:
    """
    Returns (Q, human_label) for the selected date filter.

    Expected params keys (string values):
      - date_filter: one of {"today", "this_week", "this_month", "this_year", "range"}
      - from_date: "YYYY-MM-DD" (if date_filter == "range")
      - to_date: "YYYY-MM-DD"   (if date_filter == "range")
      - month: month name ("August") or number ("8") [optional for "this_month" to override]
      - year: "2024" or "2025" [optional for this_month/this_year to override]

    Week starts on Monday. All bounds are inclusive start, exclusive end.
    """
    df = (params.get("date_filter") or "").lower().strip()
    if df not in {"today", "this_week", "this_month", "this_year", "range"}:
        # Default to "this_month" if not provided
        df = "this_month"

    date_field = DATE_FIELD_MAP.get(report_type, "created_at")
    start, end, label = _compute_bounds(df, params, tz)

    q = Q(**{f"{date_field}__gte": start, f"{date_field}__lt": end})
    return q, label


# ---------------- internal helpers ---------------- #

def _compute_bounds(
    kind: str,
    params: Mapping[str, str],
    tz: Optional[dt.tzinfo],
) -> Tuple[dt.datetime, dt.datetime, str]:
    now = timezone.now().astimezone(tz) if tz else timezone.localtime()
    today = now.date()

    if kind == "today":
        start = _start_of_day(today, tz)
        end = start + dt.timedelta(days=1)
        return start, end, f"Today ({today.strftime('%d %b %Y')})"

    if kind == "this_week":
        # Monday = 0
        weekday = today.weekday()
        monday = today - dt.timedelta(days=weekday)
        start = _start_of_day(monday, tz)
        end = start + dt.timedelta(days=7)
        label = f"This Week ({start.date().strftime('%d %b')} – {(end - dt.timedelta(days=1)).date().strftime('%d %b %Y')})"
        return start, end, label

    if kind == "this_month":
        month, year = _resolve_month_year(params, default_date=today)
        start_date = dt.date(year, month, 1)
        _, last_day = calendar.monthrange(year, month)
        end_date = start_date.replace(day=last_day) + dt.timedelta(days=1)
        start = _start_of_day(start_date, tz)
        end = _start_of_day(end_date, tz)
        label = f"{calendar.month_name[month]} {year}"
        return start, end, label

    if kind == "this_year":
        year = _safe_int(params.get("year")) or today.year
        start = _start_of_day(dt.date(year, 1, 1), tz)
        end = _start_of_day(dt.date(year + 1, 1, 1), tz)
        label = f"{year}"
        return start, end, label

    if kind == "range":
        start_str = (params.get("from_date") or "").strip()
        end_str = (params.get("to_date") or "").strip()  # inclusive date
        start_date = _parse_date_ymd(start_str) or today
        # end bound is exclusive; if user passes 2025-08-22, we go to 2025-08-23 00:00
        end_date = (_parse_date_ymd(end_str) or today) + dt.timedelta(days=1)
        start = _start_of_day(start_date, tz)
        end = _start_of_day(end_date, tz)
        label = f"{start_date.strftime('%d %b %Y')} → {(end_date - dt.timedelta(days=1)).strftime('%d %b %Y')}"
        return start, end, label

    # Fallback to this month
    month, year = _resolve_month_year(params, default_date=today)
    start_date = dt.date(year, month, 1)
    _, last_day = calendar.monthrange(year, month)
    end_date = start_date.replace(day=last_day) + dt.timedelta(days=1)
    start = _start_of_day(start_date, tz)
    end = _start_of_day(end_date, tz)
    label = f"{calendar.month_name[month]} {year}"
    return start, end, label


def _start_of_day(d: dt.date, tz: Optional[dt.tzinfo]) -> dt.datetime:
    naive = dt.datetime(d.year, d.month, d.day, 0, 0, 0)
    return timezone.make_aware(naive, tz) if tz else timezone.make_aware(naive)


def _parse_date_ymd(s: str) -> Optional[dt.date]:
    try:
        return dt.datetime.strptime(s, "%Y-%m-%d").date()
    except Exception:
        return None


def _resolve_month_year(params: Mapping[str, str], default_date: dt.date) -> Tuple[int, int]:
    raw_month = (params.get("month") or "").strip()
    raw_year = (params.get("year") or "").strip()

    year = _safe_int(raw_year) or default_date.year

    if not raw_month:
        return default_date.month, year

    # "August" or "aug" or "8"
    month_num = _month_to_int(raw_month)
    return month_num or default_date.month, year


def _safe_int(v: Optional[str]) -> Optional[int]:
    try:
        return int(v) if v else None
    except Exception:
        return None


def _month_to_int(val: str) -> Optional[int]:
    v = val.strip().lower()
    # numeric
    if v.isdigit():
        n = int(v)
        if 1 <= n <= 12:
            return n
        return None
    # name
    for i in range(1, 13):
        if v in {calendar.month_name[i].lower(), calendar.month_abbr[i].lower()}:
            return i
    return None
