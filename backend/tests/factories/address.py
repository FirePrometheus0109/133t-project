import faker

from geo import models
from tests import utils

fake = faker.Faker()


def create_address(**kwargs):
    country = utils.get_random_database_object(models.Country.objects)
    city = utils.get_random_database_object(models.City.objects)
    zip_code = utils.get_random_database_object(city.zips)
    address_data = {
        'address': fake.address().replace('\n', ' '),
        'city': city,
        'country': country,
        'zip': zip_code
    }
    address_data.update(**kwargs)
    address = models.Address(**address_data)
    address.save()
    return address
