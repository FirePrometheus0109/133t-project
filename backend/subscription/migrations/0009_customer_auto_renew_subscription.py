# Generated by Django 2.1 on 2018-12-28 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0008_auto_20181227_1447'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='auto_renew_subscription',
            field=models.BooleanField(default=False, verbose_name='auto_renew_subscription'),
        ),
    ]
