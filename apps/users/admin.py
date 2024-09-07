from django.contrib import admin

from .models import CustomUser, CustomUserGroup, UserProfile, OTP

admin.site.register(CustomUser)
admin.site.register(CustomUserGroup)
admin.site.register(UserProfile)
admin.site.register(OTP)
