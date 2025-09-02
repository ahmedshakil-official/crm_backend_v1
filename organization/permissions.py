from rest_framework.permissions import BasePermission, SAFE_METHODS
from urllib3 import request

from .models import OrganizationUser, NetworkUser
from common.enums import OrganizationRoleChoices, NetworkRoleChoices


class IsOrgUser(BasePermission):
    """
    Allow access only to users who are part of an Organization.
    """

    def has_permission(self, request, view):
        user = request.user
        return (
            hasattr(request.user, "organization")
            and request.user.organization is not None
        )


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
        return OrganizationUser.objects.filter(
            user=user, role=OrganizationRoleChoices.ADMIN
        ).exists()


class IsNetworkAdmin(BasePermission):
    """
    Allow access only to users who are part of a Network and have ADMIN role.
    """

    def has_permission(self, request, view):
        user = request.user
        return NetworkUser.objects.filter(
            user=user, role=NetworkRoleChoices.ADMIN
        ).exists()


class IsOrgAdvisor(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return OrganizationUser.objects.filter(
            user=user, role=OrganizationRoleChoices.ADVISOR
        ).exists()

class IsNetworkAdvisor(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return NetworkUser.objects.filter(
            user=user, role=NetworkRoleChoices.ADVISOR
        ).exists()

class IsOrgIntroducer(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return OrganizationUser.objects.filter(
            user=user, role=OrganizationRoleChoices.INTRODUCER
        ).exists()

class IsNetworkIntroducer(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return NetworkUser.objects.filter(
            user=user, role=NetworkRoleChoices.INTRODUCER
        ).exists()

class IsOrgClient(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return OrganizationUser.objects.filter(
            user=user, role=OrganizationRoleChoices.CLIENT
        ).exists()


class IsNetworkClient(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return NetworkUser.objects.filter(
            user=user, role=NetworkRoleChoices.CLIENT
        ).exists()

class IsOrgLead(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return OrganizationUser.objects.filter(
            user=user, role=OrganizationRoleChoices.LEAD
        ).exists()

class IsNetworkLead(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return NetworkUser.objects.filter(
            user=user, role=NetworkRoleChoices.LEAD
        ).exists()

class IsOrgJoint_user(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return OrganizationUser.objects.filter(
            user=user, role=OrganizationRoleChoices.JOINT_USER
        ).exists()

class IsNetworkJoint_user(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return NetworkUser.objects.filter(
            user=user, role=NetworkRoleChoices.JOINT_USER
        ).exists()

class IsOrgCeo(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return OrganizationUser.objects.filter(
            user=user, role=OrganizationRoleChoices.ORGANIZATION_CEO
        ).exists()


class IsNetworkCeo(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return NetworkUser.objects.filter(
            user=user, role=NetworkRoleChoices.NETWORK_CEO
        ).exists()


class IsOrgCoo(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return OrganizationUser.objects.filter(
            user=user, role=OrganizationRoleChoices.ORGANIZATION_COO
        ).exists()


class IsNetworkCoo(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return NetworkUser.objects.filter(
            user=user, role=NetworkRoleChoices.NETWORK_COO
        ).exists()


class IsOrgSystemDeveloper(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return OrganizationUser.objects.filter(
            user=user, role=OrganizationRoleChoices.ORGANIZATION_SYSTEM_DEVELOPER
        ).exists()


class IsNetworkSystemDeveloper(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return NetworkUser.objects.filter(
            user=user, role=NetworkRoleChoices.NETWORK_SYSTEM_DEVELOPER
        ).exists()


class IsOrgComplianceManager(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return OrganizationUser.objects.filter(
            user=user, role=OrganizationRoleChoices.ORGANIZATION_COMPLIANCE_MANAGER
        ).exists()

class IsNetworkComplianceManager(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return NetworkUser.objects.filter(
            user=user, role=NetworkRoleChoices.NETWORK_COMPLIANCE_MANAGER
        ).exists()


class IsOrgComplianceAssistant(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return OrganizationUser.objects.filter(
            user=user,
            role=OrganizationRoleChoices.ORGANIZATION_COMPLIANCE_ASSISTANT
        ).exists()


class IsNetworkComplianceAssistant(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return NetworkUser.objects.filter(
            user=user, role=NetworkRoleChoices.NETWORK_COMPLIANCE_ASSISTANT
        ).exists()


class IsOrgPrincipalAdviser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return OrganizationUser.objects.filter(
            user=user, role=OrganizationRoleChoices.ORGANIZATION_PRINCIPAL_ADVISER
        ).exists()


class IsNetworkPrincipalAdviser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return NetworkUser.objects.filter(
            user=user, role=NetworkRoleChoices.NETWORK_PRINCIPAL_ADVISER
        ).exists()


class IsOrgAdviserRole(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return OrganizationUser.objects.filter(
            user=user, role=OrganizationRoleChoices.ORGANIZATION_ADVISER
        ).exists()

class IsNetworkAdviserRole(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return NetworkUser.objects.filter(
            user=user, role=NetworkRoleChoices.NETWORK_ADVISER
        ).exists()


class IsOrgAdminRole(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return OrganizationUser.objects.filter(
            user=user, role=OrganizationRoleChoices.ORGANIZATION_ADMIN
        ).exists()

class IsNetworkAdminRole(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return NetworkUser.objects.filter(
            user=user, role = NetworkRoleChoices.NETWORK_ADMIN
        ).exists()

class IsOrgSupport(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return OrganizationUser.objects.filter(
            user=user, role=OrganizationRoleChoices.ORGANIZATION_SUPPORT
        ).exists()


class IsNetworkSupport(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return NetworkUser.objects.filter(
            user=user, role=NetworkRoleChoices.NETWORK_SUPPORT
        ).exists()

# This permission checked is organization user or not and is network user or not.
class IsInOrgOrNetwork(BasePermission):
    message = "You must belong to an Organization or a Network."

    #Views level permission.
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return (
            OrganizationUser.objects.filter(user=user).exists()
            or NetworkUser.objects.filter(user=user).exists()
        )
    # Objects Level permission.
    def has_object_permission(self, request, view, obj):
        user = request.user

        # using safe methods (GET, HEAD, OPTIONS)
        if request.method in SAFE_METHODS:
            return True

        # Checked organization or not
        if hasattr(obj, "organization") and obj.organization:
            return OrganizationUser.objects.filter(
                user=user, organization=obj.organization
            ).exists()

        #Checked network or not.
        if hasattr(obj, "network") and obj.network:
            return NetworkUser.objects.filter(
                user=user, network=obj.network
            ).exists()

        return False

# Advisor can create and update and Admin can create, update, delete
class CasePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        if request.method == "POST":
            return (
                OrganizationUser.objects.filter(user=user, role=OrganizationRoleChoices.ORGANIZATION_ADVISER).exists()
                or NetworkUser.objects.filter(user=user, role=NetworkRoleChoices.NETWORK_ADVISER).exists()
                or OrganizationUser.objects.filter(user=user, role=OrganizationRoleChoices.ORGANIZATION_ADMIN).exists()
                or NetworkUser.objects.filter(user=user, role=NetworkRoleChoices.NETWORK_ADMIN).exists()
            )
        if request.method in ("PUT", "PATCH"):
            return (
                    OrganizationUser.objects.filter(user=user, role=OrganizationRoleChoices.ORGANIZATION_ADVISER).exists()
                    or NetworkUser.objects.filter(user=user, role=NetworkRoleChoices.NETWORK_ADVISER).exists()
                    or OrganizationUser.objects.filter(user=user, role=OrganizationRoleChoices.ORGANIZATION_ADMIN).exists()
                    or NetworkUser.objects.filter(user=user, role=NetworkRoleChoices.NETWORK_ADMIN).exists()
            )

        if request.method == "DELETE":
            return (
                OrganizationUser.objects.filter(user=user, role=OrganizationRoleChoices.ORGANIZATION_ADMIN).exists()
                or NetworkUser.objects.filter(user=user, role=NetworkRoleChoices.NETWORK_ADMIN).exists()
            )

        return False

# Notes, Loan-details, applicant-details, products, properties, client survey api.
#clint can create, update with Advisor and admin.
class CasePermissionForClintUpdate(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True

        if request.method == "POST":
            return (
                OrganizationUser.objects.filter(user=user, role=OrganizationRoleChoices.ORGANIZATION_ADVISER).exists()
                or NetworkUser.objects.filter(user=user, role=NetworkRoleChoices.NETWORK_ADVISER).exists()
                or OrganizationUser.objects.filter(user=user, role=OrganizationRoleChoices.ORGANIZATION_ADMIN).exists()
                or NetworkUser.objects.filter(user=user, role=NetworkRoleChoices.NETWORK_ADMIN).exists()
                or OrganizationUser.objects.filter(user=user, role=OrganizationRoleChoices.CLIENT).exists()
                or NetworkUser.objects.filter(user=user, role=NetworkRoleChoices.CLIENT).exists()
            )
        if request.method in ("PUT", "PATCH"):
            return (
                OrganizationUser.objects.filter(user=user, role=OrganizationRoleChoices.ORGANIZATION_ADVISER).exists()
                or NetworkUser.objects.filter(user=user, role=NetworkRoleChoices.NETWORK_ADVISER).exists()
                or OrganizationUser.objects.filter(user=user, role=OrganizationRoleChoices.ORGANIZATION_ADMIN).exists()
                or NetworkUser.objects.filter(user=user, role=NetworkRoleChoices.NETWORK_ADMIN).exists()
                or OrganizationUser.objects.filter(user=user, role=OrganizationRoleChoices.CLIENT).exists()
                or NetworkUser.objects.filter(user=user, role=NetworkRoleChoices.CLIENT).exists()
            )
        if request.method == "DELETE":
            return (
                OrganizationUser.objects.filter(user=user, role=OrganizationRoleChoices.ORGANIZATION_ADMIN).exists()
                or NetworkUser.objects.filter(user=user, role=NetworkRoleChoices.NETWORK_ADMIN).exists()
            )

# For lead user.
class LeadPermission(BasePermission):
    message = "No permission without Lead user."
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return (
                OrganizationUser.objects.filter(user=user, role__in=[OrganizationRoleChoices.LEAD, OrganizationRoleChoices.ADMIN]).exists()
                or NetworkUser.objects.filter(user=user, role__in=[NetworkRoleChoices.LEAD, NetworkRoleChoices.ADMIN]).exists()
        )

class ClientPermission(BasePermission):
    message = "No permission without Client user."
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return (
                OrganizationUser.objects.filter(user=user, role__in=[OrganizationRoleChoices.CLIENT, OrganizationRoleChoices.ADMIN]).exists()
                or NetworkUser.objects.filter(user=user, role__in=[NetworkRoleChoices.CLIENT, NetworkRoleChoices.ADMIN]).exists()
        )

class IntroducerPermission(BasePermission):
    message = "No permission without Introducer user."
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return (
            OrganizationUser.objects.filter(user=user, role__in=[OrganizationRoleChoices.INTRODUCER, OrganizationRoleChoices.ADMIN]).exists()
            or NetworkUser.objects.filter(user=user,role__in=[NetworkRoleChoices.INTRODUCER, NetworkRoleChoices.ADMIN]).exists()
        )

class AdvisorPermission(BasePermission):
    message = "No permission without Advisor user."
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return (
                OrganizationUser.objects.filter(user=user, role__in=[OrganizationRoleChoices.ADVISOR,OrganizationRoleChoices.ADMIN]).exists()
                or NetworkUser.objects.filter(user=user, role__in=[NetworkRoleChoices.ADVISOR,NetworkRoleChoices.ADMIN]).exists()
        )