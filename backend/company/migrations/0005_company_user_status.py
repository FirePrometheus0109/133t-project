# Generated by Django 2.1 on 2018-11-07 19:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_auto_20181031_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyadmin',
            name='status',
            field=models.CharField(choices=[('NEW', 'New'), ('ACTIVE', 'Active'), ('DISABLED', 'Disabled')], default='NEW', max_length=16, verbose_name='status'),
        ),
    ]
