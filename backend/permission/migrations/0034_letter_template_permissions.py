# Generated by Django 2.1 on 2019-02-13 08:25

from django.contrib.auth import models
from django.db import migrations

from leet import enums
from permission import constants
from permission import utils


def add_permissions(apps, schema_editor):
    perms = (
        utils.get_permission_object(
            apps,
            'letter_template',
            'LetterTemplate',
            constants.Permissions.add_lettertemplate.value),
        utils.get_permission_object(
            apps,
            'letter_template',
            'LetterTemplate',
            constants.Permissions.change_lettertemplate.value),
        utils.get_permission_object(
            apps,
            'letter_template',
            'LetterTemplate',
            constants.Permissions.delete_lettertemplate.value),
    )
    letter_template_group = models.Group.objects.get_by_natural_key(
        constants.MANAGE_LETTER_TEMPLATE_GROUP
    )
    letter_template_group.permissions.add(*perms)
    perms = (
        utils.get_permission_object(
            apps,
            'letter_template',
            'LetterTemplate',
            constants.Permissions.view_lettertemplate.value),
    )
    company_user = models.Group.objects.get_by_natural_key(
        enums.AuthGroupsEnum.COMPANY_USER.value
    )
    company_user.permissions.add(*perms)


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0033_quicklist_permissions'),
    ]

    operations = [
        migrations.RunPython(add_permissions)
    ]
