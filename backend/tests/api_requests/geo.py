from django import urls


def get_countries(client):
    return client.get(urls.reverse('geo:api_v1:country-list'))


def get_cities(client, query_params=None):
    return client.get(urls.reverse('geo:api_v1:city-list'),
                      query_params if query_params else {})


def get_locations(client, query_params=None):
    return client.get(
        urls.reverse('geo:api_v1:locations'),
        query_params if query_params else {})


def get_timezones(client, query_params=None):
    return client.get(
        urls.reverse('geo:api_v1:timezone-list'),
        query_params if query_params else {}
    )
