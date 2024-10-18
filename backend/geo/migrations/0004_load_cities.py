import os

from django.db import migrations

from geo.migrations.data import csv_reader


CURRENT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
CITIES_CSV_FILE = 'us_cities.csv'
CITIES_CSV_PATH = os.path.join(CURRENT_DIR_PATH, 'data', CITIES_CSV_FILE)


def load_cities(apps, schema_editor):
    State = apps.get_model("geo", "State")
    City = apps.get_model("geo", "City")
    state_cities = csv_reader.get_cities_from_csv(
        CITIES_CSV_PATH, incorporated='True')
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
                    'zips': ','.join(i['zips'])
                })
    City.objects.bulk_create(City(**i) for i in city_data)


class Migration(migrations.Migration):

    dependencies = [
        ('geo', '0003_city_model'),
    ]

    operations = [migrations.RunPython(load_cities)]
