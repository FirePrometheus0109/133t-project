# Generated by Django 2.1 on 2018-12-10 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0003_verbose_name_for_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobcomment',
            name='ban_status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('BANNED', 'Banned')], default='ACTIVE', max_length=16, verbose_name='ban_status'),
        ),
        migrations.AddField(
            model_name='jobseekercomment',
            name='ban_status',
            field=models.CharField(choices=[('ACTIVE', 'Active'), ('BANNED', 'Banned')], default='ACTIVE', max_length=16, verbose_name='ban_status'),
        ),
    ]
