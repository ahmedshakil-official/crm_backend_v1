from django.urls import path

from .views import OrganizationNetworkDashboardListView, OrganizationDashboardListView, NetworkOrganizationLeadListCreateView

urlpatterns = [
    path("common/", OrganizationNetworkDashboardListView.as_view(), name='common-dashboard'),
    path("organization/<slug:slug>/", OrganizationDashboardListView.as_view(), name='network-organization-dashboard'),
    path("organization/<slug:slug>/leads/", NetworkOrganizationLeadListCreateView.as_view(), name="network-organization-lead-list-create"),
]
