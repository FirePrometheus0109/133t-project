# Generated by Django 2.1 on 2018-12-10 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0010_company_is_trial_available'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='ban_status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('BANNED', 'Banned')], default='ACTIVE', max_length=16, verbose_name='ban_status'),
        ),
        migrations.AddField(
            model_name='companyuser',
            name='ban_status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('BANNED', 'Banned')], default='ACTIVE', max_length=16, verbose_name='ban_status'),
        ),
    ]
