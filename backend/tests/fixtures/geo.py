import pytest
import pytz

from geo import models


@pytest.fixture
def country_usa(db):
    return models.Country.objects.get(name='USA')


@pytest.fixture
def state_alabama(country_usa):
    return country_usa.state_set.get(name='Alabama')


@pytest.fixture
def state_new_york(country_usa):
    return country_usa.state_set.get(name='New York')


@pytest.fixture
def state_iowa(country_usa):
    return country_usa.state_set.get(name='Iowa')


@pytest.fixture
def city_ashville(state_alabama):
    return state_alabama.cities.get(name='Ashville')


@pytest.fixture
def city_new_york(state_new_york):
    return state_new_york.cities.get(name='New York')


@pytest.fixture
def city_packwood(state_iowa):
    return state_iowa.cities.get(name='Packwood')


@pytest.fixture
def zip_ashville(city_ashville):
    return city_ashville.zips.get(code='35953')


@pytest.fixture
def zip_new_york(city_new_york):
    return city_new_york.zips.get(code='10001')


@pytest.fixture
def zip_packwood(city_packwood):
    return city_packwood.zips.get(code='52580')


@pytest.fixture
def timezones(db):
    return pytz.all_timezones


@pytest.fixture
def tz_new_york():
    return 'America/New_York'


@pytest.fixture
def tz_london():
    return 'Europe/London'
