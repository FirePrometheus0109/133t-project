from django.db import migrations

from permission import utils
from permission import constants
from permission import models


def add_company_user_permissions(apps, schema_editor):
    perms = (
        utils.get_permission_object(
            apps,
            'comment',
            'JobSeekerComment',
            constants.Permissions.add_jobseekercomment.value),
        utils.get_permission_object(
            apps,
            'comment',
            'JobSeekerComment',
            constants.Permissions.view_jobseekercomment.value),
        utils.get_permission_object(
            apps,
            'comment',
            'JobSeekerComment',
            constants.Permissions.change_jobseekercomment.value),
        utils.get_permission_object(
            apps,
            'comment',
            'JobSeekerComment',
            constants.Permissions.delete_jobseekercomment.value),
    )
    group = models.PermissionGroup.objects.get_by_natural_key(
        constants.MANAGE_CANDIDATE_COMMENTS_GROUP)
    group.permissions.clear()
    group.permissions.add(*perms)
    group.save()


def add_company_user_permissions_2(apps, schema_editor):
    perms = (
        utils.get_permission_object(
            apps,
            'comment',
            'JobSeekerComment',
            constants.Permissions.add_jobseekercomment.value),
        utils.get_permission_object(
            apps,
            'comment',
            'JobSeekerComment',
            constants.Permissions.view_jobseekercomment.value),
    )
    group = models.PermissionGroup.objects.get_by_natural_key(
        constants.VIEW_CREATE_CANDIDATE_COMMENTS_GROUP)
    group.permissions.clear()
    group.permissions.add(*perms)
    group.save()


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0011_view_purchased_job_seekers'),
    ]

    operations = [
        migrations.RunPython(add_company_user_permissions),
        migrations.RunPython(add_company_user_permissions_2)
    ]
