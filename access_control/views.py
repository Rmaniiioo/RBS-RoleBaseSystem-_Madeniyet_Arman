from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from access_control.models import Role, BusinessElement, AccessRoleRule
from access_control.permissions import IsAccessRulesAdmin
from access_control.services import assert_can_access
from access_control.serializer import (
    AccessRoleRuleSerializer,
    BusinessElementSerializer,
    RoleSerializer,
)

class AccessAdminMixin:
    permission_classes = [IsAuthenticated, IsAccessRulesAdmin]

    def perform_create(self, serializer):
        assert_can_access(self.request.user, 'access_rules', 'create')
        serializer.save()

    def perform_update(self, serializer):
        assert_can_access(self.request.user, 'access_rules', 'update')
        serializer.save()

    def perform_destroy(self, instance):
        assert_can_access(self.request.user, 'access_rules', 'delete')
        instance.delete()


class RoleViewSet(AccessAdminMixin, viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer


class BusinessElementViewSet(AccessAdminMixin, viewsets.ModelViewSet):
    queryset = BusinessElement.objects.all() # Исправлено!
    serializer_class = BusinessElementSerializer


class AccessRoleRuleViewSet(AccessAdminMixin, viewsets.ModelViewSet):
    queryset = AccessRoleRule.objects.select_related('role', 'element').all() 
    serializer_class = AccessRoleRuleSerializer