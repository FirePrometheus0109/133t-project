# Generated by Django 2.1 on 2018-09-20 07:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Industry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='name')),
            ],
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('description', models.CharField(blank=True, max_length=1024, verbose_name='description')),
                ('location', models.CharField(max_length=255, verbose_name='location')),
                ('position_type', models.CharField(blank=True, choices=[('FULL_TIME', 'Full Time'), ('PART_TIME', 'Part Time'), ('CONTRACT', 'Contract'), ('TEMPORARY', 'Temporary'), ('INTERNSHIP', 'Internship'), ('COMMISSION', 'Commission')], max_length=40, verbose_name='position_type')),
                ('education', models.CharField(blank=True, choices=[('HIGH_SCHOOL', 'High School'), ('CERTIFICATION', 'Certification'), ('ASSOCIATES_DEGREE', 'Associates Degree'), ('BACHELORS_DEGREE', "Bachelor's Degree"), ('MASTERS_DEGREE', "Master's Degree"), ('PHD', 'PHD')], max_length=40, verbose_name='education')),
                ('clearance', models.CharField(blank=True, choices=[('SECRET', 'Secret'), ('TOP_SECRET', 'Top Secret'), ('TOP_SECRET_SCI', 'Top Secret/SCI'), ('MBI', 'MBI'), ('PUBLIC_TRUST', 'Public Trust'), ('CONFIDENTIAL', 'Confidential'), ('UNCLASSIFIED', 'Unclassified')], max_length=40, verbose_name='clearance')),
                ('experience', models.CharField(blank=True, choices=[('NO_EXPERIENCE', 'No experience'), ('LESS_THAN_1', 'Less than 1 year'), ('FROM_1_TO_2', '1 to 2 years'), ('FROM_3_TO_5', '3 to 5 years'), ('FROM_5_TO_10', '5 to 10 years'), ('MORE_THAN_10', '10+ years')], max_length=40, verbose_name='experience')),
                ('salary_min', models.IntegerField(blank=True, null=True, verbose_name='salary_min')),
                ('salary_max', models.IntegerField(blank=True, null=True, verbose_name='salary_max')),
                ('salary_negotiable', models.BooleanField(default=False, verbose_name='salary_negotiable')),
                ('benefits', models.CharField(blank=True, choices=[('FULL_BENEFITS', 'Full Benefits'), ('PARTIAL_BENEFITS', 'Partial Benefits'), ('HEALTH', 'Health'), ('VISION', 'Vision'), ('HEALTH_AND_VISION', 'Health & Vision'), ('FOUR_OH_ONE_KEY', '401K')], max_length=40, verbose_name='benefits')),
                ('travel', models.CharField(blank=True, choices=[('REQUIRED', 'Required'), ('NOT_REQUIRED', 'Not Required')], max_length=40, verbose_name='travel')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', related_query_name='job', to='company.Company')),
                ('industry', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='job.Industry')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='JobSkill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_required', models.BooleanField(default=False, verbose_name='is_required')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_skill_set', to='job.Job')),
            ],
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True, verbose_name='name')),
                ('description', models.TextField(verbose_name='description', blank=True))
            ],
        ),
        migrations.CreateModel(
            name='Subindustry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('industry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subindustries', related_query_name='subindustry', to='job.Industry')),
            ],
        ),
        migrations.AddField(
            model_name='skill',
            name='subindustries',
            field=models.ManyToManyField(related_name='skills', related_query_name='skill', to='job.Subindustry', verbose_name='subindustries'),
        ),
        migrations.AddField(
            model_name='jobskill',
            name='skill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job.Skill'),
        ),
        migrations.AddField(
            model_name='job',
            name='subindustry',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='job.Subindustry'),
        ),
        migrations.AlterUniqueTogether(
            name='subindustry',
            unique_together={('name', 'industry')},
        ),
        migrations.AlterUniqueTogether(
            name='jobskill',
            unique_together={('job', 'skill')},
        ),
    ]
