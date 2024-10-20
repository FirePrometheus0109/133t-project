# Generated by Django 2.1 on 2018-12-12 13:40

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='date_start',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date_start'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscription',
            name='is_auto_renew',
            field=models.BooleanField(default=False, verbose_name='is_auto_renew'),
        ),
    ]
