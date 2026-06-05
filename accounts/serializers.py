from rest_framework import serializers
from access_control.models import Role
from access_control.models import RevokedToken, User
from access_control.models import hash_password, verify_password

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(source='role.code', read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "middle_name",
            "full_name",
            "email",
            "role",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "role", "is_active", "created_at", "updated_at"]


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    middle_name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
    password = serializers.CahrField(write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError('user with this email already exists.')
        return value.lower()
    
    def validate(self, attrs):
        if attrs ['password_repeat'] != attrs['password']:
            raise serializers.ValidationError({'password_repeat' 'Password do not match.'})
        return attrs
    
    def create(self, validate_data):
        validate_data.pop('password_repeat')
        password = validate_data.pop('password')
        role, _ = Role.objects.get_or_create(
            code = 'user',
            defaults = {'name': 'User', 'description': 'Default registred user.'}
        )
        return User.objects.create(
            role=role,
            password_hash=hash_password(password),
            **validate_data,
        )
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        try:
            user = User.objects.selected_related('role').get(email__iexact=attrs['email'], is_active=True)
        except User.DoesNotExist as exc:
            raise serializers.ValidationError('Invalid email or password.') from exc
        
        if not verify_password(attrs['password'], user.password_hash):
            raise serializers.ValidationError('Invalid email or password')
        
        attrs['user'] = user
        return attrs
    

class ProfilieUPdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'middle_name', 'email']

    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value).exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError('User wuth this email already exists.')
        return value.lower()
    

class AdminUserSerializer(serializers.ModelSerializer):
    role_code = serializers.CharField(source='role.code', read_only=True)
    password = serializers.CharField(min_length=8, write_only=True, required=False, allowed_blank=True)

    class Meta:
        model = Userfields = [
            'id',
            'first_name',
            "last_name",
            'middle_name',
            "email",
            "role",
            'role_code',
            'is_active',
            'password',
            'created_at',
            'update_at',
            'delete_at',

        ]
        read_only_fields = ["id", "full_name", "role_code", "created_at", "updated_at", "deleted_at"]
        
    def validate_email(self, value):
        qs = User.objects.filter(email__iexact=value)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError('User eith this email already exists.')
        return value.lower()
    
    def create(self, validate_data):
        password = validate_data.pop('password', None)
        if not password:
            raise serializers.ValidationError({'password': 'Password is required.'})
        validate_data['password_hash'] = hash_password(password)
        return User.objects.create(**validate_data)
    
    def update(self, instance, validate_data):
        password = validate_data.pop('password', None)
        for field, value in validate_data.items():
            setattr(instance, field, value)
        if password:
            instance.password_hash = hash_password(password)
        if instance.is_active:
            instance.deleted_at = None
        instance.save()
        return instance
    

class RevokedTokenSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = RevokedToken
        fields = ["id", "jti", "user", 'user_email', "revoked_at", "expires_at"]
        read_only_fields = fields
        

