# Generated by Django 2.1 on 2019-01-15 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leet_auth', '0007_useractivity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deletionreason',
            name='text',
            field=models.TextField(blank=True, max_length=2000, null=True, verbose_name='text'),
        ),
    ]
