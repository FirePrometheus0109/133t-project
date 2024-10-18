from django.db import migrations
from django.contrib.auth import models

from permission import constants
from permission import utils


def add_permissions(apps, schema_editor):
    perm = utils.get_permission_object(
        apps,
        'job',
        'Job',
        constants.Permissions.export_job_csv.value
    )
    company_admin = models.Group.objects.get(name='company_admin')
    company_admin.permissions.add(perm)


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0007_job_seeker_company_user_permission'),
    ]

    operations = [
        migrations.RunPython(add_permissions)
    ]
