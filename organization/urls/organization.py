from django.urls import path

from organization.views.organization import (
    UserOrganizationListAPIView,
    UserOrganizationRetrieveAPIView,
    OrganizationListCreateApiView,
    OrganizationRetrieveUpdateDestroyApiView,
)

urlpatterns = [
    path("", UserOrganizationListAPIView.as_view(), name="organization-list"),
    path(
        "details/",
        UserOrganizationRetrieveAPIView.as_view(),
        name="organization",
    ),
    path("list/", OrganizationListCreateApiView.as_view(), name="organization-list-create"),
    path("list/<slug:slug>/", OrganizationRetrieveUpdateDestroyApiView.as_view(), name="organization-details"),
]
