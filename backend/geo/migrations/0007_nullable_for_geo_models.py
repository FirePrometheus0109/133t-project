# Generated by Django 2.1 on 2019-01-04 06:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0006_auto_20181217_1502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='address'),
        ),
    ]
