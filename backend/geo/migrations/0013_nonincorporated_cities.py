import os

from django.db import migrations

from geo.migrations.data import csv_reader


CURRENT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
CITIES_CSV_FILE = 'us_cities.csv'
CITIES_CSV_PATH = os.path.join(CURRENT_DIR_PATH, 'data', CITIES_CSV_FILE)


def load_cities(apps, schema_editor):
    State = apps.get_model("geo", "State")
    City = apps.get_model("geo", "City")
    Zip = apps.get_model("geo", "Zip")
    state_cities = csv_reader.get_cities_from_csv(
        CITIES_CSV_PATH, incorporated='False')
    states = State.objects.all()
    states = {i.abbreviation: i for i in states}
    city_data = []
    for state_abbr, cities in state_cities.items():
        if state_abbr in states:
            state = states[state_abbr]
            for i in cities:
                city_data.append({
                    'name': i['city'],
                    'state': state,
                    'zips': i['zips'],
                    'timezone': i['timezone']
                })
    City.objects.bulk_create(
        City(name=i['name'], state=i['state'], timezone=i['timezone'])
        for i in city_data
    )
    zips_data = []
    for city in city_data:
        city_obj = City.objects.get(name=city['name'], state=city['state'])
        for code in city['zips']:
            zips_data.append({'city': city_obj, 'code': code})
    Zip.objects.bulk_create(Zip(**i) for i in zips_data)


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0012_auto_20190312_1400'),
    ]

    operations = [migrations.RunPython(load_cities)]
