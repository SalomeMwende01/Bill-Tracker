from django.db import models
from django.utils import timezone
from config import settings


# Create your models here.

# Group Model
class Group(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="created_groups",
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'groups'
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        ordering = ('-created_at',)

    def __str__(self):
        return self.name

# Tracking model membership
class GroupMember(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="group_memberships",
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="members"
    )
    joined_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'group_members'
        verbose_name = 'Group Member'
        verbose_name_plural = 'Group Members'
        unique_together = (('user', 'group'),)
        ordering = ('joined_at',)

        def __str__(self):
            return f"{self.user.name} in {self.group.name}"
