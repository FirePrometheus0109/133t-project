# Generated by Django 2.1 on 2019-01-28 10:47

from django.contrib.auth import models
from django.db import migrations

from permission import constants
from permission import utils


def add_permissions(apps, schema_editor):
    perms = (
        utils.get_permission_object(
            apps,
            'notification_center',
            'NotificationType',
            constants.Permissions.view_notificationtype.value),
        utils.get_permission_object(
            apps,
            'notification_center',
            'NotificationType',
            constants.Permissions.manage_notifications.value),
    )
    job_seeker = models.Group.objects.get_by_natural_key('job_seeker')
    job_seeker.permissions.add(*perms)


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0029_logs_permissions'),
        ('notification_center', '0001_initial')
    ]

    operations = [
        migrations.RunPython(add_permissions)
    ]
