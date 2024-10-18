# Generated by Django 2.1 on 2019-01-10 10:28

from django.db import migrations
from django.contrib.auth import models

from leet import enums
from permission import constants
from permission import utils


def add_permissions(apps, schema_editor):
    perm = utils.get_permission_object(
        apps,
        'candidate',
        'Candidate',
        constants.Permissions.view_workflowstep_stats.value
    )
    company_user = models.Group.objects.get_by_natural_key(
        enums.AuthGroupsEnum.COMPANY_USER.value
    )
    company_user.permissions.add(perm)


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0024_view_view_jobseeker'),
    ]

    operations = [
        migrations.RunPython(add_permissions)
    ]
