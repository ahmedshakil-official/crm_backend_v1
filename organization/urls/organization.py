from django.urls import path, include
from rest_framework.routers import DefaultRouter
from organization.views.organization import OrganizationViewSet, DirectorOrganizationViewSet

router = DefaultRouter()
router.register("", OrganizationViewSet, basename="organization")
router.register("admin", DirectorOrganizationViewSet, basename="director-organization")

urlpatterns = [
    path('', include(router.urls)),
]
