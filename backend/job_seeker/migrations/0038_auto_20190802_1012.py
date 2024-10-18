# Generated by Django 2.1 on 2019-08-02 10:12

from django.db import migrations, models


def migrate_clearance(apps, schema_editor):
    JobSeeker = apps.get_model(
        'job_seeker', 'JobSeeker')
    clearance_mapping = dict(
        NO_CLEARANCE=0,
        UNCLASSIFIED=1,
        CONFIDENTIAL=2,
        MBI=3,
        PUBLIC_TRUST=4,
        SECRET=5,
        TOP_SECRET=6,
        TOP_SECRET_SCI=7
    )
    job_seekers_qs = JobSeeker.objects.all()
    for seeker in job_seekers_qs.iterator():
        # There is no bulk_update in Django 2.1
        old_clearance = getattr(seeker, 'clearance', 'NO_CLEARANCE')
        if not old_clearance:
            old_clearance = 'NO_CLEARANCE'
        seeker.clearance = clearance_mapping[old_clearance]
        seeker.save()


class Migration(migrations.Migration):

    dependencies = [
        ('job_seeker', '0037_auto_20190801_0800'),
    ]

    operations = [
        migrations.RunPython(migrate_clearance),
        migrations.AlterField(
            model_name='jobseeker',
            name='clearance',
            field=models.IntegerField(blank=True, choices=[(0, 'No Clearance'), (1, 'Unclassified'), (2, 'Confidential'), (3, 'MBI'), (4, 'Public Trust'), (5, 'Secret'), (6, 'Top Secret'), (7, 'Top Secret/SCI')], null=True, verbose_name='clearance'),
        ),
    ]
