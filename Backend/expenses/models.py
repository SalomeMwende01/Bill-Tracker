from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.groups.models import Group
# Create your models here.


# Model for tracking shared espenses
class Expense(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="expenses")
    paid_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="paid_expenses")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount of expenses paid for this expense")
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "expenses"
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['group', "created_at"]),
        ]

    def __str__(self):
        return f"{self.description} - {self.amount}"


# Model for tracking how an expense is split among users
class Split(models.Model):
    expense = models.ForeignKey(Expense, on_delete=models.CASCADE, related_name="splits")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="expense_splits")
    amount_owed = models.DecimalField(max_digits=10, decimal_places=2, help_text="Amount of expenses owed")

    class Meta:
        db_table = "splits"
        verbose_name = "Split"
        verbose_name_plural = "Splits"
        unique_together = ['expense', 'user']

    def __str__(self):
        return f"{self.user.name} owes {self.amount_owed} for {self.expense.description}"
