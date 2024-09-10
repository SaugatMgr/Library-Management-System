from django.contrib import admin
from .models import DigitalResource


class DigitalResourceAdmin(admin.ModelAdmin):
    list_display = ("title", "resource_type", "description")
    search_fields = ("title",)
    filter_horizontal = ("related_books",)
    list_filter = ("resource_type",)


admin.site.register(DigitalResource, DigitalResourceAdmin)
