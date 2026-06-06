from django.urls import include, path
from rest_framework.routers import DefaultRouter

from access_control.views import AccessRoleRuleViewSet, BusinessElementViewSet, RoleViewSet


router = DefaultRouter()
router.register("roles", RoleViewSet)
router.register("elements", BusinessElementViewSet)
router.register("rules", AccessRoleRuleViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
