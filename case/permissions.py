from rest_framework.permissions import BasePermission
from case.models import JointUser
from case.models import Case

class CaseLead(BasePermission):
    def has_permission(self, request, view):
        case_id = view.kwargs.get('case_id')
        if not request.user.is_authenticated and not request.user:
            return False

        if not case_id:
            return False
        return Case.objects.filter(
            case_id=case_id,
            lead = request.user,
            is_removed=False
        ).exists()


class IsCaseJointUser(BasePermission):
    def has_permission(self, request, view):
        case_id = view.kwargs.get('case_id')
        if not request.user or not request.user.is_authenticated:
            return False

        if not case_id:
            return False

        return JointUser.objects.filter(
            case_id=case_id,
            joint_user=request.user,
            is_removed=False
        ).exists()
