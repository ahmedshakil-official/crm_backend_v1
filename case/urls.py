from django.urls import path

from .models import LoanDetails
from .views import (
    CaseListCreateApiView,
    CaseRetrieveUpdateDeleteApiView,
    FileListCreateApiView,
    FileRetrieveUpdateDeleteApiView,
    JointUserListCreateApiView,
    JointUserRetrieveUpdateDeleteApiView,
    CaseUserListApiView,
    LoanDetailsListCreateApiView,
    LoanDetailsRetrieveUpdateApiView,
    CaseUserListViewOnlyApiView,
)

urlpatterns = [
    path("", CaseListCreateApiView.as_view(), name="case-list-create"),
    path(
        "<uuid:alias>/",
        CaseRetrieveUpdateDeleteApiView.as_view(),
        name="case-retrieve-update-delete",
    ),
    path(
        "<uuid:case_alias>/files/",
        FileListCreateApiView.as_view(),
        name="file-list-create",
    ),
    path(
        "<uuid:case_alias>/files/<uuid:alias>/",
        FileRetrieveUpdateDeleteApiView.as_view(),
        name="file-detail",
    ),
    path(
        "<uuid:case_alias>/joint/users/",
        JointUserListCreateApiView.as_view(),
        name="joint-user-list-create",
    ),
    path(
        "<uuid:case_alias>/joint/users/<uuid:alias>/",
        JointUserRetrieveUpdateDeleteApiView.as_view(),
        name="joint-user-detail",
    ),
    path(
        "<uuid:case_alias>/users/",
        CaseUserListApiView.as_view(),
        name="case-user-list",
    ),
    path(
        "<uuid:case_alias>/loan/details/",
        LoanDetailsListCreateApiView.as_view(),
        name="loan-details-list-create",
    ),
    path(
        "<uuid:case_alias>/loan/details/<uuid:alias>/",
        LoanDetailsRetrieveUpdateApiView.as_view(),
        name="loan-details-detail",
    ),
    path(
        "<uuid:case_alias>/user/list",
        CaseUserListViewOnlyApiView.as_view(),
        name="case-users",
    ),
]
