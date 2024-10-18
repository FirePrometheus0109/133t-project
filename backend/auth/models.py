from django.contrib.auth.models import User
from django.db import models


class ProxyUser(User):
    class Meta:
        proxy = True
        verbose_name = 'User'


class DeletionReason(models.Model):
    user = models.OneToOneField(
        'leet_auth.ProxyUser',
        on_delete=models.CASCADE,
        related_name='deletion_reason'
    )
    text = models.TextField(
        'text',
        max_length=2000,
        blank=True,
        null=True
    )


class UserActivity(models.Model):
    user = models.OneToOneField(
        'ProxyUser',
        on_delete=models.CASCADE,
        related_name='activity'
    )
    last_activity = models.DateTimeField()
