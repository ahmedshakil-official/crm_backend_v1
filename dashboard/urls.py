from django.urls import path

from .views import OrganizationNetworkDashboardListView

urlpatterns = [
    path("", OrganizationNetworkDashboardListView.as_view(), name='network-dashboard'),
]
