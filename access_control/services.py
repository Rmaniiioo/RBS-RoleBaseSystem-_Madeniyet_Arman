from rest_framework.exceptions import PermissionDenied

from access_control.models import AccessRoleRule


ACTION_TO_FIELDS = {
    "read": ("read_permission", "read_all_permission"),
    "create": ("create_permission", None),
    "update": ("update_permission", "update_all_permission"),
    "delete": ("delete_permission", "delete_all_permission"),
}


def get_rule(user, element_code):
    return AccessRoleRule.objects.select_related("role", "element").filter(
        role=user.role,
        element__code=element_code,
    ).first()


def can_access(user, element_code, action, owner_id=None):
    if not user or not getattr(user, "is_active", False):
        return False

    own_field, all_field = ACTION_TO_FIELDS[action]
    rule = get_rule(user, element_code)
    if not rule:
        return False

    if all_field and getattr(rule, all_field):
        return True

    if getattr(rule, own_field):
        return owner_id is None or owner_id == user.id

    return False


def assert_can_access(user, element_code, action, owner_id=None):
    if not can_access(user, element_code, action, owner_id):
        raise PermissionDenied("Forbidden for current role and resource.")

