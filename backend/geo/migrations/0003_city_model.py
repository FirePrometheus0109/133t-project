# Generated by Django 2.1 on 2018-11-21 12:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0002_create_countries_and_states'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='city',
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('zips', models.TextField(verbose_name='zips')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cities', related_query_name='city', to='geo.State')),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='geo.City'),
        ),
        migrations.AlterUniqueTogether(
            name='city',
            unique_together={('name', 'state')},
        ),
    ]
