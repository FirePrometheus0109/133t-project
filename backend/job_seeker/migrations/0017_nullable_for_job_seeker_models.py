# Generated by Django 2.1 on 2019-01-04 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_seeker', '0016_jobseeker_ban_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='certification',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='certification',
            name='licence_number',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='licence_number'),
        ),
        migrations.AlterField(
            model_name='certification',
            name='location',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='location'),
        ),
        migrations.AlterField(
            model_name='education',
            name='degree',
            field=models.CharField(blank=True, choices=[('HIGH_SCHOOL', 'High School'), ('ASSOCIATES_DEGREE', 'Associates Degree'), ('BACHELORS_DEGREE', "Bachelor's Degree"), ('MASTERS_DEGREE', "Master's Degree"), ('PHD', 'PHD')], max_length=40, null=True, verbose_name='education'),
        ),
        migrations.AlterField(
            model_name='education',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='education',
            name='location',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='location'),
        ),
        migrations.AlterField(
            model_name='jobexperience',
            name='employment',
            field=models.CharField(blank=True, choices=[('FULL_TIME', 'Full Time'), ('PART_TIME', 'Part Time')], max_length=16, null=True, verbose_name='employment'),
        ),
        migrations.AlterField(
            model_name='jobseeker',
            name='about',
            field=models.TextField(blank=True, max_length=2000, null=True, verbose_name='about'),
        ),
        migrations.AlterField(
            model_name='jobseeker',
            name='benefits',
            field=models.CharField(blank=True, choices=[('FULL_BENEFITS', 'Full Benefits'), ('PARTIAL_BENEFITS', 'Partial Benefits'), ('HEALTH', 'Health'), ('VISION', 'Vision'), ('HEALTH_AND_VISION', 'Health & Vision'), ('FOUR_OH_ONE_KEY', '401K')], max_length=40, null=True, verbose_name='benefits'),
        ),
        migrations.AlterField(
            model_name='jobseeker',
            name='clearance',
            field=models.CharField(blank=True, choices=[('SECRET', 'Secret'), ('TOP_SECRET', 'Top Secret'), ('TOP_SECRET_SCI', 'Top Secret/SCI'), ('MBI', 'MBI'), ('PUBLIC_TRUST', 'Public Trust'), ('CONFIDENTIAL', 'Confidential'), ('UNCLASSIFIED', 'Unclassified')], max_length=40, null=True, verbose_name='clearance'),
        ),
        migrations.AlterField(
            model_name='jobseeker',
            name='education',
            field=models.CharField(blank=True, choices=[('HIGH_SCHOOL', 'High School'), ('CERTIFICATION', 'Certification'), ('ASSOCIATES_DEGREE', 'Associates Degree'), ('BACHELORS_DEGREE', "Bachelor's Degree"), ('MASTERS_DEGREE', "Master's Degree"), ('PHD', 'PHD')], max_length=40, null=True, verbose_name='education'),
        ),
        migrations.AlterField(
            model_name='jobseeker',
            name='experience',
            field=models.CharField(blank=True, choices=[('NO_EXPERIENCE', 'No experience'), ('LESS_THAN_1', 'Less than 1 year'), ('FROM_1_TO_2', '1 to 2 years'), ('FROM_3_TO_5', '3 to 5 years'), ('FROM_5_TO_10', '5 to 10 years'), ('MORE_THAN_10', '10+ years')], max_length=40, null=True, verbose_name='experience'),
        ),
        migrations.AlterField(
            model_name='jobseeker',
            name='phone',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='phone'),
        ),
        migrations.AlterField(
            model_name='jobseeker',
            name='position_type',
            field=models.CharField(blank=True, choices=[('FULL_TIME', 'Full Time'), ('PART_TIME', 'Part Time'), ('CONTRACT', 'Contract'), ('TEMPORARY', 'Temporary'), ('INTERNSHIP', 'Internship'), ('COMMISSION', 'Commission')], max_length=40, null=True, verbose_name='position_type'),
        ),
        migrations.AlterField(
            model_name='jobseeker',
            name='travel',
            field=models.CharField(blank=True, choices=[('NO_TRAVEL', 'No Travel'), ('WILLING_TO_TRAVEL', 'Willing To Travel')], max_length=40, null=True, verbose_name='travel'),
        ),
    ]
