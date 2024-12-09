from django.urls import path

from organization.views.organization import (
    UserOrganizationListAPIView,
    UserOrganizationRetrieveAPIView,
)

urlpatterns = [
    path("", UserOrganizationListAPIView.as_view(), name="organization-list"),
    path(
        "details/",
        UserOrganizationRetrieveAPIView.as_view(),
        name="organization-details",
    ),
]
