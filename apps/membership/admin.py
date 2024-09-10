from django.contrib import admin
from .models import MembershipPlan, Membership, Payment


class MembershipPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "plan_type", "price", "duration_in_days")
    search_fields = ("name",)
    list_filter = ("plan_type",)


class MembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "start_date", "end_date")
    search_fields = ("user__first_name", "user__last_name", "plan__name")
    list_filter = ("plan", "start_date", "end_date")
    readonly_fields = ("start_date", "end_date")


class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "plan",
        "amount",
        "payment_method",
        "transaction_id",
        "status",
    )
    search_fields = (
        "user__first_name",
        "user__last_name",
        "plan__name",
        "transaction_id",
    )
    list_filter = ("payment_method", "status", "plan")


admin.site.register(MembershipPlan, MembershipPlanAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(Payment, PaymentAdmin)
