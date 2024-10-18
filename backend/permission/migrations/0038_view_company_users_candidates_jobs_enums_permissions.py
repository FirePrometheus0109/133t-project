# Generated by Django 2.1 on 2019-02-21 14:56

from django.contrib.auth import models
from django.db import migrations

from leet import enums
from permission import constants
from permission import utils


def add_permissions(apps, schema_editor):
    perms = (
        utils.get_permission_object(
            apps,
            'company',
            'CompanyUser',
            constants.Permissions.view_company_user_enum.value),
        utils.get_permission_object(
            apps,
            'job',
            'Job',
            constants.Permissions.view_job_enum.value),
        utils.get_permission_object(
            apps,
            'candidate',
            'Candidate',
            constants.Permissions.view_candidate_enum.value),
    )
    company_user = models.Group.objects.get_by_natural_key(
        enums.AuthGroupsEnum.COMPANY_USER.value
    )
    company_user.permissions.add(*perms)


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0037_share_job_permission'),
    ]

    operations = [
        migrations.RunPython(add_permissions)
    ]
