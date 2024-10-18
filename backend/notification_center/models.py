from django.conf import settings
from django.contrib.auth import models as auth_models
from django.db import models


class NotificationType(models.Model):

    name = models.CharField(max_length=128)
    format = models.CharField(max_length=16)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name='subscribed_notifications'
    )
    groups = models.ManyToManyField(
        auth_models.Group,
    )


class NotificationVerb(models.Model):
    """
    A Notification library use field 'verb' for short describing
    action that was implemented. Bind Notification model in library with
    subscribed user notifications through field 'verb'.
    NOTE: notificationverb should refer only to NotificationType with
    format '133T Web'.
    """

    name = models.CharField(max_length=255)
    type = models.ForeignKey(
        NotificationType,
        on_delete=models.CASCADE,
        related_name='verbs'
    )
