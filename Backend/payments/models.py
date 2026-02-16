from django.db import models
from django.conf import settings
from django.utils import timezone
from apps.groups.models import Group

# Create your models here.

# Models for recording settlements btwn users
class Payment(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name="payments")
    payer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payments_made")
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="payments_received")
    amount = models.DecimalField(max_digits=10, decimal_places=2, help_text="The amount of the payment")
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "payments"
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['group','-created_at']),
        ]

    def __str__(self):
        return f"{self.payer.name} paid {self.receiver.name} {self.amount}"