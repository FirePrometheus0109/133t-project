# Generated by Django 2.1 on 2019-08-29 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_seeker', '0038_auto_20190802_1012'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobseeker',
            name='clearance',
            field=models.IntegerField(blank=True, choices=[(0, 'No Clearance'), (1, 'Unclassified'), (2, 'Confidential'), (3, 'MBI'), (4, 'Public Trust'), (5, 'Secret'), (6, 'Top Secret'), (7, 'Top Secret/SCI')], default=0, null=True, verbose_name='clearance'),
        ),
    ]
