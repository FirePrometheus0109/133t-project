# Generated by Django 2.1 on 2018-11-08 17:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_company_user_status'),
    ]

    operations = [
        migrations.RenameModel('CompanyAdmin', 'CompanyUser')
    ]

    atomic = False
