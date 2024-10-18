from django.contrib.auth import models
from django.db import migrations

from leet import enums
from permission import constants
from permission import utils


def add_permissions(apps, schema_editor):
    perms = (
        utils.get_permission_object(
            apps,
            'candidate',
            'Candidate',
            constants.Permissions.export_candidate_csv.value),
    )
    company_user = models.Group.objects.get_by_natural_key(
        enums.AuthGroupsEnum.COMPANY_USER.value
    )
    company_user.permissions.add(*perms)


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0035_change_company_logo_permission'),
    ]

    operations = [
        migrations.RunPython(add_permissions)
    ]
