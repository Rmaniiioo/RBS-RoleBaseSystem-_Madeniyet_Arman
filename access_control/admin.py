from django.contrib import admin

from .models import (
    Role,
    BusinessElement,
    AccessRoleRule,
)


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "name",
    )


@admin.register(BusinessElement)
class BusinessElementAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "code",
        "name",
    )


@admin.register(AccessRoleRule)
class AccessRoleRuleAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "role",
        "element",
        "read_permission",
        "read_all_permission",
        "create_permission",
        "update_permission",
        "update_all_permission",
        "delete_permission",
        "delete_all_permission",
    )