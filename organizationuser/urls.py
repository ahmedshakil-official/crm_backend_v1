from django.urls import path, include

from organizationuser.views import (
    OrganizationUserListCreateView, OrganizationUserRetrieveUpdateDeleteView,
)


urlpatterns = [

    path(
        "",
        OrganizationUserListCreateView.as_view(),
        name="organization-user-list-create",
    ),
    path(
        "<str:alias>/",
        OrganizationUserRetrieveUpdateDeleteView.as_view(),
        name="organization-user-retrieve-update-delete",
    ),
]
