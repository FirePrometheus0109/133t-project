# Generated by Django 2.1 on 2018-11-15 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('job_seeker', '0013_add_cover_letter'),
        ('job', '0010_job_is_cover_letter_required'),
    ]

    operations = [
        migrations.CreateModel(
            name='Candidate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='candidates', to='job.Job')),
                ('job_seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='job_seeker.JobSeeker')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='candidate',
            unique_together={('job_seeker', 'job')},
        ),
    ]
