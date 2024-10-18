import csv
from itertools import groupby


def get_cities_from_csv(csv_file_path, incorporated):
    cities = []
    with open(csv_file_path) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row['incorporated'] == incorporated:
                cities.append(
                    {
                        'city': row['city'],
                        'state': row['state_id'],
                        'zips': row['zips'].split(),
                        'timezone': row['timezone']
                    }
                )

    state_cities = {}
    for state, cities in groupby(cities, key=lambda x: x['state']):
        state_cities.update({state:  list(cities)})
    return state_cities
