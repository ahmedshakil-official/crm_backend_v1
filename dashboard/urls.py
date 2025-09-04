from django.urls import path

from .views import OrganizationNetworkDashboardListView, OrganizationDashboardListView, OrganisationStatusView

urlpatterns = [
    path("common/", OrganizationNetworkDashboardListView.as_view(), name='common-dashboard'),
    path("organization/<slug:slug>/", OrganizationDashboardListView.as_view(), name='network-organization-dashboard'),
    path("organization/<slug:slug>/cases/",
         OrganisationStatusView.as_view(), {"section": "cases"}),
    path("organization/<slug:slug>/<str:org_user>/",
         OrganisationStatusView.as_view(), {"section": "people"}),
]
