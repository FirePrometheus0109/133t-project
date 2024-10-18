from django.db import migrations

from permission import utils
from permission import constants
from permission import models


def add_permissions(apps, schema_editor):
    perms = (
        utils.get_permission_object(
            apps,
            'candidate',
            'Candidate',
            ('change_candidate_status', 'Can change candidate status')),
    )
    group = models.PermissionGroup.objects.get_by_natural_key(
        constants.MANAGE_JOB_POSTINGS_GROUP)
    group.permissions.add(*perms)
    group.save()


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0015_comment_job_permissions'),
    ]

    operations = [
        migrations.RunPython(add_permissions)
    ]
