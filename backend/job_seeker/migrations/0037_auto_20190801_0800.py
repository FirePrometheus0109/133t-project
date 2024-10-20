# Generated by Django 2.1 on 2019-08-01 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_seeker', '0036_auto_20190715_0816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='degree',
            field=models.CharField(blank=True, choices=[('HIGH_SCHOOL', 'High School'), ('ASSOCIATES_DEGREE', 'Associates Degree'), ('BACHELORS_DEGREE', "Bachelor's Degree"), ('MASTERS_DEGREE', "Master's Degree"), ('PHD', 'PHD'), ('NO_EDUCATION', 'No Education')], max_length=40, null=True, verbose_name='education'),
        ),
        migrations.AlterField(
            model_name='jobseeker',
            name='benefits',
            field=models.CharField(blank=True, choices=[('FULL_BENEFITS', 'Full Benefits'), ('PARTIAL_BENEFITS', 'Partial Benefits'), ('HEALTH', 'Health'), ('VISION', 'Vision'), ('HEALTH_AND_VISION', 'Health & Vision'), ('FOUR_OH_ONE_KEY', '401K'), ('NO_BENEFITS', 'No Benefits')], max_length=40, null=True, verbose_name='benefits'),
        ),
        migrations.AlterField(
            model_name='jobseeker',
            name='clearance',
            field=models.CharField(blank=True, choices=[('SECRET', 'Secret'), ('TOP_SECRET', 'Top Secret'), ('TOP_SECRET_SCI', 'Top Secret/SCI'), ('MBI', 'MBI'), ('PUBLIC_TRUST', 'Public Trust'), ('CONFIDENTIAL', 'Confidential'), ('UNCLASSIFIED', 'Unclassified'), ('NO_CLEARANCE', 'No Clearance')], max_length=40, null=True, verbose_name='clearance'),
        ),
        migrations.AlterField(
            model_name='jobseeker',
            name='education',
            field=models.CharField(blank=True, choices=[('HIGH_SCHOOL', 'High School'), ('CERTIFICATION', 'Certification'), ('ASSOCIATES_DEGREE', 'Associates Degree'), ('BACHELORS_DEGREE', "Bachelor's Degree"), ('MASTERS_DEGREE', "Master's Degree"), ('PHD', 'PHD'), ('NO_EDUCATION', 'No Education')], max_length=40, null=True, verbose_name='education'),
        ),
    ]
