from django.db import migrations
from django.contrib.auth import models

from leet import enums
from permission import utils
from permission import constants


def add_company_user_permissions(apps, schema_editor):
    perms = (
        utils.get_permission_object(
            apps,
            'job_seeker',
            'SavedJobSeeker',
            constants.Permissions.add_savedjobseeker.value),
    )
    company_user = models.Group.objects.get_by_natural_key(
        enums.AuthGroupsEnum.COMPANY_USER.value
    )
    company_user.permissions.add(*perms)
    company_user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0031_view_autoapply_stats_permissions'),
    ]

    operations = [
        migrations.RunPython(add_company_user_permissions)
    ]
