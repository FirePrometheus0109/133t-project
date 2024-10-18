from rest_framework import exceptions

from geo import constants


def validate_zip_belongs_to_the_city(zip_code, city):
    if (not city and zip_code or
            (all((zip_code, city)) and zip_code.city != city)):
        raise exceptions.ValidationError({
            'zip': constants.ZIP_SHOULD_BELONG_TO_THE_CITY
        })
