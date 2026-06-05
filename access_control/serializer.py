from rest_framework import serializers
from access_control.models import AccessRoleRule, BussinesElement, Role

class RoleSerializers(serializers.Modelserializer):
    class Meta:
        model = Role
        fields = ['id', 'code', 'name', 'description', 'is_system']

class BussinessElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRoleRule
        fields = [
            'id',
            'role',
            'role_code',
            'element',
            'element_code',
            'read_permission',
            'read_all_permission',
            'create_permission',
            'update_permission',
            'update_all_permission',
            'delete_permission',
            'delete_all_permission',
        ]
