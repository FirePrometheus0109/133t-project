# Generated by Django 2.1 on 2018-11-12 11:49

from django.db import migrations

from django.contrib.auth import models

from permission import constants
from permission import utils


def add_cover_letter_permissions(apps, schema_editor):
    js_perms = (
        utils.get_permission_object(
            apps,
            'job_seeker',
            'CoverLetter',
            constants.Permissions.view_coverletter.value),
        utils.get_permission_object(
            apps,
            'job_seeker',
            'CoverLetter',
            constants.Permissions.add_coverletter.value),
        utils.get_permission_object(
            apps,
            'job_seeker',
            'CoverLetter',
            constants.Permissions.change_coverletter.value),
        utils.get_permission_object(
            apps,
            'job_seeker',
            'CoverLetter',
            constants.Permissions.delete_coverletter.value),
    )
    cu_perms = (
        utils.get_permission_object(
            apps,
            'job_seeker',
            'CoverLetter',
            constants.Permissions.view_coverletter.value),
    )
    job_seeker = models.Group.objects.get(name='job_seeker')
    job_seeker.permissions.add(*js_perms)
    company_user = models.Group.objects.get(name='company_user')
    company_user.permissions.add(*cu_perms)


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0009_company_user_permissions_instead_company_admin'),
        ('job_seeker', '0013_add_cover_letter'),
    ]

    operations = [
        migrations.RunPython(add_cover_letter_permissions)
    ]
