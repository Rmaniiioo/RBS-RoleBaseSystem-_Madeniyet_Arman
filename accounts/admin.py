from django.contrib import admin
from .models import User, RevokedToken

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "is_active",
    )

    search_fields = (
        'email',
        "first_name",
        "last_name",
    )

    list_filter = (
        "is_active",
    )

@admin.register(RevokedToken)
class RevokedTokenAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "revoked_at",
        "expires_at",
    )