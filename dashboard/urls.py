from django.urls import path

from .views import OrganizationNetworkDashboardListView

urlpatterns = [
    path("common/", OrganizationNetworkDashboardListView.as_view(), name='network-dashboard'),
]
