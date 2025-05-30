from django.db import models
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from common.enums import UserTypeChoices
from organization.models import Organization, OrganizationUser, Network, NetworkUser



class AuthenticationRequiredMixin:
    """Mixin to handle authentication checks"""

    def check_authentication(self):
        if not self.request.user.is_authenticated:
            raise ValidationError("User must be authenticated.")

    def get_user_context(self):
        """
        Determines if user is associated with an organization or network.
        Returns a dict with 'type', 'instance', 'model', and 'serializer' keys.
        """
        self.check_authentication()
        user = self.request.user

        # Check if user is associated with an organization
        organization_user = OrganizationUser.objects.filter(user=user).first()
        if organization_user:
            # Import here to avoid circular imports
            from organization.serializers import OrganizationUserSerializer
            from .serializers import (
                OrganizationUserListCreateSerializer,
                OrganizationUserRetrieveUpdateDeleteSerializer,
            )
            return {
                'type': 'organization',
                'instance': organization_user.organization,
                'model': OrganizationUser,
                'full_serializer': OrganizationUserSerializer,
                'list_create_serializer': OrganizationUserListCreateSerializer,
                'retrieve_update_delete_serializer': OrganizationUserRetrieveUpdateDeleteSerializer,
                'foreign_key_field': 'organization'
            }

        # Check if user is associated with a network
        network_user = NetworkUser.objects.filter(user=user).first()
        if network_user:
            # Import NetworkUser serializers
            from .serializers import (
                NetworkUserSerializer,
                NetworkUserListCreateSerializer,
                NetworkUserRetrieveUpdateDeleteSerializer,
            )
            return {
                'type': 'network',
                'instance': network_user.network,
                'model': NetworkUser,
                'full_serializer': NetworkUserSerializer,
                'list_create_serializer': NetworkUserListCreateSerializer,
                'retrieve_update_delete_serializer': NetworkUserRetrieveUpdateDeleteSerializer,
                'foreign_key_field': 'network'
            }

        # If neither found, raise error
        raise PermissionDenied(
            "You cannot perform this action without being associated with an organization or network."
        )


class BaseUserView:
    """Base class containing common functionality for user views (works for both Organization and Network users)"""
    permission_classes = [IsAuthenticated]
    lookup_field = "alias"

    def get_base_queryset(self):
        self.check_authentication()
        user_context = self.get_user_context()

        # Get the appropriate model and filter
        model = user_context['model']
        instance = user_context['instance']
        foreign_key_field = user_context['foreign_key_field']

        # Create filter kwargs dynamically
        filter_kwargs = {foreign_key_field: instance}

        return model.objects.filter(
            **filter_kwargs
        ).select_related(foreign_key_field, "user", "created_by", "updated_by")

    def get_serializer_class(self):
        """Dynamically return the appropriate serializer class"""
        user_context = self.get_user_context()
        return user_context['full_serializer']

    def get_serializer_context(self):
        """Add user context to serializer"""
        context = super().get_serializer_context()
        context['user_context'] = self.get_user_context()
        return context


class UserListCreateView(AuthenticationRequiredMixin, BaseUserView, ListCreateAPIView):
    """Generic view for listing and creating users (works for both org and network users)"""

    def get_queryset(self):
        return self.get_base_queryset()

    def perform_create(self, serializer):
        user_context = self.get_user_context()
        instance = user_context['instance']
        foreign_key_field = user_context['foreign_key_field']

        # Create save kwargs dynamically
        save_kwargs = {
            foreign_key_field: instance,
            'created_by': self.request.user,
            'updated_by': self.request.user,
        }

        serializer.save(**save_kwargs)


class UserRetrieveUpdateDeleteView(AuthenticationRequiredMixin, BaseUserView, RetrieveUpdateDestroyAPIView):
    """Generic view for retrieving, updating and deleting users (works for both org and network users)"""

    def get_queryset(self):
        return self.get_base_queryset()

    def perform_update(self, serializer):
        self.check_authentication()
        serializer.save(updated_by=self.request.user)


class BaseRoleSpecificView:
    """Base class for role-specific views"""
    role = None  # Must be set by subclasses

    def get_role_filtered_queryset(self):
        base_queryset = self.get_base_queryset()
        return base_queryset.filter(role=self.role)

    def get_serializer_class(self):
        """Return role-specific serializer for list/create operations"""
        user_context = self.get_user_context()
        return user_context['list_create_serializer']


class RoleSpecificListCreate(BaseRoleSpecificView, UserListCreateView):

    def get_queryset(self):
        return self.get_role_filtered_queryset()

    def perform_create(self, serializer):
        user_context = self.get_user_context()
        instance = user_context['instance']
        foreign_key_field = user_context['foreign_key_field']

        # Create save kwargs dynamically
        save_kwargs = {
            'role': self.role,
            foreign_key_field: instance,
            'created_by': self.request.user,
        }

        serializer.save(**save_kwargs)


class RoleSpecificRetrieveUpdateDelete(BaseRoleSpecificView, UserRetrieveUpdateDeleteView):

    def get_serializer_class(self):
        """Return role-specific serializer for retrieve/update/delete operations"""
        user_context = self.get_user_context()
        return user_context['retrieve_update_delete_serializer']

    def get_queryset(self):
        return self.get_role_filtered_queryset()


# Role-specific view implementations (work for both org and network users)
class LeadListCreateView(RoleSpecificListCreate):
    role = UserTypeChoices.LEAD


class LeadRetrieveUpdateDeleteView(RoleSpecificRetrieveUpdateDelete):
    role = UserTypeChoices.LEAD


class ClientListCreateView(RoleSpecificListCreate):
    role = UserTypeChoices.CLIENT


class ClientRetrieveUpdateDeleteView(RoleSpecificRetrieveUpdateDelete):
    role = UserTypeChoices.CLIENT


class IntroducerListCreateView(RoleSpecificListCreate):
    role = UserTypeChoices.INTRODUCER


class IntroducerRetrieveUpdateDeleteView(RoleSpecificRetrieveUpdateDelete):
    role = UserTypeChoices.INTRODUCER


class AdvisorListCreateView(RoleSpecificListCreate):
    role = UserTypeChoices.ADVISOR


class AdvisorRetrieveUpdateDeleteView(RoleSpecificRetrieveUpdateDelete):
    role = UserTypeChoices.ADVISOR