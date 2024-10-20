# Generated by Django 2.1 on 2019-01-31 06:46

from django.contrib.auth import models as auth_models
from django.db import migrations

from leet import enums
from notification_center import constants
from notification_center.migrations.data import constants as data


def create_notifications_types(type_model):
    job_seeker = auth_models.Group.objects.get_by_natural_key(
        enums.AuthGroupsEnum.JOB_SEEKER.value
    )
    type_model.objects.bulk_create(
        type_model(**i) for i in data.NOTIFICATIONS_JOB_SEEKER_TYPES_DATA)
    types = type_model.objects.values_list('id', flat=True)
    job_seeker.notificationtype_set.add(*types)


def create_notification_types_verbs(apps, schema_editor):
    NotificationType = apps.get_model(
        'notification_center', 'NotificationType')
    NotificationVerb = apps.get_model(
        'notification_center', 'NotificationVerb')
    create_notifications_types(NotificationType)
    types_for_verbs = NotificationType.objects.filter(
        format=constants.NOTIFICATION_FORMAT_WEB)
    types = {t.name: t for t in types_for_verbs}
    for i in data.NOTIFICATIONS_JOB_SEEKER_VERBS_DATA:
        i['type'] = types[i['type']]
        NotificationVerb.objects.create(**i)


class Migration(migrations.Migration):

    dependencies = [
        ('notification_center', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_notification_types_verbs)
    ]
