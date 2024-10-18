# Generated by Django 2.1 on 2019-09-24 09:32

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0019_plan_is_reporting_enabled'),
    ]

    operations = [
        migrations.AddField(
            model_name='plan',
            name='users_number',
            field=models.SmallIntegerField(default=1, validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)]),
        ),
    ]
