# Generated by Django 2.1 on 2019-02-08 09:55

from django.db import migrations


def fill_data(apps, schema_editor):
    model = apps.get_model('job_seeker', 'ViewJobSeeker')
    views = model.objects.all()
    for v in views:
        v.company_user = v.company.company_users.first()
        v.save()


class Migration(migrations.Migration):

    dependencies = [
        ('job_seeker', '0021_company_user_field_instead_company'),
    ]

    operations = [
        migrations.RunPython(fill_data)
    ]
