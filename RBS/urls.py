from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("business.urls")),
    path("api/auth/", include("accounts.urls")),
    path("api/access/", include("access_control.urls")),
    path("admin/", admin.site.urls),
]