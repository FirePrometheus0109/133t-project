# Generated by Django 2.1 on 2019-02-12 16:50

from django.contrib.auth import models as auth_models
from django.db import migrations

from leet import enums
from notification_center import constants

NOTIFICATION_COMPANY_USER_VERBS_DATA = (
    {
        'name': constants.NOTIFICATION_VERB_PACKAGE_WILL_DELETED,
        'type': constants.NOTIFICATION_TYPE_PACKAGE_DELETION
    },
    {
        'name': constants.NOTIFICATION_VERB_PACKAGE_WAS_DELETED,
        'type': constants.NOTIFICATION_TYPE_PACKAGE_DELETION
    },
)


def create_notifications_types(type_model):
    formats = (constants.NOTIFICATION_FORMAT_EMAIL,
               constants.NOTIFICATION_FORMAT_WEB)
    types = []
    for notif_format in formats:
        type_, _ = type_model.objects.get_or_create(
            format=notif_format,
            name=constants.NOTIFICATION_TYPE_PACKAGE_DELETION
        )
        types.append(type_)
    company_user = auth_models.Group.objects.get_by_natural_key(
        enums.AuthGroupsEnum.COMPANY_USER.value
    )
    types_ids = [t.id for t in types]
    company_user.notificationtype_set.add(*types_ids)
    return types


def create_notification_types_verbs(apps, schema_editor):
    NotificationType = apps.get_model(
        'notification_center', 'NotificationType')
    NotificationVerb = apps.get_model(
        'notification_center', 'NotificationVerb')
    types = create_notifications_types(NotificationType)
    types = {t.name: t for t in types}
    for i in NOTIFICATION_COMPANY_USER_VERBS_DATA:
        i['type'] = types[i['type']]
        NotificationVerb.objects.get_or_create(**i)


class Migration(migrations.Migration):

    dependencies = [
        ('notification_center', '0004_drop_can_disable'),
    ]

    operations = [
        migrations.RunPython(create_notification_types_verbs)
    ]
