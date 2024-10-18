from django.conf import settings
from django.contrib.auth import models as auth_models
from django.db import models

from leet import enums


class PermissionGroup(auth_models.Group):
    """
    Extended default django model 'Group'.
    Is is allow to use default groups permissions engine.
    """

    title = models.CharField(
        'name',
        max_length=128
    )
    description = models.TextField('description')


class UserCustomPermission(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='custom_permissions'
    )
    action = models.CharField(
        'action',
        max_length=8,
        choices=enums.ActionEnum.choices
    )
    permission = models.ForeignKey(
        auth_models.Permission,
        on_delete=models.CASCADE
    )
    reason = models.CharField(
        'reason',
        max_length=40,
        choices=enums.CustomPermissionReasonEnum.choices,
        blank=True,
        null=True
    )
