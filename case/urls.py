from django.urls import path
from .views import CaseListCreateApiView, CaseRetrieveUpdateDeleteApiView

urlpatterns = [
    path("", CaseListCreateApiView.as_view(), name="case-list-create"),
    path("<uuid:alias>/", CaseRetrieveUpdateDeleteApiView.as_view(), name="case-retrieve-update-delete"),
]
