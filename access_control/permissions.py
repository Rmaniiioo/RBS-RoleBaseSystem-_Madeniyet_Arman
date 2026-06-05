from rest_framework.permissions import BasePermission
from access_control.services import can_access

class IsAccessRulesAdmin(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_active
            and can_access(request.user, 'acces_rules', 'read')
        )