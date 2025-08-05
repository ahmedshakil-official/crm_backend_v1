from django.urls import path

from .views import NetworkDashboardListView

urlpatterns = [
    path('network/', NetworkDashboardListView.as_view(), name='network-dashboard'),
]
