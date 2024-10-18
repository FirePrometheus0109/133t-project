# Generated by Django 2.1 on 2018-11-15 04:56

from django.db import migrations
from django.contrib.auth import models as auth_models

from permission import utils
from permission import constants
from permission import models


def add_permissions(apps, schema_editor):
    perms = (
        utils.get_permission_object(
            apps,
            'candidate',
            'Candidate',
            constants.Permissions.add_candidate.value),
        utils.get_permission_object(
            apps,
            'candidate',
            'Candidate',
            constants.Permissions.change_candidate.value),
        utils.get_permission_object(
            apps,
            'candidate',
            'Candidate',
            constants.Permissions.delete_candidate.value),
    )
    group = models.PermissionGroup.objects.get_by_natural_key(
        constants.MANAGE_JOB_POSTINGS_GROUP)
    group.permissions.add(*perms)
    group.save()

    perm = utils.get_permission_object(
            apps,
            'candidate',
            'Candidate',
            constants.Permissions.view_candidate.value)
    company_user = auth_models.Group.objects.get(name='company_user')
    company_user.permissions.add(perm)
    company_user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0012_comment_job_seeker_profile_permissions'),
    ]

    operations = [
        migrations.RunPython(add_permissions)
    ]
