# Generated by Django 2.1 on 2018-09-24 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job_seeker', '0002_jobseeker_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobExperience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('company', models.CharField(max_length=256, verbose_name='company')),
                ('job_title', models.CharField(max_length=256, verbose_name='job_title')),
                ('date_from', models.DateTimeField()),
                ('date_to', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('is_current', models.BooleanField(default=False)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_experience', to='job_seeker.JobSeeker')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
