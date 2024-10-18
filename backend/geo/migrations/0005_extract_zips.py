# Generated by Django 2.1 on 2018-11-27 13:39

import django.db.models.deletion
from django.db import migrations, models


def move_zips_to_separate_table(apps, schema_editor):
    Zip = apps.get_model('geo', 'Zip')
    City = apps.get_model('geo', 'City')
    cities = City.objects.all()
    zip_data = []
    for city in cities:
        zips = city.zips.split(',')
        for i in zips:
            zip_data.append({
                'code': i,
                'city': city
            })
    Zip.objects.bulk_create(Zip(**i) for i in zip_data)


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0004_load_cities'),
    ]

    operations = [
        migrations.CreateModel(
            name='Zip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=32, verbose_name='code')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zip_set', to='geo.City')),
            ],
        ),
        migrations.RunPython(move_zips_to_separate_table),
        migrations.RemoveField(
            model_name='city',
            name='zips',
        ),
        migrations.AlterField(
            model_name='zip',
            name='city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='zips', to='geo.City'),
        ),
        migrations.RemoveField(
            model_name='address',
            name='state',
        ),
        migrations.RemoveField(model_name='address', name='zip'),
        migrations.AddField(
            model_name='address',
            name='zip',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='geo.Zip'),
        ),
        migrations.AlterField(
            model_name='address',
            name='address',
            field=models.CharField(blank=True, max_length=255, verbose_name='address'),
        ),
    ]
