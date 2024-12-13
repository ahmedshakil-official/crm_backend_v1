from django.urls import path
from .views import (
    CaseListCreateApiView,
    CaseRetrieveUpdateDeleteApiView,
    FileListCreateApiView,
    FileRetrieveUpdateDeleteApiView,
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
]
