from django.urls import path
from rest_framework.routers import DefaultRouter
from accounts.views import AdminUserViewSet, LoginView, LogoutView, ProfileView, RegisterView, RevokedTokenViewSet


router = DefaultRouter()
router.register("admin/users", AdminUserViewSet)
router.register("admin/revoked-tokens", RevokedTokenViewSet)


urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/", ProfileView.as_view(), name="profile"),
] + router.urls
