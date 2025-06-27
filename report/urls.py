from django.urls import path
from .views import (
    NetworkReportView,
    OrganizationReportView,
    AdviserReportView,
    AdminReportView,
    BulkReportView,
)

urlpatterns = [
    path("network/", NetworkReportView.as_view(), name="network-report"),
    path("organization/", OrganizationReportView.as_view(), name="organization-report"),
    path("adviser/", AdviserReportView.as_view(), name="adviser-report"),
    path("admin/", AdminReportView.as_view(), name="admin-report"),
    path("bulk/", BulkReportView.as_view(), name="bulk-report"),
]
