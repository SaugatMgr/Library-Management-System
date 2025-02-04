from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import CustomUserGroup, CustomUser, UserProfile, OTP


class CustomUserGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "get_permissions")
    search_fields = ("name",)
    filter_horizontal = ("permissions",)

    def get_permissions(self, obj):
        return ", ".join([p.name for p in obj.permissions.all()])

    get_permissions.short_description = "Permissions"


class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "first_name",
        "middle_name",
        "last_name",
        "is_active",
        "is_staff",
    )
    search_fields = ("email", "first_name", "last_name")
    list_filter = ("is_active", "is_staff", "groups")
    readonly_fields = ("get_full_name", "password")
    filter_horizontal = ("groups",)

    def get_full_name(self, obj):
        return obj.get_full_name

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ("get_full_name", "password")
        return ("get_full_name",)

    get_full_name.short_description = "Full Name"

    def save_model(self, request, obj, form, change):
        """Hash the password before saving if it's changed."""
        if not change or "password" in form.changed_data:
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "profile_picture",
        "library_card_number",
        "phone_number",
        "date_of_birth",
        "gender",
    )
    search_fields = ("user__email", "library_card_number")
    list_filter = ("gender", "date_of_birth")


class OTPAdmin(admin.ModelAdmin):
    list_display = ("user", "secret_key", "verified", "last_used")
    search_fields = ("user__email", "secret_key")
    list_filter = ("verified",)


admin.site.register(CustomUserGroup, CustomUserGroupAdmin)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(OTP, OTPAdmin)
