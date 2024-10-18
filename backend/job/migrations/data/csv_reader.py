import csv

from job import constants


def get_skills_from_csv(csv_file_path):
    skills = {}
    with open(csv_file_path) as csv_file:
        csv_reader = csv.DictReader(csv_file,
                                    delimiter=constants.CSV_DELIMITER)
        for row in csv_reader:
            skills[row['skill']] = {
                    'description': row['description'],
                    'type': row['type']
                }
    return skills


def get_column_from_csv(csv_file_path, column_name):
    csv_data = set()
    with open(csv_file_path) as csv_file:
        csv_reader = csv.DictReader(csv_file,
                                    delimiter=constants.CSV_DELIMITER)
        for row in csv_reader:
            csv_data.add(row[column_name])
    return csv_data
