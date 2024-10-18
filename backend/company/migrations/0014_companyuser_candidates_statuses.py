# Generated by Django 2.1 on 2019-01-15 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leet', '0005_drop_null'),
        ('company', '0013_companyuser_is_disabled_by_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyuser',
            name='candidate_statuses',
            field=models.ManyToManyField(to='leet.CandidateStatus'),
        ),
    ]
