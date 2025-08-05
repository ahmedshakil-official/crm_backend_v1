from django.urls import path

from .views import OrganizationNetworkDashboardListView, OrganizationDashboardListView

urlpatterns = [
    path("common/", OrganizationNetworkDashboardListView.as_view(), name='common-dashboard'),
    path("organization/<slug:slug>/", OrganizationDashboardListView.as_view(), name='organization-dashboard'),
]
