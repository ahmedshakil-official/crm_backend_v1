from rest_framework.permissions import BasePermission
from common.enums import RoleChoices

class IsOrgUser(BasePermission):
    """
    Allow access only to users who are part of an Organization.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, "organization") and request.user.organization is not None


class IsNetworkUser(BasePermission):
    """
    Allow access only to users who are part of a Network.
    """
    def has_permission(self, request, view):
        return hasattr(request.user, "network") and request.user.network is not None


class IsOrgAdmin(BasePermission):
    """
    Allow access only to users who are part of an Organization and have ADMIN role.
    """
    def has_permission(self, request, view):
        user = request.user
        return (
            hasattr(user, "organization") and
            user.organization is not None and
            user.role == RoleChoices.ADMIN
        )


class IsNetworkAdmin(BasePermission):
    """
    Allow access only to users who are part of a Network and have ADMIN role.
    """
    def has_permission(self, request, view):
        user = request.user
        return (
            hasattr(user, "network") and
            user.network is not None and
            user.role == RoleChoices.ADMIN
        )

class IsOrgAdvisor(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            hasattr(user, "organization") and
            user.organization is not None and
            user.role == RoleChoices.ADVISOR
        )

class IsOrgIntroducer(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            hasattr(user, "organization") and
            user.organization is not None and
            user.role == RoleChoices.INTRODUCER
        )

class IsOrgClient(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            hasattr(user, "organization") and
            user.organization is not None and
            user.role == RoleChoices.CLIENT
        )

class IsNetworkAdvisor(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            hasattr(user, "network") and
            user.network is not None and
            user.role == RoleChoices.ADVISOR
        )

class IsNetworkIntroducer(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            hasattr(user, "network") and
            user.network is not None and
            user.role == RoleChoices.INTRODUCER
        )

class IsNetworkClient(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            hasattr(user, "network") and
            user.network is not None and
            user.role == RoleChoices.CLIENT
        )