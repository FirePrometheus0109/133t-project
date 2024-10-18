from django.contrib.auth import models
from django.db import migrations

from permission import utils
from permission import constants


def add_permissions(apps, schema_editor):
    perm = (
        utils.get_permission_object(
            apps,
            'job_seeker',
            'ViewJobSeeker',
            constants.Permissions.view_viewjobseeker.value)
    )
    job_seeker = models.Group.objects.get_by_natural_key('job_seeker')
    job_seeker.permissions.add(perm)


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0023_usercustompermission_reason'),
    ]

    operations = [
        migrations.RunPython(add_permissions)
    ]
