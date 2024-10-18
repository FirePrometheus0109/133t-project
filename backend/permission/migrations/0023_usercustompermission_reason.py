# Generated by Django 2.1 on 2019-01-08 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('permission', '0022_job_posting_attribute_perms'),
    ]

    operations = [
        migrations.AddField(
            model_name='usercustompermission',
            name='reason',
            field=models.CharField(blank=True, choices=[('SUBSCRIPTION_LIMIT', 'Subscription limit')], max_length=40, null=True, verbose_name='reason'),
        ),
    ]
