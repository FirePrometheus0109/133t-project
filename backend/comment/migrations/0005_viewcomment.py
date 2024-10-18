# Generated by Django 2.1 on 2019-01-03 07:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('leet_auth', '0005_verbose_name_user'),
        ('contenttypes', '0002_remove_content_type_name'),
        ('comment', '0004_auto_20181210_0951'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True)),
                ('object_pk', models.TextField(verbose_name='object ID')),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType', verbose_name='content type')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='comment_viewer', to='leet_auth.ProxyUser', verbose_name='User')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
