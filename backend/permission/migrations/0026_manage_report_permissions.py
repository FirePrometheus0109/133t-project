from django.db import migrations

from permission import utils
from permission import constants
from permission import models


def add_company_user_permissions(apps, schema_editor):
    perms = (
        utils.get_permission_object(
            apps,
            'company',
            'CompanyUser',
            constants.Permissions.add_report.value),
        utils.get_permission_object(
            apps,
            'company',
            'CompanyUser',
            constants.Permissions.change_report.value),
        utils.get_permission_object(
            apps,
            'company',
            'CompanyUser',
            constants.Permissions.view_report.value),
        utils.get_permission_object(
            apps,
            'company',
            'CompanyUser',
            constants.Permissions.delete_report.value),
    )
    group = models.PermissionGroup.objects.get_by_natural_key(
        constants.MANAGE_REPORTS_GROUP)
    group.permissions.clear()
    group.permissions.add(*perms)
    group.save()


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0025_workflow_steps_stats_permissions'),
    ]

    operations = [
        migrations.RunPython(add_company_user_permissions)
    ]