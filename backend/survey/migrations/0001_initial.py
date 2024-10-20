# Generated by Django 2.1 on 2018-10-18 06:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('job_seeker', '0007_relation_name_job_seeker'),
        ('job', '0007_jobs_views'),
        ('company', '0002_companyadmin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('yes_no_value', models.CharField(blank=True, choices=[('YES', 'Yes'), ('NO', 'No')], max_length=8, verbose_name='yes_no_value')),
                ('plain_text_value', models.TextField(blank=True, verbose_name='plain_text_value')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AnswerJobSeeker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('answer_type', models.CharField(choices=[('YES_NO', 'Yes/No'), ('PLAIN_TEXT', 'Plain Text'), ('SIMPLE_CHOICE', 'Simple Choice'), ('MULTIPLE_CHOICE', 'Multiple Choice')], default='YES_NO', max_length=64, verbose_name='answer_type')),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Answer')),
                ('job', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='job.Job')),
                ('job_seeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='job_seeker.JobSeeker')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('body', models.CharField(max_length=256, verbose_name='body')),
                ('is_answer_required', models.BooleanField(default=False, verbose_name='is_answer_reqired')),
                ('answer_type', models.CharField(choices=[('YES_NO', 'Yes/No'), ('PLAIN_TEXT', 'Plain Text'), ('SIMPLE_CHOICE', 'Simple Choice'), ('MULTIPLE_CHOICE', 'Multiple Choice')], default='YES_NO', max_length=64, verbose_name='answer_type')),
                ('disqualifying_answer', models.CharField(blank=True, max_length=256, verbose_name='disqualifying_answer')),
                ('is_default', models.BooleanField(default=False, verbose_name='is_default')),
                ('company', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='saved_questions', to='company.Company')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=256, verbose_name='title')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='surveys', to='company.Company')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='surveys',
            field=models.ManyToManyField(blank=True, related_name='questions', to='survey.Survey'),
        ),
        migrations.AddField(
            model_name='answerjobseeker',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='survey.Question'),
        ),
        migrations.AlterUniqueTogether(
            name='survey',
            unique_together={('title', 'company')},
        ),
    ]
