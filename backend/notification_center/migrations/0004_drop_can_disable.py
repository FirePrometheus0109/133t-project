# Generated by Django 2.1 on 2019-02-07 14:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notification_center', '0003_notifications_company_user_verbs_types_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificationtype',
            name='can_disable',
        ),
    ]
