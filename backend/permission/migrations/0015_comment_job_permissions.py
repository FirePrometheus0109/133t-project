from django.db import migrations

from permission import utils
from permission import constants
from permission import models


def add_company_user_permissions(apps, schema_editor):
    perms = (
        utils.get_permission_object(
            apps,
            'comment',
            'JobComment',
            constants.Permissions.add_jobcomment.value),
        utils.get_permission_object(
            apps,
            'comment',
            'JobComment',
            constants.Permissions.view_jobcomment.value),
        utils.get_permission_object(
            apps,
            'comment',
            'JobComment',
            constants.Permissions.change_jobcomment.value),
        utils.get_permission_object(
            apps,
            'comment',
            'JobComment',
            constants.Permissions.delete_jobcomment.value),
    )
    group = models.PermissionGroup.objects.get_by_natural_key(
        constants.MANAGE_JOB_COMMENTS_GROUP)
    group.permissions.clear()
    group.permissions.add(*perms)
    group.save()


def add_company_user_permissions_2(apps, schema_editor):
    perms = (
        utils.get_permission_object(
            apps,
            'comment',
            'JobComment',
            constants.Permissions.add_jobcomment.value),
        utils.get_permission_object(
            apps,
            'comment',
            'JobComment',
            constants.Permissions.view_jobcomment.value),
    )
    group = models.PermissionGroup.objects.get_by_natural_key(
        constants.VIEW_CREATE_JOB_COMMENTS_GROUP)
    group.permissions.clear()
    group.permissions.add(*perms)
    group.save()


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0014_rate_candidate_permissions'),
    ]

    operations = [
        migrations.RunPython(add_company_user_permissions),
        migrations.RunPython(add_company_user_permissions_2)
    ]
