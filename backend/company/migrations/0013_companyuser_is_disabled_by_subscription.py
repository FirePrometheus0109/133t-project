# Generated by Django 2.1 on 2019-01-08 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0012_nullable_for_company_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyuser',
            name='is_disabled_by_subscription',
            field=models.BooleanField(default=False),
        ),
    ]
