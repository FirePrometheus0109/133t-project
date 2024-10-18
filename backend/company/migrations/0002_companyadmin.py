# Generated by Django 2.1 on 2018-09-20 11:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leet_auth', '0002_create_user_groups'),
        ('company', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyAdmin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_admin_set', related_query_name='company_admin', to='company.Company')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='company_admin', to='leet_auth.ProxyUser')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
