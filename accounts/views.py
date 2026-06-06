from datetime import datetime, timezone as datetime_timezone

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

from access_control.services import assert_can_access
from accounts.models import RevokedToken, User
from accounts.serializers import (
    AdminUserSerializer,
    LoginSerializer,
    ProfileUpdateSerializer,
    RegisterSerializer,
    RevokedTokenSerializer,
    UserSerializer,
)
from accounts.token import create_access_token


class RegisterView(APIView):
    authentication_classes = []

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, payload = create_access_token(user)
        return Response(
            {
                "access_token": token,
                "token_type": "Bearer",
                "expires_at": payload["exp"],
                "user": UserSerializer(user).data,
            }
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        payload = request.auth_payload
        expires_at = datetime.fromtimestamp(payload["exp"], tz=datetime_timezone.utc)
        RevokedToken.objects.get_or_create(
            jti=payload["jti"],
            defaults={"user": request.user, "expires_at": expires_at},
        )
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

    def patch(self, request):
        serializer = ProfileUpdateSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(UserSerializer(request.user).data)

    def delete(self, request):
        payload = request.auth_payload
        expires_at = datetime.fromtimestamp(payload["exp"], tz=datetime_timezone.utc)
        RevokedToken.objects.get_or_create(
            jti=payload["jti"],
            defaults={"user": request.user, "expires_at": expires_at},
        )
        request.user.soft_delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.select_related("role").all()
    serializer_class = AdminUserSerializer
    permission_classes = [IsAuthenticated]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        assert_can_access(request.user, "access_rules", "read")

    def perform_create(self, serializer):
        assert_can_access(self.request.user, "access_rules", "create")
        serializer.save()

    def perform_update(self, serializer):
        assert_can_access(self.request.user, "access_rules", "update")
        serializer.save()

    def perform_destroy(self, instance):
        assert_can_access(self.request.user, "access_rules", "delete")
        instance.soft_delete()


class RevokedTokenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = RevokedToken.objects.select_related("user").all()
    serializer_class = RevokedTokenSerializer
    permission_classes = [IsAuthenticated]

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        assert_can_access(request.user, "access_rules", "read")
