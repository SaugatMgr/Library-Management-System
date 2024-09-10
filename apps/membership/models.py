from datetime import timedelta
from django.utils.timezone import now
from django.db import models
from django.contrib.auth import get_user_model

from utils.constants import MemberShipPlanChoices
from utils.models import CommonInfo

User = get_user_model()


class MembershipPlan(CommonInfo):
    name = models.CharField(max_length=50)
    plan_type = models.CharField(max_length=10, choices=MemberShipPlanChoices.choices)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration_in_days = models.PositiveIntegerField(
        help_text="Duration of the plan in days"
    )

    def __str__(self) -> str:
        return f"{self.name} - {self.plan_type}"


class Membership(CommonInfo):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(MembershipPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    def save(self, *args, **kwargs) -> None:
        if not self.end_date:
            self.end_date = now() + timedelta(days=self.plan.duration_in_days)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return f"{self.user.get_full_name} - {self.plan.name}"
