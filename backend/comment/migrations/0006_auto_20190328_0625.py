# Generated by Django 2.1 on 2019-03-28 06:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0005_viewcomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='viewcomment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comment_viewer', to='leet_auth.ProxyUser', verbose_name='User'),
        ),
    ]
