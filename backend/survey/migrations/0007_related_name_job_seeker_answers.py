# Generated by Django 2.1 on 2018-11-28 05:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('survey', '0006_auto_20181026_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answerjobseeker',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_seeker_answers', to='survey.Answer'),
        ),
    ]
