from django.urls import path

from organizationuser.views import (
    OrganizationUserListCreateView,
    OrganizationUserRetrieveUpdateDeleteView,
    AdvisorRetrieveUpdateDeleteView,
    AdvisorListCreateView,
    IntroducerRetrieveUpdateDeleteView,
    IntroducerListCreateView,
    ClientRetrieveUpdateDeleteView,
    ClientListCreateView,
    LeadRetrieveUpdateDeleteView,
    LeadListCreateView,
)


urlpatterns = [
    path(
        "",
        OrganizationUserListCreateView.as_view(),
        name="organization-user-list-create",
    ),
    path(
        "<uuid:alias>/",
        OrganizationUserRetrieveUpdateDeleteView.as_view(),
        name="organization-user-retrieve-update-delete",
    ),
    # Lead URLs
    path("leads/", LeadListCreateView.as_view(), name="lead-list-create"),
    path(
        "leads/<uuid:alias>/",
        LeadRetrieveUpdateDeleteView.as_view(),
        name="lead-retrieve-update-delete",
    ),
    # Client URLs
    path("clients/", ClientListCreateView.as_view(), name="client-list-create"),
    path(
        "clients/<uuid:alias>/",
        ClientRetrieveUpdateDeleteView.as_view(),
        name="client-retrieve-update-delete",
    ),
    # Introducer URLs
    path(
        "introducers/",
        IntroducerListCreateView.as_view(),
        name="introducer-list-create",
    ),
    path(
        "introducers/<uuid:alias>/",
        IntroducerRetrieveUpdateDeleteView.as_view(),
        name="introducer-retrieve-update-delete",
    ),
    # # Advisor URLs
    path("advisors/", AdvisorListCreateView.as_view(), name="advisor-list-create"),
    path(
        "advisors/<uuid:alias>/",
        AdvisorRetrieveUpdateDeleteView.as_view(),
        name="advisor-retrieve-update-delete",
    ),
]
