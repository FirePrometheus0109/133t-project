# Generated by Django 2.1 on 2019-03-12 06:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('letter_template', '0003_drop_letter_template_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lettertemplate',
            name='event_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='leet.EventType'),
        ),
    ]
