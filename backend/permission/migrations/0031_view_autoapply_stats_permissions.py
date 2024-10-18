# Generated by Django 2.1 on 2019-02-04 12:28

from django.contrib.auth import models
from django.db import migrations

from leet import enums
from permission import constants
from permission import utils


def add_permissions(apps, schema_editor):
    perms = (
        utils.get_permission_object(
            apps,
            'apply',
            'Autoapply',
            constants.Permissions.view_autoapply_stats.value),
    )
    job_seeker = models.Group.objects.get_by_natural_key(
        enums.AuthGroupsEnum.JOB_SEEKER.value
    )
    job_seeker.permissions.add(*perms)


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0030_notification_center_permissions'),
    ]

    operations = [
        migrations.RunPython(add_permissions)
    ]
