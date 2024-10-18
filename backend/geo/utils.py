from django.db import models as orm

from geo import models


def charfield(value):
    return orm.Value(value, output_field=orm.CharField())


def integerfield(value):
    return orm.Value(value, output_field=orm.IntegerField())


def get_locations(search_param):
    """
    Return list of locations (zip, city, state) which contains search_param.
    '_type_id' is used only for ordering.
    """
    zip_codes = (models.Zip.objects
                           .annotate(
                               name=orm.F('code'),
                               _type=charfield('Zip Code'),
                               _type_id=integerfield(1),
                               _state_id=charfield(''))
                           .values('name', '_type', '_type_id', '_state_id')
                           .filter(name__icontains=search_param))
    cities = (models.City.objects
                         .annotate(
                             _type=charfield('City'),
                             _type_id=integerfield(2),
                             _state_id=orm.F('state__abbreviation'))
                         .values('name', '_type', '_type_id', '_state_id')
                         .filter(name__icontains=search_param))
    states = (models.State.objects
                          .annotate(
                              _type=charfield('State'),
                              _type_id=integerfield(3),
                              _state_id=orm.F('abbreviation'))
                          .values('name', '_type', '_type_id', '_state_id')
                          .filter(name__icontains=search_param))
    result_query = cities.union(states, zip_codes)
    return list(result_query.order_by('_type_id', 'name'))


def create_or_update_instance_address(instance, address_data):
    if instance.address is not None:
        for attr, val in address_data.items():
            setattr(instance.address, attr, val)
        instance.address.save()
    else:
        instance.address = models.Address.objects.create(**address_data)
